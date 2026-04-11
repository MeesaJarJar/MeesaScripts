# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Ultima Online 55 Language Translator using
# Ollama Local, which allows for you to specify Gemma
# or any other model to use to use as a translator. This is
# intended to be a proof of concept to help bring UO into
# more languages. Now with Compact / Expanded toggle and
# overhead translated speech bubbles above the speaker!
# -------------------------------------------------------------#

import clr
clr.AddReference("System")
import System
from System.Net  import WebClient, WebException
from System.Text import Encoding
Journal.Clear()

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
OLLAMA_URL       = "http://localhost:11434/api/generate"
OLLAMA_MODEL     = "gemma3:1b"
TARGET_LANGUAGE  = "Spanish"
POLL_INTERVAL_MS = 2000
CONTEXT_LINES    = 3
SYSTEM_HUE       = 946
DEBUG            = True

TRANSLATE_TYPES = ('Regular', 'Yell', 'Whisper', 'Encoded', 'Special',
                   'Guild', 'Alliance', 'Party')

IGNORE_CONTAINS = [
    "[translated]", "[translator]",
    "your house", "defenders are needed",
    "writ of lease",
]

# ---------------------------------------------------------------------------
# HEAD MESSAGE CONFIG
# ---------------------------------------------------------------------------
# When a translation is ready we search for the speaker within HEAD_MSG_RANGE
# tiles and call Mobiles.Message() to show the translation above their head.
#
# HEAD_MSG_ENABLED  - set False to turn off overhead bubbles entirely
# HEAD_MSG_HUE      - colour of the overhead text (matches HUE_TRANS by default)
# HEAD_MSG_RANGE    - tile radius searched for the speaker mobile
# HEAD_MSG_PREFIX   - short tag prepended to every overhead translation
# ---------------------------------------------------------------------------
HEAD_MSG_ENABLED = True
HEAD_MSG_HUE     = 68      # same green as HUE_TRANS in the gump
HEAD_MSG_RANGE   = 12      # search radius in tiles
HEAD_MSG_PREFIX  = "[T] "  # visible prefix above the mobiles head

# ---------------------------------------------------------------------------
# LAYOUT PROFILES
# ---------------------------------------------------------------------------
PROFILES = {
    "expanded": {
        "WIN_W":        860,
        "WIN_H":        390,
        "COL_W":        390,
        "MARGIN":       14,
        "ROWS_Y_START": 72,
        "ROW_H":        18,
        "MAX_ROWS":     15,
        "WRAP_CHARS":   20,
        "NAME_CHARS":   15,
        "LABEL_OFFSET": 100,
    },
    "compact": {
        "WIN_W":        520,
        "WIN_H":        220,
        "COL_W":        220,
        "MARGIN":       10,
        "ROWS_Y_START": 52,
        "ROW_H":        14,
        "MAX_ROWS":     8,
        "WRAP_CHARS":   15,
        "NAME_CHARS":   10,
        "LABEL_OFFSET": 72,
    },
}

# ---------------------------------------------------------------------------
# GUMP CONSTANTS
# ---------------------------------------------------------------------------
GUMP_ID = 0x7ABC
GUMP_X  = 100
GUMP_Y  = 80

HUE_TITLE    = 1153
HUE_HEADER   = 1150
HUE_ORIG     = 1149
HUE_TRANS    = 68
HUE_CACHE    = 1109
HUE_BTN      = 1152
HUE_BTN_WARN = 33
HUE_BTN_TOG  = 88

BTN_CLOSE    = 1
BTN_CLEAR    = 2
BTN_TOGGLE   = 3

# ---------------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------------
_translation_cache  = {}
_display_rows       = []
_last_journal_count = 0
_name_hues          = {}
_compact_mode       = False

# ---------------------------------------------------------------------------
# MOBILE FINDER
# ---------------------------------------------------------------------------
def _find_mobile_by_name(name):
    """
    Search nearby mobiles for one whose Name matches `name` exactly.
    Returns the Mobile object on the first match, or None if not found.
    The search radius is controlled by HEAD_MSG_RANGE in CONFIG above.
    """
    if not name:
        return None

    name = str(name).strip()

    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled          = True
    mobileFilter.RangeMin         = 0
    mobileFilter.RangeMax         = HEAD_MSG_RANGE
    mobileFilter.CheckLineOfSight = False
    mobileFilter.IsGhost          = False

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    for mobile in foundMobiles:
        if str(mobile.Name).strip() == name:
            return mobile

    return None


