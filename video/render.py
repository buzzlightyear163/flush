# renders video.html: one mp4 per scene from JPEG frames, then joins them
import pathlib, subprocess, os, json
from playwright.sync_api import sync_playwright
FPS = 30
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(pathlib.Path("video.html").resolve().as_uri()); pg.wait_for_selector("body[data-ready]")
    meta = pg.evaluate("META"); json.dump(meta, open("meta.json", "w"))
    files = []
    for i, ((name, L), st) in enumerate(zip(meta["SCENES"], meta["STARTS"])):
        n0, n1 = round(st * FPS), round((st + L) * FPS)
        tmp, out = f"s{i}_{name}.tmp.mp4", f"s{i}_{name}.mp4"
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
        for n in range(n0, n1):
            pg.evaluate(f"render({n / FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close()
        if ff.wait() == 0: os.replace(tmp, out); files.append(out); print("scene", i, name, n1 - n0, "frames")
        else: raise SystemExit("ffmpeg failed on " + name)
    b.close()
open("list.txt", "w").write("".join(f"file '{f}'\n" for f in files))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "video_noaudio.tmp.mp4"], check=True)
os.replace("video_noaudio.tmp.mp4", "video_noaudio.mp4"); print("errors", errs)
