#!/usr/bin/env python3
"""Locate Model select / Expert via Accessibility frames."""
import time
import re
from pathlib import Path
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCopyAttributeValue,
    kAXValueCGPointType,
    kAXValueCGSizeType,
    AXValueGetValue,
)
import Quartz
from Quartz import CGPoint, CGSize
from PIL import Image
import numpy as np

def ax_get(el, attr):
    err, val = AXUIElementCopyAttributeValue(el, attr, None)
    return val if err == 0 else None

def get_point(el):
    pos = ax_get(el, "AXPosition")
    if pos is None:
        return None
    try:
        return (float(pos.x), float(pos.y))
    except Exception:
        pass
    s = str(pos)
    m = re.search(r"([0-9.]+).*,\s*([0-9.]+)", s)
    if m:
        return (float(m.group(1)), float(m.group(2)))
    return None

def get_size(el):
    size = ax_get(el, "AXSize")
    if size is None:
        return None
    try:
        return (float(size.width), float(size.height))
    except Exception:
        pass
    s = str(size)
    m = re.search(r"([0-9.]+).*,\s*([0-9.]+)", s)
    if m:
        return (float(m.group(1)), float(m.group(2)))
    return None

def main():
    apps = NSWorkspace.sharedWorkspace().runningApplications()
    safari = next((a for a in apps if a.bundleIdentifier() == "com.apple.Safari"), None)
    if not safari:
        raise SystemExit("Safari not running")
    safari.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    time.sleep(0.5)
    pid = safari.processIdentifier()
    app_el = AXUIElementCreateApplication(pid)
    windows = ax_get(app_el, "AXWindows") or []
    print(f"Safari pid={pid} windows={len(windows)}")

    hits = []
    popups = []

    def walk(el, depth=0):
        if depth > 45:
            return
        role = ax_get(el, "AXRole") or ""
        title = ax_get(el, "AXTitle") or ""
        desc = ax_get(el, "AXDescription") or ""
        value = ax_get(el, "AXValue")
        val_s = ""
        if value is not None:
            val_s = value if isinstance(value, str) else str(value)[:80]
        pos = get_point(el)
        size = get_size(el)
        blob = f"{role}|{title}|{desc}|{val_s}".lower()
        keys = ("model", "expert", "fast", "heavy", "menu", "sheet", "microphone", "dictation", "popup", "pop up")
        if any(k in blob for k in keys):
            hits.append(dict(depth=depth, role=role, title=title, desc=desc, value=val_s[:80], pos=pos, size=size))
        if "Button" in role or "PopUp" in role or "Menu" in role:
            if pos and size and 100 < pos[1] < 1000:
                popups.append((role, title or desc or val_s, pos, size))
        for c in (ax_get(el, "AXChildren") or []):
            walk(c, depth + 1)

    for w in windows:
        wtitle = ax_get(w, "AXTitle")
        print(f"Window title={wtitle!r} pos={get_point(w)} size={get_size(w)}")
        walk(w)

    print(f"\nInteresting hits ({len(hits)}):")
    for h in hits:
        print(f"  d={h['depth']} role={h['role']!r} title={h['title']!r} desc={h['desc']!r} val={h['value']!r}")
        print(f"      pos={h['pos']} size={h['size']}")
        if h["pos"] and h["size"] and not isinstance(h["pos"][0], str):
            cx = h["pos"][0] + h["size"][0] / 2
            cy = h["pos"][1] + h["size"][1] / 2
            print(f"      CENTER=({cx:.1f},{cy:.1f})")

    print(f"\nButtons/popups mid-window ({len(popups)}):")
    for p in popups:
        role, name, pos, size = p
        cx = pos[0] + size[0] / 2
        cy = pos[1] + size[1] / 2
        print(f"  {role!r} name={name!r} pos={pos} size={size} center=({cx:.1f},{cy:.1f})")

    # Image content analysis for Expert label
    shot = Path(__file__).parent / "00-shot-0.png"
    if shot.exists():
        im = Image.open(shot).convert("RGB")
        arr = np.array(im)
        h, w = arr.shape[:2]
        print(f"\nScreenshot {w}x{h}")
        # find non-dark rows in mid band
        gray = arr.mean(axis=2)
        for y0, y1 in [(int(h * 0.38), int(h * 0.52)), (int(h * 0.42), int(h * 0.50))]:
            band = gray[y0:y1, :]
            cols = (band > 50).sum(axis=0)
            xs = np.where(cols > 1)[0]
            if len(xs):
                print(f"  y={y0}-{y1} content x={xs.min()}-{xs.max()}")
                # right third of content may be Expert
                mid = (xs.min() + xs.max()) // 2
                right = xs[xs > mid]
                if len(right):
                    print(f"    right of mid: x={right.min()}-{right.max()}")
                    # find Expert-ish cluster (smaller blob near right of pill)
                    # row mean brightness per x
                    row_mean = band.mean(axis=0)
                    # peaks near right
                    for thr in [80, 100, 120]:
                        bright_xs = np.where(row_mean > thr)[0]
                        bright_xs = bright_xs[bright_xs > w * 0.5]
                        if len(bright_xs):
                            print(f"    thr={thr} bright x in right half: {bright_xs.min()}-{bright_xs.max()} n={len(bright_xs)}")

if __name__ == "__main__":
    main()