def _show_head_message(speaker_name, translated_text):
    """
    Locate the speaker and pop the translation above their head.
    Silently does nothing when:
      - HEAD_MSG_ENABLED is False
      - speaker_name is empty (system / world messages)
      - the translation is an error string
      - the mobile is not found within HEAD_MSG_RANGE tiles
    """
    if not HEAD_MSG_ENABLED:
        return
    if not speaker_name:
        return
    if translated_text.startswith("[ERR"):
        return

    # If the speaker is the player themselves, skip the mobile scan entirely
    # and use Player.Serial directly — its always available and exact.
    if str(speaker_name).strip() == str(Player.Name).strip():
        target = Mobiles.FindBySerial(Player.Serial)
        serial = Player.Serial
    else:
        target = _find_mobile_by_name(speaker_name)
        if target is None:
            if DEBUG:
                Misc.SendMessage(
                    "[T] HeadMsg: '{}' not in range {}.".format(
                        speaker_name, HEAD_MSG_RANGE),
                    SYSTEM_HUE)
            return
        serial = target.Serial

    Mobiles.Message(target, HEAD_MSG_HUE, HEAD_MSG_PREFIX + translated_text, False)

    if DEBUG:
        Misc.SendMessage(
            "[T] HeadMsg -> {} (0x{:X})".format(speaker_name, serial),
            SYSTEM_HUE)

# ---------------------------------------------------------------------------
# TEXT WRAP
# ---------------------------------------------------------------------------
def _wrap(text, width=30):
    text = str(text).replace("\n", " ").replace("\r", "")
    words = text.split()
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 <= width:
            current = (current + " " + w).strip()
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

