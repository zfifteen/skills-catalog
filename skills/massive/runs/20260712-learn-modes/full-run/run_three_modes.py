#!/usr/bin/env python3
"""Full three-mode Grok PGS test: select mode → type → send → wait → harvest."""
from __future__ import annotations

import json
import re
import subprocess
import time
import base64
from pathlib import Path
from datetime import datetime, timezone

from Cocoa import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from Quartz import (
    CGEventCreateMouseEvent,
    CGEventPost,
    kCGHIDEventTap,
    kCGEventMouseMoved,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGMouseButtonLeft,
    CGEventSetIntegerValueField,
    kCGMouseEventClickState,
)

RUN = Path.home() / ".grok/skills/massive/runs/20260712-learn-modes/full-run"
MODES = ["Fast", "Expert", "Heavy"]
OCU = "open-computer-use"

FIND_MODEL = r'''
tell application "Safari" to activate
delay 0.25
tell application "System Events"
  tell process "Safari"
    set frontmost to true
    return my findModel(window 1, 0)
  end tell
end tell
on findModel(el, depth)
  if depth > 28 then return "DEEP"
  tell application "System Events"
    try
      if name of el is "Model select" then
        set p to position of el
        set s to size of el
        return "FOUND|" & (item 1 of p as text) & "," & (item 2 of p as text) & "," & (item 1 of s as text) & "," & (item 2 of s as text)
      end if
    end try
    try
      repeat with k in UI elements of el
        set r to my findModel(k, depth + 1)
        if r starts with "FOUND" then return r
      end repeat
    end try
  end tell
  return "NOTFOUND"
end findModel
'''

FIND_MENU = r'''
tell application "System Events"
  tell process "Safari"
    set out to {}
    my collectMenu(window 1, 0, out)
    set AppleScript's text item delimiters to linefeed
    return out as text
  end tell
end tell
on collectMenu(el, depth, out)
  if depth > 30 then return
  tell application "System Events"
    try
      if role of el is "AXMenuItem" then
        set t to name of el
        set p to position of el
        set s to size of el
        set w to item 1 of s
        if w > 400 then set w to 260
        set h to item 2 of s
        if h > 80 then set h to 50
        set cx to (item 1 of p) + (w / 2)
        set cy to (item 2 of p) + (h / 2)
        set firstName to paragraph 1 of t
        set end of out to firstName & "|" & (cx as text) & "|" & (cy as text)
      end if
    end try
    try
      repeat with k in UI elements of el
        my collectMenu(k, depth + 1, out)
      end repeat
    end try
  end tell
end collectMenu
'''

FIND_DONT_ALLOW = r'''
tell application "System Events"
  tell process "Safari"
    try
      if exists (button "Don’t Allow" of sheet 1 of window 1) then
        set b to button "Don’t Allow" of sheet 1 of window 1
        set p to position of b
        set s to size of b
        return "FOUND|" & ((item 1 of p) + (item 1 of s)/2 as text) & "," & ((item 2 of p) + (item 2 of s)/2 as text)
      end if
    end try
    try
      if exists (button "Don't Allow" of sheet 1 of window 1) then
        set b to button "Don't Allow" of sheet 1 of window 1
        set p to position of b
        set s to size of b
        return "FOUND|" & ((item 1 of p) + (item 1 of s)/2 as text) & "," & ((item 2 of p) + (item 2 of s)/2 as text)
      end if
    end try
  end tell
end tell
return "NONE"
'''


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(RUN / "run.log", "a") as f:
        f.write(line + "\n")


def activate_safari() -> None:
    apps = NSWorkspace.sharedWorkspace().runningApplications()
    safari = next(a for a in apps if a.bundleIdentifier() == "com.apple.Safari")
    safari.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    time.sleep(0.35)
    subprocess.run(["osascript", "-e", 'tell application "Safari" to activate'], check=False)
    time.sleep(0.25)


def se(script: str, timeout: float = 45) -> str:
    return subprocess.check_output(["osascript", "-e", script], text=True, timeout=timeout).strip()


def cursor_click(x: float, y: float, settle: float = 0.12) -> None:
    e = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, e)
    time.sleep(settle)
    e = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft)
    CGEventSetIntegerValueField(e, kCGMouseEventClickState, 1)
    CGEventPost(kCGHIDEventTap, e)
    time.sleep(0.05)
    e = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft)
    CGEventSetIntegerValueField(e, kCGMouseEventClickState, 1)
    CGEventPost(kCGHIDEventTap, e)


def ocu(tool: str, args: dict) -> dict:
    raw = subprocess.check_output(
        [OCU, "call", tool, "--args", json.dumps(args)],
        text=True,
        timeout=120,
    )
    return json.loads(raw)


