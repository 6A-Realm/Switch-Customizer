from utils.create_background import Background
import streamlit as st
from utils.hekate_tools import Tools


Background.place()

# Basic HTML and also remove hamburger menu
st.markdown("<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style><center><h1> Generate Your Hekate Experience</h1>", unsafe_allow_html = True)
st.write('<p style="text-align: center;font-size:20px;" > <bold> Use the menu below to start customizing hekate. </bold><p><br>', unsafe_allow_html = True)

# Icon maker
with st.expander(":arrows_counterclockwise: Icon Converter"):
    Tools.create_logo()

# Background maker
with st.expander(":art: Hekate Background Maker"):
    Tools.create_background()

# Config.ini maker
with st.expander(":toolbox: Hekate Config.ini Toolbox"):
    # https://blog.streamlit.io/accessible-color-themes-for-streamlit-apps/
    Tools.create_config()
