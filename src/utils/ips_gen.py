from utils.resources import *
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import streamlit as st
from PIL import Image
from ips import Patch


class Generate:
    def bootlogo_ips(input):
        try:

            st.spinner(text = "Generating your IPS patches...")

            # Open Image
            open_f = Image.open(BytesIO(input.read())).convert("RGBA")

            # Resize image if needed
            if open_f.size != (base_width, base_height):
                open_f = open_f.resize((base_width, base_height), Image.LANCZOS)

            print(open_f.size)

            # Generate patches
            new_f = BytesIO(open_f.tobytes())
            new_f.seek(0, 2)
            new_len = new_f.tell()
            new_f.seek(0)

            base_patch = Patch()
            while new_f.tell() < new_len:
                base_patch.add_record(new_f.tell(), new_f.read(0xFFFF))

            # Create zipfile with patches
            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                for build_id, offset in patch_info.items():
                    tmp_patch = Patch()
                    for r in base_patch.records:
                        tmp_patch.add_record(r.offset + offset, r.content, r.rle_size)
                    zip_file.writestr(f"atmosphere/exefs_patches/bootlogo{build_id}.ips", bytes(tmp_patch))

            # Prompt download button
            st.download_button("✅ Click here to download", zip_buffer, file_name = file_name)

        except Exception as e:
            st.error("An error has occurred", icon = "🚨")
            print(e)
