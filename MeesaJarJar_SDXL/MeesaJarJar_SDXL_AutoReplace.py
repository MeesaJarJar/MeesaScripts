# MeesaJarJar MeesaJarJar.com MeesaJarJar.shop Github.com/MeesaJarJar - SDXL Turbo AutoReplace
# Continuously scans nearby statics as you walk around.
# Generates AI art for newly seen objects automatically.

# Config
ART_DIR = r"C:\Program Files (x86)\UOForever\UO\override\art"
WORKER_COUNT = 3  # parallel generation threads

import os
import clr
import json
import base64
import tempfile
import subprocess
import time
import threading
import queue as thread_queue

clr.AddReference("System.Drawing")
from System.Drawing import Imaging
clr.AddReference("System.IO")
from System.IO import MemoryStream, StreamReader
from System import Array, Byte
from System.Net import WebRequest
clr.AddReference("System.Reflection")
from System.Reflection import BindingFlags
import System

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "sdxl_autoreplace_log.txt")


def log(msg):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(time.strftime("%H:%M:%S") + " [SDXL] " + msg + "\n")
    except:
        pass


PYTHON = os.path.join(SCRIPT_DIR, "python_embedded", "python.exe")
SERVER_SCRIPT = os.path.join(SCRIPT_DIR, "MeesaJarJar_SDXL_Server.py")
SERVER_URL = "http://127.0.0.1:5555"
RANGE = 16
SCAN_INTERVAL = 3
GUMP_ID = 90002
PROMPT_FILE = os.path.join(SCRIPT_DIR, "sdxl_autoreplace_prompt.txt")
SEED_FILE = os.path.join(SCRIPT_DIR, "sdxl_autoreplace_seed.txt")

running = False
task_queue = thread_queue.Queue()
seen_ids = set()
processed = 0
failed = 0
skipped = 0
generated = 0
server_online = False
current_item = ""
stats_lock = threading.Lock()
workers = []

# Mutable refs so workers pick up live prompt/seed changes
prompt_ref = [""]
seed_ref = [0]


def load_prompt():
    try:
        if os.path.exists(PROMPT_FILE):
            with open(PROMPT_FILE, "r") as f:
                return f.read().strip()
    except:
        pass
    return ""


def save_prompt(text):
    try:
        with open(PROMPT_FILE, "w") as f:
            f.write(text)
    except:
        pass


