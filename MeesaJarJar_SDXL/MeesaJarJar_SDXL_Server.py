"""
# MeesaJarJar MeesaJarJar.com MeesaJarJar.shop Github.com/MeesaJarJar
Persistent SDXL Turbo server — loads model once, stays alive.
Accepts POST /generate with JSON: { "image": base64_png, "prompt": "text", "hex": "0x000E" }
Returns JSON: { "ok": true, "hex": "0x000E", "path": "full_path" }

Triggered automatically by the Razor Enhanced AutoReplace script in-game.
User must restart client fully to see replacement art in UOForever
"""

import argparse
import base64
import io
import json
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

import torch
from PIL import Image


MODEL_ID = "stabilityai/sdxl-turbo"
MODEL_PATHS = [
    os.path.join(os.path.dirname(__file__), "models", "sd_xl_turbo_1.0_fp16.safetensors"),
    os.path.join(os.path.dirname(__file__), "..", "Data", "AI", "models", "sd_xl_turbo_1.0_fp16.safetensors"),
    r"C:\Users\meesa\source\repos\ClassicUO-JAR\Data\AI\models\sd_xl_turbo_1.0_fp16.safetensors",
]
DEFAULT_OUTPUT_DIR = r"C:\Program Files (x86)\UOForever\UO\override\art"

# Generation defaults
STEPS = 17
CFG = 5.0
STRENGTH = 0.58
SIZE = 512

pipe = None
device = None


def remove_background(img, threshold=0.07):
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            avg = (r + g + b) / 3.0 / 255.0
            if avg < threshold:
                pixels[x, y] = (0, 0, 0, 0)
    return img


def load_model():
    global pipe, device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}", flush=True)

    local_model = None
    for candidate in MODEL_PATHS:
        p = Path(candidate).resolve()
        if p.exists():
            local_model = p
            break

    if local_model:
        print(f"Loading model from: {local_model}", flush=True)
        from diffusers import StableDiffusionXLImg2ImgPipeline
        pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(
            str(local_model),
            torch_dtype=torch.float16,
            variant="fp16",
        )
    else:
        print(f"No local model found, downloading from HuggingFace: {MODEL_ID}", flush=True)
        from diffusers import StableDiffusionXLImg2ImgPipeline
        pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            variant="fp16",
        )

    pipe = pipe.to(device)
    print("Model loaded and ready.", flush=True)


def generate(image_b64, prompt, hex_id, strength=STRENGTH, steps=STEPS, cfg=CFG, seed=0):
    # Decode input image
    img_bytes = base64.b64decode(image_b64)
    input_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    orig_w, orig_h = input_img.size

    # Resize to working resolution
    resized = input_img.resize((SIZE, SIZE), Image.BICUBIC)

    generator = torch.Generator(device=device).manual_seed(seed)

    t0 = time.time()
    result = pipe(
        prompt=prompt,
        image=resized,
        num_inference_steps=steps,
        guidance_scale=cfg,
        strength=strength,
        generator=generator,
    ).images[0]
    elapsed = time.time() - t0

    # Resize back to original
    result = result.resize((orig_w, orig_h), Image.BICUBIC)

    # Remove background
    result = remove_background(result)

    # Brighten visible near-black pixels so only transparent pixels are pure black
    px = result.load()
    w, h = result.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and r == 0 and g == 0 and b == 0:
                px[x, y] = (1, 1, 1, a)

    # Save
    out_dir = Path(DEFAULT_OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{hex_id}.png"
    result.save(str(out_path))

    print(f"  Generated {hex_id} in {elapsed:.1f}s", flush=True)
    return str(out_path.resolve())


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/generate":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            try:
                path = generate(
                    image_b64=body["image"],
                    prompt=body["prompt"],
                    hex_id=body["hex"],
                    strength=body.get("strength", STRENGTH),
                    steps=body.get("steps", STEPS),
                    cfg=body.get("cfg", CFG),
                    seed=body.get("seed", 0),
                )
                resp = {"ok": True, "hex": body["hex"], "path": path}
            except Exception as e:
                print(f"[ERROR] {body.get('hex', '?')}: {e}", flush=True)
                resp = {"ok": False, "error": str(e)}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "model": "sdxl-turbo"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Persistent SDXL Turbo server")
    parser.add_argument("--port", type=int, default=5555, help="Port (default: 5555)")
    args = parser.parse_args()

    load_model()

    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Server listening on http://127.0.0.1:{args.port}", flush=True)
    print("Endpoints: POST /generate, GET /health", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.", flush=True)
        server.server_close()


if __name__ == "__main__":
    main()
