import streamlit as st
from modules import weather, living, secret, experience

st.set_page_config(
    page_title="Paper Universe",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
header[data-testid="stHeader"], [data-testid="stToolbar"], section[data-testid="stSidebar"] {
    display: none !important;
}
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100vw !important;
}
iframe {
    width: 100vw !important;
    height: 100vh !important;
    border: none !important;
    display: block !important;
}
</style>
""", unsafe_allow_html=True)

living.render()