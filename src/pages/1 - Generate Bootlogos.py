from utils.contributors import Contributors
from utils.create_background import Background
import streamlit as st
from utils.ips_gen import Generate


# Pull contributors
contributors = Contributors.pull()


Background.place()

# Basic HTML and also remove hamburger menu
st.markdown("<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style><center><h1> Generate Custom Boot Logos</h1>", unsafe_allow_html = True)
st.write('<p style="text-align: center;font-size:20px;" > <bold> Generate custom IPS patches for your modded CFW Nintendo Switch. </bold><p><br>', unsafe_allow_html = True)


# Create boot logo ips patches expander
with st.expander(":camera: Generate Boot Logo"):

    # Choose an image prompt
    input = st.file_uploader("Choose an image:", accept_multiple_files = False, type =[ "png", "jpg", "jpeg"])

    if input is not None:
        Generate.bootlogo_ips(input)

# How to use expander
with st.expander(":information_source: How To Use"):
    st.write("This project uses Python to create IPS patches for a desired image for your CFW Nintendo Switch. Only PNG and JPG images are curently supported. Choose your desired image then click the prompted button to download a zip file of your patches. The files are already sorted for you, all you have to do is exact the zip file and drag and drop the atmosphere folder into the root of your SD card. Then you are done, happy generating!")

# Credits expander
with st.expander(":sparkles: Notible Contributors"):
    st.write(contributors)

