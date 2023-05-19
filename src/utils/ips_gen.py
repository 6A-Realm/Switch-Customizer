import streamlit as st
from PIL import Image
from io import BytesIO
from utils.resources import BootlogoData
from ips import Patch
from zipfile import ZipFile, ZIP_DEFLATED

original_logo = open(r'assets/logo.txt', "rb")

class Generate:
    def bootlogo_ips():
        try:

            keep_ratio = st.checkbox("Keep image aspect ratio", value = False)

            # Choose an image prompt
            input = st.file_uploader("Choose an image:", accept_multiple_files = False, type =[ "png", "jpg", "jpeg"])

            if input is not None:
                st.spinner(text="Generating your IPS patches...")

                # Open Image
                new_logo = Image.open(BytesIO(input.read())).convert("RGBA")

                # Resize image if needed
                if keep_ratio:
                    width, height = new_logo.size
                    aspect_ratio = BootlogoData.base_width / BootlogoData.base_height
                    new_aspect_ratio = width / height

                    if new_aspect_ratio > aspect_ratio:
                        new_width = int(height * aspect_ratio)
                        new_logo = new_logo.resize((new_width, height), Image.LANCZOS)
                    elif new_aspect_ratio < aspect_ratio:
                        new_height = int(width / aspect_ratio)
                        new_logo = new_logo.resize((width, new_height), Image.LANCZOS)

                else:
                    new_logo = new_logo.resize((BootlogoData.base_width, BootlogoData.base_height), Image.LANCZOS)

                # Create background with transparency
                bg = Image.new("RGBA", (BootlogoData.base_width, BootlogoData.base_height), (0, 0, 0, 0))
                bg.paste(new_logo, ((BootlogoData.base_width - new_logo.width) // 2, (BootlogoData.base_height - new_logo.height) // 2))

                st.image(bg, caption="Logo preview")

                # Generate patches
                base_patch = Patch.create(original_logo, bg.tobytes())

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
                st.download_button("✅ Click here to download", zip_buffer, file_name=BootlogoData.file_name, use_container_width=True)

        except Exception:
            st.error("An error has occurred", icon = "🚨")
