import streamlit as st
from PIL import Image
from io import BytesIO
from utils.resources import BootlogoData
from ips import Patch
from zipfile import ZipFile, ZIP_DEFLATED


original_logo = open(r'assets/logo.txt', "rb")

class Generate:

    def bootlogo_ips(input):
        try:

            st.spinner(text = "Generating your IPS patches...")

            # Open Image
            new_logo = Image.open(BytesIO(input.read())).convert("RGBA")

            # Resize image if needed
            if new_logo.size != (BootlogoData.base_width, BootlogoData.base_height):
                new_logo = new_logo.resize((BootlogoData.base_width, BootlogoData.base_height), Image.LANCZOS)

            st.image(new_logo, caption = "Logo preview")

            # Generate patches
            base_patch = Patch.create(original_logo, new_logo.tobytes())

            # Create zipfile with patches
            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                for build_id, offset in BootlogoData.patch_info.items():
                    tmp_patch = Patch()
                    for r in base_patch.records:
                        tmp_patch.add_record(r.offset + offset, r.content, r.rle_size)
                        
                    # Filepath
                    zip_file.writestr(f"atmosphere/exefs_patches/bootlogo/{build_id}.ips", bytes(tmp_patch))

            # Prompt download button
            st.download_button("✅ Click here to download", zip_buffer, file_name = BootlogoData.file_name, use_container_width = True)

        except Exception:
            st.error(f"An error has occurred", icon = "🚨")
