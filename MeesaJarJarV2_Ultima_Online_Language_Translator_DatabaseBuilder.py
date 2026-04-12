# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Offline cache builder — multithreaded + batched.
# Spins up one thread per language group so multiple languages
# are translated simultaneously, each sending batches of
# BATCH_SIZE messages per Ollama call.
#
# Tune WORKER_THREADS to match your GPU. Start at 3, go up if
# Ollama handles the load cleanly, down if you see timeouts.
#
# Fully resumable — stop and restart anytime.
# -------------------------------------------------------------#

import clr
clr.AddReference("System")
import System
from System.IO        import Directory, File, SearchOption
from System.Net       import WebClient, WebException
from System.Text      import Encoding
from System.Threading import Thread, ThreadStart, Monitor, Mutex
import re as _re

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
JOURNAL_DIR = r"C:\Program Files (x86)\UOForever\UO\ForeverOnline\Data\Client\JournalLogs"
CACHE_FILE  = r"C:\Program Files (x86)\UOForever\UO\ForeverOnline\Data\Client\uo_translation_cache.json"

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:1b"

# Messages per Ollama call per thread
BATCH_SIZE = 10

# How many languages to translate in parallel.
# Rule of thumb: start at 3, watch your GPU utilisation.
# Each thread makes its own HTTP connection to Ollama.
WORKER_THREADS = 3

# Flush cache to disk after this many newly translated pairs (across all threads)
SAVE_EVERY_PAIRS = 100

SKIP_SENDERS = ["System", "BASEFONT"]

LANGUAGES = [
    "English",
    "Chinese (Mandarin)",
    "Spanish",
    "French",
    "German",
    "Japanese",
    "Korean",
    "Portuguese",
    "Italian",
    "Russian",
    "Polish",
    "Arabic",
    "Hindi",
]

# ---------------------------------------------------------------------------
# SHARED STATE  (protected by _cache_lock)
# ---------------------------------------------------------------------------
_cache       = {}           # { message: { lang: translation } }
_cache_lock  = object()     # used with Monitor.Enter / Monitor.Exit
_done_pairs  = [0]          # wrapped in list so threads can mutate it
_error_pairs = [0]
_unsaved     = [0]
_progress    = {}           # { lang: (done, total) }

# ---------------------------------------------------------------------------
# JOURNAL PARSING
# ---------------------------------------------------------------------------
_TIMESTAMP_RE = _re.compile(r'^\[\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\]')

def _parse_message(line):
    line = line.strip()
    if not line or not _TIMESTAMP_RE.match(line):
        return None
    close = line.find("]")
    line = line[close + 1:].strip()
    colon = line.find(":")
    if colon == -1:
        return None
    sender  = line[:colon].strip()
    message = line[colon + 1:].strip()
    if not message:
        return None
    for skip in SKIP_SENDERS:
        if skip.lower() in sender.lower():
            return None
    if not _re.search(r'[a-zA-Z]', message):
        return None
    if message[0] in ('(', '%', '[', '<', '{', '}'):
        return None
    return message


def _collect_messages():
    unique = set()
    try:
        txt_files = Directory.GetFiles(
            JOURNAL_DIR, "*.txt", SearchOption.AllDirectories)
    except System.Exception as e:
        print("ERROR reading journal dir: {}".format(str(e.Message)))
        return []
    for filepath in txt_files:
        try:
            lines = File.ReadAllLines(filepath)
        except System.Exception:
            continue
        for raw in lines:
            msg = _parse_message(str(raw))
            if msg:
                unique.add(msg)
    return sorted(unique, key=lambda s: s.lower())