def load_seed():
    try:
        if os.path.exists(SEED_FILE):
            with open(SEED_FILE, "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0


def save_seed(val):
    try:
        with open(SEED_FILE, "w") as f:
            f.write(str(val))
    except:
        pass


def show_gump(prompt_text="", status_text="", stats_text="", seed_text="0"):
    gd = Gumps.CreateGump()
    Gumps.AddPage(gd, 0)
    Gumps.AddBackground(gd, 0, 0, 340, 420, 9200)
    Gumps.AddLabel(gd, 15, 10, 2101, "AI AutoReplace")
    if server_online:
        Gumps.AddLabel(gd, 250, 10, 66, "SERVER: ON")
    else:
        Gumps.AddLabel(gd, 250, 10, 33, "SERVER: OFF")
    Gumps.AddButton(gd, 250, 28, 4005, 4006, 4, 1, 0)
    Gumps.AddLabel(gd, 280, 30, 2101, "Reconnect")
    Gumps.AddButton(gd, 250, 46, 4005, 4006, 5, 1, 0)
    Gumps.AddLabel(gd, 280, 48, 33, "Kill Server")
    python_ok = os.path.exists(PYTHON)
    if python_ok:
        Gumps.AddLabel(gd, 15, 30, 66, "Python: READY")
    else:
        Gumps.AddLabel(gd, 15, 30, 33, "Python: NOT FOUND - run setup_sdxl_python.py")
    Gumps.AddLabel(gd, 15, 50, 2101, "Prompt:")
    Gumps.AddTextEntry(gd, 15, 70, 300, 25, 1152, 0, prompt_text)
    Gumps.AddLabel(gd, 15, 100, 2101, "Suffix added to each item name automatically.")
    Gumps.AddLabel(gd, 15, 120, 2101, "Seed:")
    Gumps.AddTextEntry(gd, 55, 118, 80, 25, 1152, 1, seed_text)
    Gumps.AddButton(gd, 15, 155, 4005, 4006, 1, 1, 0)
    Gumps.AddLabel(gd, 50, 157, 66, "START")
    Gumps.AddButton(gd, 100, 155, 4005, 4006, 2, 1, 0)
    Gumps.AddLabel(gd, 135, 157, 2101, "STOP")
    Gumps.AddButton(gd, 200, 155, 4005, 4006, 3, 1, 0)
    Gumps.AddLabel(gd, 235, 157, 2101, "OPEN ART")
    Gumps.AddButton(gd, 15, 180, 4005, 4006, 6, 1, 0)
    Gumps.AddLabel(gd, 50, 182, 2101, "REPLACE SINGLE")
    Gumps.AddLabel(gd, 180, 182, 900, "(click an object)")
    if status_text:
        Gumps.AddLabel(gd, 15, 210, 55, status_text)
    if stats_text:
        Gumps.AddLabel(gd, 15, 235, 1152, stats_text)
    Gumps.SendGump(GUMP_ID, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)


def check_server():
    try:
        req = WebRequest.Create(SERVER_URL + "/health")
        req.Timeout = 2000
        resp = req.GetResponse()
        resp.Close()
        return True
    except:
        return False


def start_server():
    if check_server():
        log("Server already running.")
        return True
    if not os.path.exists(PYTHON):
        log("ERROR: Python not found at {}".format(PYTHON))
        Player.HeadMessage(33, "Python not found! Run setup_sdxl_python.py")
        return False
    if not os.path.exists(SERVER_SCRIPT):
        log("ERROR: Server script not found at {}".format(SERVER_SCRIPT))
        Player.HeadMessage(33, "sdxl_server.py not found next to script!")
        return False
    kill_server()
    Misc.Pause(500)
    log("Starting SDXL server.")
    Player.HeadMessage(1152, "Starting SDXL server...")
    try:
        subprocess.Popen([PYTHON, SERVER_SCRIPT])
    except Exception as e:
        log("ERROR launching server: {}".format(e))
        Player.HeadMessage(33, "Launch failed: " + str(e)[:60])
        return False
    for i in range(60):
        Misc.Pause(1000)
        if check_server():
            log("Server ready after {}s.".format(i + 1))
            Player.HeadMessage(66, "SDXL server ready!")
            return True
    log("ERROR: Server failed to start after 60s.")
    Player.HeadMessage(33, "Server failed to start! Check the server console window.")
    return False


def kill_server():
    global server_online
    log("Killing server.")
    try:
        from System.Diagnostics import Process
        for proc in Process.GetProcessesByName("python"):
            try:
                if proc.MainModule and "sdxl" in proc.MainModule.FileName.lower():
                    proc.Kill()
            except:
                pass
    except:
        pass
    os.system('taskkill /f /im python.exe /fi "MODULES eq *sdxl*" >nul 2>&1')
    server_online = False
    Player.HeadMessage(33, "Server killed.")


def send_to_server(image_path, prompt, hex_id, seed=0):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    data = json.dumps({"image": img_b64, "prompt": prompt, "hex": hex_id, "seed": seed}).encode("utf-8")
    req = WebRequest.Create(SERVER_URL + "/generate")
    req.Method = "POST"
    req.ContentType = "application/json"
    req.Timeout = 120000
    stream = req.GetRequestStream()
    stream.Write(Array[Byte](data), 0, len(data))
    stream.Close()
    resp = req.GetResponse()
    reader = StreamReader(resp.GetResponseStream())
    raw = reader.ReadToEnd()
    resp.Close()
    return json.loads(raw)


def get_item_name(item_id):
    try:
        itemData = Statics.GetItemData(item_id)
        if itemData and hasattr(itemData, "Name") and itemData.Name:
            return str(itemData.Name).lower().strip()
    except:
        pass
    return ""


def scan_nearby():
    global skipped
    px = Player.Position.X
    py = Player.Position.Y
    new_items = []
    for dx in range(-RANGE, RANGE + 1):
        for dy in range(-RANGE, RANGE + 1):
            x = px + dx
            y = py + dy
            tileinfo = Statics.GetStaticsTileInfo(x, y, Player.Map)
            if tileinfo and tileinfo.Count > 0:
                for tile in tileinfo:
                    key = (tile.StaticID, tile.Hue)
                    if key not in seen_ids:
                        seen_ids.add(key)
                        hex_id = "0x{:04X}".format(tile.StaticID)
                        out_path = os.path.join(ART_DIR, "{}.png".format(hex_id))
                        if os.path.exists(out_path):
                            with stats_lock:
                                skipped += 1
                            continue
                        name = get_item_name(tile.StaticID)
                        new_items.append((tile.StaticID, tile.Hue, name))
    return new_items


def process_item(item_id, hue, name, prompt, seed=0):
    global processed, failed
    hex_id = "0x{:04X}".format(item_id)
    out_path = os.path.join(ART_DIR, "{}.png".format(hex_id))
    if os.path.exists(out_path):
        return True

    item_img = Items.GetImage(item_id, hue)
    if item_img is None:
        log("GetImage failed: {}".format(hex_id))
        with stats_lock:
            failed += 1
        return False

    tmp_path = os.path.join(tempfile.gettempdir(), "sdxl_auto_{}.png".format(hex_id))
    item_img.Save(tmp_path, Imaging.ImageFormat.Png)

    full_prompt = "{}, {}".format(name, prompt) if name else prompt

    try:
        result = send_to_server(tmp_path, full_prompt, hex_id, seed)
        if result.get("ok"):
            with stats_lock:
                processed += 1
            return True
        else:
            log("Server error on {}: {}".format(hex_id, result.get("error", "unknown")))
            with stats_lock:
                failed += 1
            return False
    except Exception as e:
        log("Exception on {}: {}".format(hex_id, e))
        with stats_lock:
            failed += 1
        return False


def worker_loop():
    """Worker thread: pulls items from task_queue and generates art."""
    while True:
        item = task_queue.get()
        if item is None:  # poison pill — exit signal
            task_queue.task_done()
            break
        item_id, hue, name = item
        process_item(item_id, hue, name, prompt_ref[0], seed_ref[0])
        task_queue.task_done()


def start_workers():
    global workers
    stop_workers()
    for _ in range(WORKER_COUNT):
        t = threading.Thread(target=worker_loop, daemon=True)
        t.start()
        workers.append(t)
    log("Started {} worker threads.".format(WORKER_COUNT))


def stop_workers():
    global workers
    if not workers:
        return
    for _ in workers:
        task_queue.put(None)
    for t in workers:
        t.join(timeout=2)
    workers.clear()
    log("Workers stopped.")


# --- Startup ---
log("Script starting. ART_DIR={}".format(ART_DIR))

show_gump(status_text="Checking server...")
server_online = check_server()
if not server_online:
    show_gump(status_text="Server not running. Starting...")
    server_online = start_server()

saved_prompt = load_prompt()
saved_seed = str(load_seed())
seed_val = load_seed()
prompt_ref[0] = saved_prompt
seed_ref[0] = seed_val

if server_online:
    show_gump(saved_prompt, status_text="Server ready. Press START to begin.", seed_text=saved_seed)
else:
    show_gump(saved_prompt, status_text="Server offline. Press Reconnect.", seed_text=saved_seed)

last_scan = 0

while True:
    Misc.Pause(500)

    gd = Gumps.GetGumpData(GUMP_ID)
    if gd:
        if gd.buttonid == 1:  # START
            prompt = Gumps.GetTextByID(gd, 0)
            if not prompt or prompt.strip() == "":
                show_gump(prompt, "Enter a prompt first!", seed_text=str(seed_val))
                gd.buttonid = -1
                continue

            save_prompt(prompt.strip())
            seed_str = Gumps.GetTextByID(gd, 1)
            try:
                seed_val = int(seed_str)
            except:
                seed_val = 0
            save_seed(seed_val)
            prompt_ref[0] = prompt.strip()
            seed_ref[0] = seed_val

            if not server_online:
                if not start_server():
                    show_gump(prompt, "Server failed! Use Reconnect.", seed_text=str(seed_val))
                    gd.buttonid = -1
                    continue
                server_online = True

            running = True
            with stats_lock:
                processed = 0
                failed = 0
                skipped = 0
            seen_ids.clear()
            # Drain any leftover queue items
            while not task_queue.empty():
                try:
                    task_queue.get_nowait()
                    task_queue.task_done()
                except:
                    break
            last_scan = 0
            start_workers()
            log("START. Prompt='{}' Seed={} Workers={}".format(prompt.strip(), seed_val, WORKER_COUNT))
            show_gump(prompt, "Running ({} workers)... walk around!".format(WORKER_COUNT), seed_text=str(seed_val))
            gd.buttonid = -1

        elif gd.buttonid == 2:  # STOP
            running = False
            stop_workers()
            log("STOP. Done={} Skipped={} Failed={}".format(processed, skipped, failed))
            show_gump(saved_prompt, "Stopped. Done: {} | Skipped: {} | Failed: {}".format(
                processed, skipped, failed), seed_text=str(seed_val))
            gd.buttonid = -1

        elif gd.buttonid == 3:  # OPEN ART
            os.system('explorer "{}"'.format(ART_DIR))
            show_gump(saved_prompt, status_text="Opened art folder.", seed_text=str(seed_val))
            gd.buttonid = -1

        elif gd.buttonid == 4:  # RECONNECT
            server_online = check_server()
            if server_online:
                show_gump(saved_prompt, status_text="Server connected!", seed_text=str(seed_val))
            else:
                show_gump(saved_prompt, status_text="Server not found. Starting...", seed_text=str(seed_val))
                server_online = start_server()
                if server_online:
                    show_gump(saved_prompt, status_text="Server started!", seed_text=str(seed_val))
                else:
                    show_gump(saved_prompt, status_text="Failed to connect.", seed_text=str(seed_val))
            gd.buttonid = -1

        elif gd.buttonid == 5:  # KILL SERVER
            kill_server()
            show_gump(saved_prompt, status_text="Server killed.", seed_text=str(seed_val))
            gd.buttonid = -1

        elif gd.buttonid == 6:  # REPLACE SINGLE
            prompt = Gumps.GetTextByID(gd, 0)
            if not prompt or prompt.strip() == "":
                show_gump(prompt, "Enter a prompt first!", seed_text=str(seed_val))
                gd.buttonid = -1
                continue
            save_prompt(prompt.strip())
            seed_str = Gumps.GetTextByID(gd, 1)
            try:
                seed_val = int(seed_str)
            except:
                seed_val = 0
            save_seed(seed_val)

            if not server_online:
                if not start_server():
                    show_gump(prompt, "Server failed! Use Reconnect.", seed_text=str(seed_val))
                    gd.buttonid = -1
                    continue
                server_online = True

            show_gump(prompt, "Target the object to replace...", seed_text=str(seed_val))
            gd.buttonid = -1

            target = Target.PromptTarget("Select an object to replace")
            tile_id = 0
            tile_hue = 0

            if target and target != 0:
                item = Items.FindBySerial(target)
                if item:
                    tile_id = item.ItemID
                    tile_hue = item.Hue
                else:
                    tile_id = target

            if tile_id == 0:
                px = Player.Position.X
                py = Player.Position.Y
                for sdx in range(-1, 2):
                    for sdy in range(-1, 2):
                        if tile_id != 0:
                            break
                        tileinfo = Statics.GetStaticsTileInfo(px + sdx, py + sdy, Player.Map)
                        if tileinfo and tileinfo.Count > 0:
                            tile_id = tileinfo[0].StaticID
                            tile_hue = tileinfo[0].Hue

            if tile_id == 0:
                show_gump(prompt, "No object found to replace.", seed_text=str(seed_val))
                continue

            item_img = Items.GetImage(tile_id, tile_hue)
            if item_img is None:
                show_gump(prompt, "Could not get image for target.", seed_text=str(seed_val))
                continue

            hex_id = "0x{:04X}".format(tile_id)
            tmp_path = os.path.join(tempfile.gettempdir(), "sdxl_single_{}.png".format(hex_id))
            item_img.Save(tmp_path, Imaging.ImageFormat.Png)

            name = get_item_name(tile_id)
            full_prompt = "{}, {}".format(name, prompt.strip()) if name else prompt.strip()

            show_gump(prompt, "Generating for {}...".format(hex_id), seed_text=str(seed_val))
            try:
                result = send_to_server(tmp_path, full_prompt, hex_id, seed_val)
                if result.get("ok"):
                    show_gump(prompt, "Done! Generated {}.".format(hex_id),
                              "Path: {}".format(result.get("path", "")), str(seed_val))
                else:
                    show_gump(prompt, "Server error: {}".format(result.get("error", "unknown")),
                              seed_text=str(seed_val))
            except Exception as e:
                show_gump(prompt, "Failed: {}".format(str(e)[:80]), seed_text=str(seed_val))

    if not running:
        continue

    if not server_online:
        server_online = check_server()
        if not server_online:
            show_gump(saved_prompt, "Server offline! Reconnect to resume.", seed_text=str(seed_val))
            running = False
            stop_workers()
            continue

    now = time.time()
    if now - last_scan >= SCAN_INTERVAL:
        last_scan = now
        new_items = scan_nearby()
        for item in new_items:
            task_queue.put(item)

    q_size = task_queue.qsize()
    show_gump(
        saved_prompt,
        "Running ({} workers)... walk around!".format(WORKER_COUNT) if q_size == 0 else "Generating... queue: {}".format(q_size),
        "Done: {} | Skipped: {} | Failed: {} | Seen: {}".format(processed, skipped, failed, len(seen_ids)),
        str(seed_val)
    )