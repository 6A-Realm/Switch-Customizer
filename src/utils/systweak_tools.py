import streamlit as st
from PIL import Image
from io import BytesIO
from utils.resources import SysTweakData
from zipfile import ZipFile, ZIP_DEFLATED


class Reformat:

    def icon():
        try:
            title_id = st.text_input("Enter the title ID: ")
            
            # 256x256 jpg image no bigger than 128K
            img = st.file_uploader("Choose an image:", accept_multiple_files = False, type =[ "png", "jpg", "jpeg"])

            if title_id and img:
                st.spinner(text = "Reformating image...")

                # Open Image
                open_f = Image.open(BytesIO(img.read()))

                # Resize image if needed
                if open_f.size != (SysTweakData.width_height, SysTweakData.width_height):
                        open_f = open_f.resize((SysTweakData.width_height, SysTweakData.width_height), Image.LANCZOS)

                st.image(open_f, caption = "Icon preview")

                img_buffer = BytesIO()
                open_f.save(img_buffer, "JPEG")

                # Create zipfile with icon
                zip_buffer = BytesIO()
                with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                    zip_file.writestr(f"atmosphere/contents/{title_id}/icon.jpg", img_buffer.getvalue())

                st.download_button("✅ Click here to download", zip_buffer, file_name = SysTweakData.file_name, use_container_width = True, key = 10)

        except Exception:
            st.error(f"An error has occurred", icon = "🚨")

    def title_info():
        try:
            # Get inputs
            title = st.text_input("Enter the title ID: ", key = 2)
            name = st.text_input("Enter the new title name: ")            
            author = st.text_input("Enter the new title author: ")
            display_version = st.text_input("Enter the new title display version: ")

            if title and name and author and display_version:
                if st.button("Submit", key = 4):

                    # Preview config.ini
                    config = f"[override_nacp]\nname={name}\nauthor={author}\ndisplay_version={display_version}"
                    st.code(config, language = "ini")

                    # Create zip file
                    zip_buffer = BytesIO()
                    with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                        zip_file.writestr(f"atmosphere/contents/{title}/config.ini", str.encode(config, "utf-8"))
                    st.download_button("✅ Click here to download", zip_buffer, file_name = SysTweakData.file_name_title, use_container_width = True, key = 11)

        except Exception:
            st.error(f"An error has occurred", icon = "🚨")
