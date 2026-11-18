"""Crystal Cavern (Scene 3) module for The Folded Lumen project.

Reads the p5.js project files from assets/crystal-cavern/ and renders
them inline in a Streamlit iframe via components.html().
"""

import base64
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

_ASSET_DIR = Path(__file__).resolve().parent / "assets" / "crystal-cavern"


def _read_text(filename):
    return (_ASSET_DIR / filename).read_text(encoding="utf-8")


def _read_b64(filename):
    raw = (_ASSET_DIR / filename).read_bytes()
    return base64.b64encode(raw).decode("ascii")


def _build_inline_html():
    """Read index.html and inline all CSS, JS, and image references."""
    html = _read_text("index.html")

    # --- Inline CSS ---
    css_match = re.search(r'<link[^>]+href="css/style\.css[^"]*"[^>]*>', html)
    if css_match:
        css_content = _read_text("css/style.css")
        html = html.replace(
            css_match.group(0),
            f"<style>\n{css_content}\n</style>",
        )

    # --- Inline JS files ---
    for js_file in [
        "js/p5.min.js",
        "js/config.js",
        "js/audio.js",
        "js/texture.js",
        "js/cavern.js",
        "js/sketch.js",
    ]:
        # Match <script src="js/...?v=N"></script>
        pattern = re.compile(
            r'<script[^>]+src="' + re.escape(js_file) + r'[^"]*"[^>]*>\s*</script>'
        )
        match = pattern.search(html)
        if match:
            js_content = _read_text(js_file)
            html = html.replace(
                match.group(0),
                f"<script>\n{js_content}\n</script>",
            )

    # --- Inline background image as base64 ---
    img_b64 = _read_b64("assets/background.jpg")
    img_match = re.search(
        r"loadImage\(['\"]assets/background\.jpg[^'\"]*['\"]", html
    )
    if img_match:
        html = html.replace(
            img_match.group(0),
            f'loadImage("data:image/jpeg;base64,{img_b64}"',
        )

    # Also handle any remaining references in JS code that reference the image path
    # (e.g., inside texture.js or sketch.js if they reference the path directly)
    html = html.replace(
        "assets/background.jpg?v=3",
        f"data:image/jpeg;base64,{img_b64}",
    )
    html = html.replace(
        "assets/background.jpg",
        f"data:image/jpeg;base64,{img_b64}",
    )

    return html


def render():
    """Display the Crystal Cavern module."""
    st.header("💎 Crystal Cavern (Scene 3)")
    st.write("**The Folded Lumen** — Activate the earth veins and the Origami Heart.")
    st.write(
        "Drag elements together to synthesize:\n"
        "- Rock + Rain → Raw Stone\n"
        "- Raw Stone + Sun → Luminous Crystal\n"
        "- Luminous Crystal + Wildflowers → Origami Heart"
    )

    try:
        html_content = _build_inline_html()
        components.html(html_content, height=680, scrolling=False)
    except Exception as e:
        st.error(f"Failed to load Crystal Cavern module: {e}")
        st.info(
            "You can also open the project directly from "
            "`modules/assets/crystal-cavern/index.html` in a browser."
        )
