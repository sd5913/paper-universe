
import streamlit as st

from modules import weather, living, secret, experience

st.set_page_config(
    page_title="Paper Universe",
    page_icon="🌸",
    layout="wide",
)

st.title("🌸 Paper Universe")
st.write("An interactive paper-cut collage world.")

st.sidebar.title("🌍 Explore Worlds")

world = st.sidebar.radio(
    "Choose a world:",
    [
        "Home",
        "Weather World",
        "Living World",
        "Secret World",
        "World Experience",
    ],
)

if world == "Home":
    st.header("Welcome to Paper Universe")
    st.write(
        "Explore different elements, discover hidden reactions, "
        "and create your own playful world."
    )

    st.info("Choose a world from the sidebar to begin.")

elif world == "Weather World":
    weather.render()

elif world == "Living World":
    living.render()

elif world == "Secret World":
    secret.render()

elif world == "World Experience":
    experience.render()
