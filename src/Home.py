import streamlit as st
from utils.create_background import Background


def main():
    """Home page for Nintendo Switch Customizer"""

    # Configure default settings for the page
    st.set_page_config(
        page_title = "Nintendo Switch Customizer",
        page_icon = "🎮",
        layout = "wide",
        # Hide the sidebar on mobile-sized devices
        initial_sidebar_state = "auto"
    )

    Background.place()

    # Basic HTML and also remove hamburger menu
    st.markdown("<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style><center><h1> Nintendo Switch Customizer </h1>", unsafe_allow_html = True)
    st.write('<p style="text-align: center;font-size:20px;" > <bold> This web app is meant to give some customizability and individuality to your CFW Nintendo Swtch. </bold><p><br>', unsafe_allow_html = True)
    st.write('<p style="text-align: center;font-size:20px;" > <bold> Use the sidebar to jump between functions. </bold><p><br>', unsafe_allow_html = True)

    # Capabilites expander
    with st.expander(":muscle: Capabilites", expanded = True):
        st.write("This web app has the power to generate:\n - Custom IPS patches for custom bootlogos\n - Custom [hekate](https://github.com/CTCaer/hekate) image resources and configs files\n - Config.ini files for [sys-tweak](https://github.com/p-sam/switch-sys-tweak)")

    # Contribute
    with st.expander(":thinking_face: Contribute", expanded = True):
        st.write("This is an open source project and you are more than welcome to contribute. Feel free to create [issues](https://github.com/6A-Realm/Bootlogo-Generator/issues), [pull requests](https://github.com/6A-Realm/Bootlogo-Generator/pulls), or view the [source code](https://github.com/6A-Realm/Bootlogo-Generator).")

if __name__ == "__main__":
    main()