def ocu_calls(calls: list, sleep: float = 0.8) -> list:
    raw = subprocess.check_output(
        [OCU, "call", "--calls", json.dumps(calls), "--sleep", str(sleep)],
        text=True,
        timeout=180,
    )
    return json.loads(raw)


def extract_state(raw_or_list) -> tuple[str, list[str]]:
    """Return (tree_text, list of image data urls/base64)."""
    if isinstance(raw_or_list, str):
        j = json.loads(raw_or_list)
    else:
        j = raw_or_list
    texts: list[str] = []
    imgs: list[str] = []

    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "text" and "text" in o:
                texts.append(o["text"])
            if o.get("type") == "image" and "data" in o:
                imgs.append(o["data"])
            # tool wrapper
            if "result" in o:
                walk(o["result"])
            if "content" in o:
                walk(o["content"])
            for k, v in o.items():
                if k not in ("result", "content", "text", "data"):
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(j)
    return "\n".join(texts), imgs


def save_shot(imgs: list[str], path: Path) -> None:
    if not imgs:
        return
    d = imgs[0]
    if d.startswith("data:"):
        d = d.split(",", 1)[1]
    path.write_bytes(base64.b64decode(d))


def get_app_state(text_limit="max", max_nodes=4000, max_depth=100) -> tuple[str, list[str]]:
    raw = ocu(
        "get_app_state",
        {
            "app": "Safari",
            "text_limit": text_limit,
            "max_tree_nodes": max_nodes,
            "max_tree_depth": max_depth,
        },
    )
    return extract_state(raw)


def dismiss_mic_if_any() -> bool:
    try:
        out = se(FIND_DONT_ALLOW, timeout=15)
    except Exception as e:
        log(f"  mic probe err: {e}")
        return False
    if out.startswith("FOUND|"):
        x, y = [float(v) for v in out.split("|", 1)[1].split(",")]
        log(f"  dismiss mic sheet at ({x:.0f},{y:.0f})")
        cursor_click(x, y)
        time.sleep(0.6)
        return True
    # also check OCU tree
    text, _ = get_app_state(text_limit=300, max_nodes=1500, max_depth=40)
    if "microphone" in text.lower() or "Don’t Allow" in text or "Don't Allow" in text:
        # try element click via index if present
        m = re.search(r"(?m)^\s*(\d+)\s+button.*Don.?t Allow", text)
        if m:
            idx = m.group(1)
            log(f"  OCU click Don't Allow idx={idx}")
            ocu("click", {"app": "Safari", "element_index": idx})
            time.sleep(0.6)
            return True
    return False


def nav_grok_home() -> bool:
    """Human-like: Meta+l, type grok.com, Return. Gate on URL."""
    activate_safari()
    dismiss_mic_if_any()
    log("  nav: Meta+l → grok.com → Return")
    ocu_calls(
        [
            {"tool": "press_key", "args": {"app": "Safari", "key": "Meta+l"}},
            {"tool": "type_text", "args": {"app": "Safari", "text": "https://grok.com"}},
            {"tool": "press_key", "args": {"app": "Safari", "key": "Return"}},
        ],
        sleep=0.6,
    )
    time.sleep(3.5)
    dismiss_mic_if_any()
    text, imgs = get_app_state(text_limit=500, max_nodes=2000)
    ok = "URL: https://grok.com" in text or "https://grok.com" in text
    ok = ok and "Ask Grok" in text and "Model select" in text
    log(f"  nav gate: {ok}")
    return ok


def model_geo():
    out = se(FIND_MODEL)
    if not out.startswith("FOUND|"):
        return None
    x, y, w, h = [float(v) for v in out.split("|", 1)[1].split(",")]
    return dict(x=x, y=y, w=w, h=h, cx=x + w / 2, cy=y + h / 2)


def menu_items() -> dict:
    out = se(FIND_MENU)
    items = {}
    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) >= 3:
            items[parts[0].strip()] = (float(parts[1]), float(parts[2]))
    return items


def select_mode(mode: str) -> dict:
    activate_safari()
    dismiss_mic_if_any()
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 53'], check=False)
    time.sleep(0.35)
    geo = model_geo()
    if not geo:
        return {"ok": False, "error": "Model select not found"}
    log(f"  open Model select @ ({geo['cx']:.0f},{geo['cy']:.0f}) w={geo['w']}")
    cursor_click(geo["cx"], geo["cy"])
    time.sleep(1.1)
    items = menu_items()
    log(f"  menu keys: {list(items.keys())}")
    if mode not in items:
        return {"ok": False, "error": f"{mode} missing from menu", "items": list(items.keys()), "geo": geo}
    mx, my = items[mode]
    log(f"  click {mode} @ ({mx:.0f},{my:.0f})")
    cursor_click(mx, my)
    time.sleep(1.0)
    items2 = menu_items()
    geo2 = model_geo()
    still = "Fast" in items2 and "Expert" in items2 and "Heavy" in items2
    ok = (not still) and geo2 is not None
    return {
        "ok": ok,
        "width_before": geo["w"],
        "width_after": geo2["w"] if geo2 else None,
        "menu_still": still,
        "geo_after": geo2,
    }