# ---------------------------------------------------------------------------
# DISK CACHE
# ---------------------------------------------------------------------------
def _json_escape(s):
    s = str(s)
    s = s.replace("\\", "\\\\")
    s = s.replace('"',  '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    s = s.replace("\t", "\\t")
    return s


def _json_unescape(s):
    return (s.replace('\\"', '"')
             .replace('\\\\', '\\')
             .replace('\\n', '\n')
             .replace('\\r', '\r')
             .replace('\\t', '\t'))


def _load_cache():
    result = {}
    if not File.Exists(CACHE_FILE):
        print("No existing cache file, starting fresh.")
        return result
    try:
        text = File.ReadAllText(CACHE_FILE)
        outer = _re.findall(
            r'"((?:[^"\\]|\\.)*?)"\s*:\s*\{([^{}]*)\}', text, _re.DOTALL)
        for msg_esc, inner_text in outer:
            msg = _json_unescape(msg_esc)
            langs = {}
            pairs = _re.findall(
                r'"((?:[^"\\]|\\.)*?)"\s*:\s*"((?:[^"\\]|\\.)*?)"', inner_text)
            for lang_esc, trans_esc in pairs:
                langs[_json_unescape(lang_esc)] = _json_unescape(trans_esc)
            result[msg] = langs
        print("Loaded {} cached messages from disk.".format(len(result)))
    except System.Exception as e:
        print("Cache load error: {}".format(str(e.Message)))
    return result


def _save_cache_locked():
    """Must be called while holding _cache_lock."""
    try:
        lines = ["{"]
        keys = list(_cache.keys())
        for ki, msg in enumerate(keys):
            comma_outer = "," if ki < len(keys) - 1 else ""
            lines.append('  "{}": {{'.format(_json_escape(msg)))
            langs = _cache[msg]
            lang_keys = list(langs.keys())
            for li, lang in enumerate(lang_keys):
                comma_inner = "," if li < len(lang_keys) - 1 else ""
                lines.append('    "{}": "{}"{}'.format(
                    _json_escape(lang),
                    _json_escape(langs[lang]),
                    comma_inner))
            lines.append("  }}{}".format(comma_outer))
        lines.append("}")
        File.WriteAllText(CACHE_FILE, "\n".join(lines))
    except System.Exception as e:
        print("  [SAVE ERROR] {}".format(str(e.Message)[:80]))

# ---------------------------------------------------------------------------
# OLLAMA
# ---------------------------------------------------------------------------
def _json_escape_prompt(s):
    s = s.replace("\\", "\\\\")
    s = s.replace('"',  '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    s = s.replace("\t", "\\t")
    return '"' + s + '"'


def _parse_ollama_response(resp):
    key = '"response":'
    idx = resp.find(key)
    if idx == -1:
        return ""
    start = resp.find('"', idx + len(key))
    if start == -1:
        return ""
    out = []
    i = start + 1
    while i < len(resp):
        c = resp[i]
        if c == '\\' and i + 1 < len(resp):
            nc = resp[i + 1]
            out.append({'n':'\n','t':'\t','"':'"','\\':'\\','r':'\r'}.get(nc, nc))
            i += 2
            continue
        if c == '"':
            break
        out.append(c)
        i += 1
    return "".join(out).strip()


def _parse_numbered_response(text, expected_count):
    pattern = _re.compile(r'^\s*\d+[\.\)]\s*(.+)', _re.MULTILINE)
    results = [m.strip() for m in pattern.findall(text)]
    while len(results) < expected_count:
        results.append(None)
    return results[:expected_count]


def _translate_batch(messages, language):
    numbered = "\n".join(
        "{}. {}".format(i + 1, msg) for i, msg in enumerate(messages))
    prompt = (
        "Translate each of the following messages into {lang}.\n"
        "Return ONLY a numbered list with one translation per line, "
        "in the exact same order. No explanations, no extra text.\n\n"
        "{msgs}"
    ).format(lang=language, msgs=numbered)
    body = (
        '{{"model":"{m}","prompt":{p},"stream":false,'
        '"options":{{"temperature":0.1,"num_predict":1024,"top_k":10}}}}'
    ).format(m=OLLAMA_MODEL, p=_json_escape_prompt(prompt))
    try:
        wc = WebClient()
        wc.Headers.Add("Content-Type", "application/json")
        wc.Encoding = Encoding.UTF8
        rb = wc.UploadData(OLLAMA_URL, "POST", Encoding.UTF8.GetBytes(body))
        raw = _parse_ollama_response(Encoding.UTF8.GetString(rb))
        return _parse_numbered_response(raw, len(messages))
    except System.Exception as e:
        print("  [{}] Ollama error: {}".format(language, str(e.Message)[:60]))
        return [None] * len(messages)

# ---------------------------------------------------------------------------
# WORKER  — one per language (or language group)
# ---------------------------------------------------------------------------
def _worker(languages_for_this_thread, all_messages):
    """
    Runs in its own thread. Processes a list of languages sequentially,
    but runs concurrently with other threads handling different languages.
    Writes results into _cache under _cache_lock.
    """
    for lang in languages_for_this_thread:
        # Figure out which messages still need this language (read under lock)
        Monitor.Enter(_cache_lock)
        try:
            todo = [m for m in all_messages
                    if m not in _cache or lang not in _cache[m]]
        finally:
            Monitor.Exit(_cache_lock)

        if not todo:
            print("[{}] already complete, skipping.".format(lang))
            _progress[lang] = (0, 0)
            continue

        print("[{}] {} messages to translate ({} batches of {})...".format(
            lang, len(todo),
            (len(todo) + BATCH_SIZE - 1) // BATCH_SIZE,
            BATCH_SIZE))

        local_done   = 0
        local_errors = 0

        for batch_start in range(0, len(todo), BATCH_SIZE):
            batch   = todo[batch_start:batch_start + BATCH_SIZE]
            results = _translate_batch(batch, lang)

            # Write results into shared cache under lock
            Monitor.Enter(_cache_lock)
            try:
                for msg, translation in zip(batch, results):
                    if msg not in _cache:
                        _cache[msg] = {}
                    if translation:
                        _cache[msg][lang] = translation
                        _done_pairs[0]  += 1
                        _unsaved[0]     += 1
                        local_done      += 1
                    else:
                        _error_pairs[0] += 1
                        local_errors    += 1

                # Flush to disk if threshold reached
                if _unsaved[0] >= SAVE_EVERY_PAIRS:
                    _save_cache_locked()
                    _unsaved[0] = 0
                    print("  [Saved] {} total pairs in cache  (thread: {})".format(
                        _done_pairs[0], lang))
            finally:
                Monitor.Exit(_cache_lock)

        _progress[lang] = (local_done, len(todo))
        print("  [{}] complete. Translated: {}  Errors: {}".format(
            lang, local_done, local_errors))

    # Each thread does a final save when it finishes all its languages
    Monitor.Enter(_cache_lock)
    try:
        _save_cache_locked()
    finally:
        Monitor.Exit(_cache_lock)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    global _cache

    print("=== UO Translation Cache Builder (Batched + Multithreaded) ===")
    print("Languages    : {}".format(len(LANGUAGES)))
    print("Batch size   : {}".format(BATCH_SIZE))
    print("Worker threads: {}".format(WORKER_THREADS))
    print("Cache file   : {}".format(CACHE_FILE))
    print("")

    print("Collecting unique messages from journal logs...")
    messages = _collect_messages()
    total_msgs = len(messages)
    print("Unique messages: {}".format(total_msgs))

    print("Loading existing cache...")
    _cache = _load_cache()

    already_done = sum(len(v) for v in _cache.values())
    total_pairs  = total_msgs * len(LANGUAGES)
    remaining    = total_pairs - already_done
    est_calls    = (remaining + BATCH_SIZE - 1) // BATCH_SIZE
    est_calls_threaded = (est_calls + WORKER_THREADS - 1) // WORKER_THREADS

    print("Already cached  : {} / {}".format(already_done, total_pairs))
    print("Remaining pairs : {}".format(remaining))
    print("Est. API calls  : ~{} total  (~{} per thread)".format(
        est_calls, est_calls_threaded))
    print("")

    # Distribute languages across threads as evenly as possible
    buckets = [[] for _ in range(WORKER_THREADS)]
    for i, lang in enumerate(LANGUAGES):
        buckets[i % WORKER_THREADS].append(lang)

    print("Language assignments:")
    for ti, bucket in enumerate(buckets):
        print("  Thread {}: {}".format(ti + 1, ", ".join(bucket)))
    print("")

    # Launch threads
    threads = []
    for bucket in buckets:
        if not bucket:
            continue
        # IronPython needs a closure workaround for loop variables
        def make_target(b):
            def target():
                _worker(b, messages)
            return target

        t = Thread(ThreadStart(make_target(bucket)))
        t.IsBackground = True
        t.Start()
        threads.append(t)

    print("All {} threads running...\n".format(len(threads)))

    # Wait for all threads to finish
    for t in threads:
        t.Join()

    # Final save
    Monitor.Enter(_cache_lock)
    try:
        _save_cache_locked()
    finally:
        Monitor.Exit(_cache_lock)

    print("\n=== Complete ===")
    print("Messages   : {}".format(total_msgs))
    print("Languages  : {}".format(len(LANGUAGES)))
    print("New pairs  : {}".format(_done_pairs[0]))
    print("Errors     : {}".format(_error_pairs[0]))
    print("Total cache: {} messages".format(len(_cache)))
    print("Saved to   : {}".format(CACHE_FILE))

    print("\nPer-language summary:")
    for lang in LANGUAGES:
        if lang in _progress:
            done, total = _progress[lang]
            print("  {:30s}  {}/{}".format(lang, done, total))


main()