# ---------------------------------------------------------------------------
# OLLAMA
# ---------------------------------------------------------------------------
def _json_escape(s):
    s = s.replace("\\", "\\\\")
    s = s.replace('"',  '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    s = s.replace("\t", "\\t")
    return '"' + s + '"'


def _parse_response(resp):
    key = '"response":'
    idx = resp.find(key)
    if idx == -1:
        return "[no response field]"
    start = resp.find('"', idx + len(key))
    if start == -1:
        return "[parse error]"
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
    return "".join(out)


def _call_ollama(prompt):
    body = (
        '{{"model":"{m}","prompt":{p},"stream":false,'
        '"options":{{"temperature":0.1,"num_predict":150,"top_k":10}}}}'
    ).format(m=OLLAMA_MODEL, p=_json_escape(prompt))
    try:
        wc = WebClient()
        wc.Headers.Add("Content-Type", "application/json")
        wc.Encoding = Encoding.UTF8
        rb = wc.UploadData(OLLAMA_URL, "POST", Encoding.UTF8.GetBytes(body))
        rs = Encoding.UTF8.GetString(rb)
        return True, _parse_response(rs).strip()
    except WebException as e:
        return False, "NET ERR: {}".format(str(e.Message)[:60])
    except System.Exception as e:
        return False, "ERR: {}".format(str(e.Message)[:60])


def _build_prompt(context_lines, line):
    ctx = ""
    if context_lines:
        ctx = "Context (do NOT translate):\n"
        for c in context_lines:
            ctx += "  - {}\n".format(c)
        ctx += "\n"
    return (
        "You are a silent translator inside Ultima Online. "
        "Translate the player message below to {lang}. "
        "Do not change the message, punctuation, other than translate to {lang} "
        "Do not change anything if the message is in {lang}. "
        "Output ONLY the translation, do not infer or interpret.\n\n"
        "{ctx}Message:\n{msg}"
    ).format(lang=TARGET_LANGUAGE, ctx=ctx, msg=line)


def _translate(line, context):
    key = line.strip()
    if key in _translation_cache:
        if DEBUG:
            Misc.SendMessage("[T] CACHE: {}".format(key[:40]), SYSTEM_HUE)
        return _translation_cache[key]
    if DEBUG:
        Misc.SendMessage("[T] Translating: {}".format(key[:40]), SYSTEM_HUE)
    ok, result = _call_ollama(_build_prompt(context, key))
    val = result if ok else "[ERR: {}]".format(result)
    _translation_cache[key] = val
    return val

# ---------------------------------------------------------------------------
# JOURNAL
# ---------------------------------------------------------------------------
def _get_name_hue(name):
    if name in _name_hues:
        return _name_hues[name]
    h = abs(hash(name)) % 1000
    hue = 20 + (h % 980)
    _name_hues[name] = hue
    return hue


def _get_new_entries():
    global _last_journal_count
    journal_list = Journal.GetJournalEntry(-1)
    total = len(journal_list)
    if total <= _last_journal_count:
        return []
    new_entries = journal_list[_last_journal_count:total]
    _last_journal_count = total
    return new_entries


def _should_skip(entry):
    if entry.Type not in TRANSLATE_TYPES:
        return True
    text = (entry.Text or "").strip()
    name = (entry.Name or "")
    if len(text) < 2:
        return True
    if (text.startswith("[") and text.endswith("]")) or \
       (text.startswith("(") and text.endswith(")")):
        inner = text[1:-1].strip()
        if inner and " " not in inner:
            return True
    if name and text.lower() == name.lower():
        return True
    combined = (name + ": " + text).lower()
    for ig in IGNORE_CONTAINS:
        if ig in combined:
            return True
    return False


def _clamp(text, n=500):
    text = str(text).replace("\n", " ").replace("\r", "")
    if len(text) > n:
        return text[:n - 1] + "~"
    return text

# ---------------------------------------------------------------------------
# GUMP
# ---------------------------------------------------------------------------
def _draw_gump():
    global _compact_mode

    p = PROFILES["compact"] if _compact_mode else PROFILES["expanded"]
    WIN_W        = p["WIN_W"]
    WIN_H        = p["WIN_H"]
    COL_W        = p["COL_W"]
    MARGIN       = p["MARGIN"]
    ROWS_Y_START = p["ROWS_Y_START"]
    ROW_H        = p["ROW_H"]
    MAX_ROWS     = p["MAX_ROWS"]
    WRAP_CHARS   = p["WRAP_CHARS"]
    NAME_CHARS   = p["NAME_CHARS"]
    LABEL_OFFSET = p["LABEL_OFFSET"]

    COL_LEFT_X  = MARGIN
    COL_RIGHT_X = MARGIN + COL_W + 20

    toggle_label = "[ Expand ]" if _compact_mode else "[ Compact ]"

    gd = Gumps.CreateGump(True, True, False, False)
    Gumps.AddPage(gd, 0)

    Gumps.AddBackground(gd, 0, 0, WIN_W, WIN_H, 9270)
    Gumps.AddAlphaRegion(gd, 0, 0, WIN_W, WIN_H)

    title_str = "[ MeesaJarJar`s UO Translator  >>  {} ]".format(TARGET_LANGUAGE)
    Gumps.AddLabel(gd, MARGIN, 10, HUE_TITLE, title_str)

    if not _compact_mode:
        Gumps.AddLabel(gd, COL_LEFT_X,  40, HUE_HEADER, "Original Message")
        Gumps.AddLabel(gd, COL_RIGHT_X, 40, HUE_HEADER, "Translated")
        Gumps.AddImageTiled(gd, MARGIN, 60, WIN_W - MARGIN * 2, 2, 9304)
    else:
        Gumps.AddLabel(gd, COL_LEFT_X,  30, HUE_HEADER, "Original")
        Gumps.AddLabel(gd, COL_RIGHT_X, 30, HUE_HEADER, "Translated")
        Gumps.AddImageTiled(gd, MARGIN, 44, WIN_W - MARGIN * 2, 2, 9304)

    Gumps.AddImageTiled(gd, COL_RIGHT_X - 12, 36, 2, WIN_H - 60, 9304)

    visible = []
    line_count = 0
    for orig, trans in reversed(_display_rows):
        msg_o = orig.split(": ", 1)[1] if ": " in orig else orig
        msg_t = trans.split(": ", 1)[1] if ": " in trans else trans
        wrap_o = _wrap(msg_o, WRAP_CHARS)
        wrap_t = _wrap(msg_t, WRAP_CHARS)
        needed = max(len(wrap_o), len(wrap_t))
        if line_count + needed > MAX_ROWS:
            break
        visible.append((orig, trans))
        line_count += needed
    visible = visible[::-1]

    y = ROWS_Y_START

    if not visible:
        Gumps.AddLabel(gd, COL_LEFT_X, y, HUE_CACHE, "Waiting for chat...")
    else:
        for (orig, trans) in visible:
            if ": " in orig:
                name_o, msg_o = orig.split(": ", 1)
                hue_o = _get_name_hue(name_o)
            else:
                name_o, msg_o = None, orig
                hue_o = HUE_ORIG

            if ": " in trans:
                name_t, msg_t = trans.split(": ", 1)
                hue_t = _get_name_hue(name_t)
            else:
                name_t, msg_t = None, trans
                hue_t = HUE_TRANS

            wrap_o = _wrap(msg_o, WRAP_CHARS)
            wrap_t = _wrap(msg_t, WRAP_CHARS)
            max_lines = max(len(wrap_o), len(wrap_t))

            for li in range(max_lines):
                yy = y + (li * ROW_H)

                if li < len(wrap_o):
                    line = wrap_o[li]
                    if li == 0 and name_o:
                        Gumps.AddLabel(gd, COL_LEFT_X, yy, hue_o,
                                       str(name_o)[:NAME_CHARS] + ":")
                        Gumps.AddLabel(gd, COL_LEFT_X + LABEL_OFFSET,
                                       yy, HUE_ORIG, line)
                    else:
                        Gumps.AddLabel(gd,
                                       COL_LEFT_X + (LABEL_OFFSET if name_o else 0),
                                       yy, HUE_ORIG, line)

                if li < len(wrap_t):
                    line = wrap_t[li]
                    if li == 0 and name_t:
                        Gumps.AddLabel(gd, COL_RIGHT_X, yy, hue_t,
                                       str(name_t)[:NAME_CHARS] + "  :")
                        Gumps.AddLabel(gd, COL_RIGHT_X + LABEL_OFFSET,
                                       yy, HUE_TRANS, line)
                    else:
                        Gumps.AddLabel(gd,
                                       COL_RIGHT_X + (LABEL_OFFSET if name_t else 0),
                                       yy, HUE_TRANS, line)

            y += max_lines * ROW_H

    btn_y = WIN_H - 34

    Gumps.AddLabel(gd, MARGIN, btn_y + 6, HUE_CACHE,
                   "Cache: {}  |  Rows: {}".format(
                       len(_translation_cache), len(visible)))

    Gumps.AddButton(gd, WIN_W - 280, btn_y, 4017, 4019, BTN_TOGGLE, 1, 0)
    Gumps.AddLabel (gd, WIN_W - 245, btn_y + 6, HUE_BTN_TOG, toggle_label)

    Gumps.AddButton(gd, WIN_W - 180, btn_y, 4017, 4019, BTN_CLEAR, 1, 0)
    Gumps.AddLabel (gd, WIN_W - 145, btn_y + 6, HUE_BTN, "Clear")

    Gumps.AddButton(gd, WIN_W - 80,  btn_y, 4020, 4022, BTN_CLOSE, 1, 0)
    Gumps.AddLabel (gd, WIN_W - 45,  btn_y + 6, HUE_BTN_WARN, "Close")

    Gumps.CloseGump(GUMP_ID)
    Gumps.SendGump(GUMP_ID, Player.Serial, GUMP_X, GUMP_Y,
                   gd.gumpDefinition, gd.gumpStrings)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    global _last_journal_count, _display_rows, _compact_mode

    Misc.SendMessage("[Translator] Starting...", SYSTEM_HUE)
    Player.ChatSay("Starting Meesa Translator.")
    seed = Journal.GetJournalEntry(-1)
    _last_journal_count = len(seed)

    _display_rows = []
    _draw_gump()

    running = True
    while running:
        Misc.Pause(POLL_INTERVAL_MS)

        gd = Gumps.GetGumpData(GUMP_ID)
        if gd and gd.buttonid > 0:
            if gd.buttonid == BTN_CLOSE:
                running = False
                Gumps.CloseGump(GUMP_ID)
                break
            elif gd.buttonid == BTN_CLEAR:
                del _display_rows[:]
            elif gd.buttonid == BTN_TOGGLE:
                _compact_mode = not _compact_mode
                _draw_gump()
                continue

        new_entries = _get_new_entries()
        p = PROFILES["compact"] if _compact_mode else PROFILES["expanded"]

        for i, entry in enumerate(new_entries):
            if _should_skip(entry):
                continue

            speaker_name = entry.Name or None
            display_orig = "{}: {}".format(speaker_name, entry.Text) \
                           if speaker_name else entry.Text

            ctx = []
            for j in range(max(0, i - CONTEXT_LINES), i):
                if not _should_skip(new_entries[j]):
                    ctx.append(new_entries[j].Text)

            trans = _translate(entry.Text.strip(), ctx)

            display_trans = "{}: {}".format(speaker_name, trans) \
                            if speaker_name else trans

            _display_rows.append((display_orig, display_trans))

            # ---------- HEAD MESSAGE ----------
            # After the translation comes back, find the speaker in the world
            # and pop the translated text above their head. Gracefully skips
            # system messages (no name), out-of-range speakers, and errors.
            _show_head_message(speaker_name, trans)
            # ----------------------------------

        max_keep = p["MAX_ROWS"] * 3
        if len(_display_rows) > max_keep:
            del _display_rows[:p["MAX_ROWS"]]

        _draw_gump()


main()