def focus_composer() -> bool:
    text, _ = get_app_state(text_limit=400, max_nodes=1500)
    m = re.search(r"(?m)^\s*(\d+)\s+text entry area.*Ask Grok", text)
    if not m:
        log("  composer not found in AX")
        return False
    idx = m.group(1)
    ocu("click", {"app": "Safari", "element_index": idx})
    time.sleep(0.4)
    return True


def type_prompt(prompt: str) -> dict:
    """Type prompt into focused composer. Prefer set_value if possible, else type_text chunks."""
    activate_safari()
    dismiss_mic_if_any()
    if not focus_composer():
        return {"ok": False, "error": "no composer"}

    # Clear any existing text: Meta+a then delete
    ocu_calls(
        [
            {"tool": "press_key", "args": {"app": "Safari", "key": "Meta+a"}},
            {"tool": "press_key", "args": {"app": "Safari", "key": "Backspace"}},
        ],
        sleep=0.25,
    )
    time.sleep(0.3)

    # set_value on text entry — more reliable for long text
    text, _ = get_app_state(text_limit=300, max_nodes=1200)
    m = re.search(r"(?m)^\s*(\d+)\s+text entry area.*Ask Grok", text)
    if not m:
        return {"ok": False, "error": "composer lost after clear"}
    idx = m.group(1)

    # Try set_value first
    try:
        ocu("set_value", {"app": "Safari", "element_index": idx, "value": prompt})
        time.sleep(0.6)
    except Exception as e:
        log(f"  set_value failed: {e}; falling back to type_text")
        # type in chunks of ~80 chars
        chunk = 100
        for i in range(0, len(prompt), chunk):
            ocu("type_text", {"app": "Safari", "text": prompt[i : i + chunk]})
            time.sleep(0.15)

    # Verify: get value from tree / text
    text2, imgs = get_app_state(text_limit="max", max_nodes=3000)
    # Sample first 40 chars of prompt should appear
    sample = prompt[:40]
    present = sample in text2 or prompt[:25] in text2
    # Sometimes AX value is truncated; also check if not still empty placeholder only
    log(f"  type verify sample present={present}")
    if not present:
        # fallback type_text full
        log("  retype via type_text")
        ocu("click", {"app": "Safari", "element_index": idx})
        time.sleep(0.2)
        ocu_calls(
            [
                {"tool": "press_key", "args": {"app": "Safari", "key": "Meta+a"}},
                {"tool": "press_key", "args": {"app": "Safari", "key": "Backspace"}},
            ],
            sleep=0.2,
        )
        # clipboard paste is more human for long text
        pb = subprocess.run(["pbcopy"], input=prompt, text=True, check=True)
        ocu("press_key", {"app": "Safari", "key": "Meta+v"})
        time.sleep(0.8)
        text2, imgs = get_app_state(text_limit="max", max_nodes=3000)
        present = sample in text2 or prompt[:25] in text2
        log(f"  paste verify present={present}")

    return {"ok": present, "verified": present}


def send_prompt() -> None:
    # Prefer Return in composer; grok often uses Enter to send
    ocu("press_key", {"app": "Safari", "key": "Return"})
    time.sleep(1.0)


