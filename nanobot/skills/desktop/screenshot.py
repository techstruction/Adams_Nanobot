"""
screenshot.py — Capture macOS desktop screenshots.

Usage:
    python3 screenshot.py [output_path]
    python3 screenshot.py --base64

Requires: Screen Recording permission for Terminal in
    System Settings → Privacy & Security → Screen & System Audio Recording
"""

import sys
import base64
import io
from pathlib import Path
from datetime import datetime


def take_screenshot(output_path: str | None = None, region: dict | None = None) -> dict:
    """
    Capture a screenshot of the full screen or a region.

    Args:
        output_path: Where to save the PNG. If None, saves to ~/.nanobot/workspace/screenshots/.
        region: Optional dict with keys: top, left, width, height (pixels).

    Returns:
        dict with keys: path, width, height, base64 (PNG encoded)
    """
    try:
        import mss
        import mss.tools
    except ImportError:
        return {"error": "mss not installed. Run: uv pip install mss"}

    # Default save location
    if output_path is None:
        save_dir = Path.home() / ".nanobot" / "workspace" / "screenshots"
        save_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = str(save_dir / f"screenshot_{timestamp}.png")

    with mss.mss() as sct:
        monitor = region if region else sct.monitors[0]  # monitors[0] = all screens combined
        img = sct.grab(monitor)

        # Save to file
        mss.tools.to_png(img.rgb, img.size, output=output_path)

        # Also encode as base64 for agent use
        png_bytes = mss.tools.to_png(img.rgb, img.size)
        b64 = base64.b64encode(png_bytes).decode("utf-8")

    return {
        "path": output_path,
        "width": img.size[0],
        "height": img.size[1],
        "base64": b64,
    }


def screenshot_region(top: int, left: int, width: int, height: int, output_path: str | None = None) -> dict:
    """Capture a specific region of the screen."""
    return take_screenshot(output_path=output_path, region={"top": top, "left": left, "width": width, "height": height})


if __name__ == "__main__":
    if "--base64" in sys.argv:
        result = take_screenshot()
        if "error" in result:
            print(result["error"])
        else:
            print(f"Saved: {result['path']} ({result['width']}x{result['height']})")
            print(f"Base64 length: {len(result['base64'])} chars")
    else:
        path = sys.argv[1] if len(sys.argv) > 1 else None
        result = take_screenshot(output_path=path)
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        print(f"Screenshot saved: {result['path']} ({result['width']}x{result['height']})")
