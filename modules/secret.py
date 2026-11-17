"""Secret World module — Paper Universe Module C.

Embeds a self-contained p5.js interactive experience via Streamlit components.
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

HTML_PATH = Path(__file__).resolve().parent / "assets" / "secret" / "secret-world.html"


def render():
    """Display the Secret World interactive module."""
    st.header("Secret World")
    st.write(
        "Explore a surreal paper-cut world with four hidden elements, "
        "three combination reactions, and a secret mandala."
    )
    st.caption(
        "Click elements to discover them. Drag the crystal, rotate the compass, "
        "and experiment with combinations. "
        "Press **J** for the secret star map, **H** for help, **R** to reset."
    )

    html_content = HTML_PATH.read_text(encoding="utf-8")
    components.html(html_content, height=680, scrolling=False)