def wait_done(mode: str, timeout_s: int = 300) -> dict:
    """Poll until not Generating / Stop button gone and response text present."""
    start = time.time()
    last_len = 0
    stable = 0
    while time.time() - start < timeout_s:
        text, imgs = get_app_state(text_limit="max", max_nodes=6000, max_depth=120)
        low = text.lower()
        generating = (
            "stop" in low
            and ("generating" in low or "thinking" in low)
            or "button Stop" in text
            or "Stop generating" in text
        )
        # Heuristic: substantial content after send
        body_markers = ["prime", "gap", "gwr", "tau", "nlsc", "divisor", "proved", "invalidat"]
        hits = sum(1 for m in body_markers if m in low)
        # length of HTML content text region
        content_len = len(text)
        if content_len == last_len and not generating and hits >= 2:
            stable += 1
        else:
            stable = 0
        last_len = content_len
        elapsed = int(time.time() - start)
        log(f"  wait {mode}: t={elapsed}s gen={generating} hits={hits} len={content_len} stable={stable}")
        if not generating and hits >= 3 and stable >= 2:
            save_shot(imgs, RUN / f"{mode.lower()}-done.png")
            (RUN / f"{mode.lower()}-tree.txt").write_text(text)
            return {"ok": True, "elapsed": elapsed, "text": text, "hits": hits}
        if not generating and hits >= 2 and elapsed > 25 and stable >= 3:
            save_shot(imgs, RUN / f"{mode.lower()}-done.png")
            (RUN / f"{mode.lower()}-tree.txt").write_text(text)
            return {"ok": True, "elapsed": elapsed, "text": text, "hits": hits}
        time.sleep(4.0)
    text, imgs = get_app_state(text_limit="max", max_nodes=6000)
    save_shot(imgs, RUN / f"{mode.lower()}-timeout.png")
    (RUN / f"{mode.lower()}-tree.txt").write_text(text)
    return {"ok": False, "error": "timeout", "text": text}


def harvest_response(tree_text: str) -> str:
    """Best-effort extract assistant response from AX tree / page text."""
    # Prefer AppleScript innerText for full body
    try:
        body = subprocess.check_output(
            [
                "osascript",
                "-e",
                '''
tell application "Safari"
  set theTab to current tab of front window
  tell theTab
    set t to do JavaScript "document.body.innerText"
  end tell
  return t
end tell
''',
            ],
            text=True,
            timeout=30,
        )
    except Exception as e:
        log(f"  innerText failed: {e}")
        body = tree_text

    # Trim common chrome
    lines = body.splitlines()
    # Drop empty leading, keep from first substantial block
    return body.strip()


def run_one(mode: str) -> dict:
    log(f"======== {mode} ========")
    result = {"mode": mode, "steps": [], "ok": False}
    prompt = (RUN / f"prompt-{mode.lower()}.txt").read_text().strip()
    result["prompt_len"] = len(prompt)

    # 1. Fresh home
    if not nav_grok_home():
        # retry once
        time.sleep(2)
        if not nav_grok_home():
            result["error"] = "nav failed"
            return result
    result["steps"].append({"nav": True})

    # 2. Select mode
    sel = select_mode(mode)
    result["select"] = sel
    result["steps"].append({"select_mode": sel.get("ok")})
    if not sel.get("ok"):
        result["error"] = f"select failed: {sel}"
        return result
    text, imgs = get_app_state(text_limit=400, max_nodes=1500)
    save_shot(imgs, RUN / f"{mode.lower()}-mode.png")

    # 3. Type
    typed = type_prompt(prompt)
    result["type"] = typed
    result["steps"].append({"type": typed.get("ok")})
    if not typed.get("ok"):
        result["error"] = "type verify failed"
        # still try send? no — hard gate
        return result

    # 4. Send
    log("  send Return")
    send_prompt()
    result["steps"].append({"send": True})

    # 5. Wait
    wait = wait_done(mode, timeout_s=360 if mode == "Heavy" else 240)
    result["wait"] = {"ok": wait.get("ok"), "elapsed": wait.get("elapsed"), "hits": wait.get("hits")}
    result["steps"].append({"wait": wait.get("ok")})

    # 6. Harvest
    body = harvest_response(wait.get("text", ""))
    out_path = RUN / f"{mode.lower()}-response.txt"
    out_path.write_text(body)
    result["response_path"] = str(out_path)
    result["response_chars"] = len(body)
    # word count rough
    words = len(re.findall(r"\b\w+\b", body))
    result["response_words"] = words
    result["ok"] = bool(wait.get("ok") and len(body) > 200)
    log(f"  harvested {len(body)} chars ~{words} words ok={result['ok']}")
    return result


def main():
    (RUN / "run.log").write_text(f"start {datetime.now(timezone.utc).isoformat()}\n")
    all_results = {}
    for mode in MODES:
        try:
            all_results[mode] = run_one(mode)
        except Exception as e:
            log(f"EXCEPTION {mode}: {e}")
            all_results[mode] = {"mode": mode, "ok": False, "error": str(e)}
        time.sleep(1.5)

    final = "PASS" if all(r.get("ok") for r in all_results.values()) else "FAIL"
    summary = {
        "final": final,
        "modes": all_results,
        "finished": datetime.now(timezone.utc).isoformat(),
    }
    (RUN / "result.json").write_text(json.dumps(summary, indent=2, default=str))
    log(f"FINAL {final}")
    for m, r in all_results.items():
        log(f"  {m}: ok={r.get('ok')} err={r.get('error')} words={r.get('response_words')} steps={r.get('steps')}")


if __name__ == "__main__":
    main()
