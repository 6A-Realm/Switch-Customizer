from utils.create_background import Background
import streamlit as st
from utils.systweak_tools import Reformat


Background.place()

# Basic HTML and also remove hamburger menu
st.markdown("<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style><center><h1> Generate Custom Sys-Tweak Files</h1>", unsafe_allow_html = True)
st.write('<p style="text-align: center;font-size:20px;" > <bold> Create config.ini files and icons to use with sys-tweak. </bold><p><br>', unsafe_allow_html = True)


# Icon reformatter
with st.expander(":desktop_computer: Icon Maker"):
    Reformat.icon()

# Title info reformatter
with st.expander(":pencil2: Editing Title Info"):
    Reformat.title_info()

# IconGrabber
with st.expander(":hammer: IconGrabber for Sys-Tweak (recommended)"):
    st.write("A useful homebrew sysmodule for your Nintendo Switch is [IconGrabber](https://github.com/Slluxx/IconGrabber) by [Slluxx](https://github.com/Slluxx). With IconGrabber, you can search for games and then preview and download icons that you want. You can then use sys-tweak to change your downloaded game icons.\n - Note: An API key from steamgriddb.com is required.\n - Guide: [How to use IconGrabber](https://sodasoba1.github.io/icongrabber/) by [sodasoba1](https://github.com/sodasoba1).")
