import streamlit as st
from PIL import Image
from utils.resources import HekateData
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED


class Tools:
    def create_logo():
        try:
            img = st.file_uploader("Choose an image:", accept_multiple_files = False, type =[ "png", "jpg", "jpeg"], key = 1)

            if img:
                st.spinner(text = "Reformating image...")

                # Open the image
                image = Image.open(img)

                # Get the current dimensions
                current_width, current_height = image.size

                # Check if resizing is necessary
                if current_width > HekateData.logo_width or current_height > HekateData.logo_height:

                    # Resize the image
                    aspect_ratio = current_width / current_height
                    if aspect_ratio > (HekateData.logo_width / HekateData.logo_height):
                        new_width = HekateData.logo_width
                        new_height = int(HekateData.logo_width / aspect_ratio)
                    else:
                        new_height = HekateData.logo_height
                        new_width = int(HekateData.logo_height * aspect_ratio)

                    image = image.resize((new_width, new_height), Image.ANTIALIAS)

                # Check if rotation is necessary
                if image.size[0] == HekateData.logo_height and image.size[1] == HekateData.logo_width:

                    # Rotate the image counterclockwise by 90 degrees
                    image = image.transpose(Image.ROTATE_270)

                # Convert to 32-bit ARGB mode
                image = image.convert("RGBA")
                image_data = image.tobytes("raw", "RGBA")

                st.image(image, caption = "Bootlogo preview")

                # Save the resized and rotated image
                img_buffer = BytesIO()
                image.save(img_buffer, "BMP", transparency = 0, dpi = (300, 300))


                # Create zipfile with icon
                zip_buffer = BytesIO()
                with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                    zip_file.writestr(f"bootloader/res/bootlogo.bmp", img_buffer.getvalue())

                st.download_button("✅ Click here to download", zip_buffer, file_name = HekateData.file_name_logo, use_container_width = True, key = 7)

        except Exception:
            st.error(f"An error has occurred", icon = "🚨")
    
    def create_background():
        try:
            img = st.file_uploader("Choose an image:", accept_multiple_files = False, type =[ "png", "jpg", "jpeg"], key = 2)

            if img:
                st.spinner(text = "Reformating image...")

                # Open the image
                image = Image.open(img)

                # Check if resizing is necessary
                if image.size != (HekateData.background_width, HekateData.background_height):
                    # Resize the image
                    image = image.resize((HekateData.background_width, HekateData.background_height), Image.ANTIALIAS)

                # Convert to 32-color RGB mode
                image = image.convert("P", palette = Image.ADAPTIVE, colors = 32)

                st.image(image, caption = "Background preview")

                # Save the resized and converted image
                img_buffer = BytesIO()
                image.save(img_buffer, "BMP")

                # Create zipfile with icon
                zip_buffer = BytesIO()
                with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                    zip_file.writestr(f"bootloader/res/background.bmp", img_buffer.getvalue())

                st.download_button("✅ Click here to download", zip_buffer, file_name = HekateData.file_name_background, use_container_width = True, key = 8)

        except Exception:
            st.error(f"An error has occurred", icon = "🚨")

    
    def create_config():
        prompt = f"""
        ### Global Configuration keys/values:

        | Config option      | Description                                                |
        | ------------------ | ---------------------------------------------------------- |
        | autoboot=0         | 0: Disable, #: Boot entry number to auto boot.             |
        | autoboot_list=0    | 0: Read `autoboot` boot entry from hekate_ipl.ini, 1: Read from ini folder (ini files are ASCII ordered). |
        | bootwait=3         | 0: Disable (It also disables bootlogo. Having **VOL-** pressed since injection goes to menu.), #: Time to wait for **VOL-** to enter menu. Max: 20s. |
        | noticker=0         | 0: Animated line is drawn during custom bootlogo, signifying time left to skip to menu. 1: Disable. |
        | autohosoff=1       | 0: Disable, 1: If woke up from HOS via an RTC alarm, shows logo, then powers off completely, 2: No logo, immediately powers off.|
        | autonogc=1         | 0: Disable, 1: Automatically applies nogc patch if unburnt fuses found and a >= 4.0.0 HOS is booted. |
        | bootprotect=0      | 0: Disable, 1: Protect bootloader folder from being corrupted by disallowing reading or editing in HOS. |
        | updater2p=0        | 0: Disable, 1: Force updates (if needed) the reboot2payload binary to be hekate. |
        | backlight=100      | Screen backlight level. 0-255.                             |
        """
        
        st.write(prompt)

        autoboot = st.number_input("Enter autoboot value", min_value = 0, max_value = None, value = 0)
        autoboot_list = st.number_input("Enter autoboot list value", min_value = 0, max_value = None, value = 0)
        bootwait = st.number_input("Enter bootwait value", min_value = 0, max_value = 20, value = 3)
        noticker = st.number_input("Enter noticker value", min_value = 0, max_value = 1, value = 0)
        autohosoff = st.number_input("Enter autohosoff value", min_value = 0, max_value = 2, value = 1)
        autonogc = st.number_input("Enter autonogc value", min_value = 0, max_value = 1, value = 1)
        bootprotect = st.number_input("Enter bootprotect value", min_value = 0, max_value = 1, value = 0)
        updater2p = st.number_input("Enter updater2p value", min_value = 0, max_value = 1, value = 0)
        backlight = st.number_input("Enter autobacklightboot value", min_value = 0, max_value = 255, value = 100)

        if st.button("Submit", key = 3):

            # Preview config
            config = f"""\
[config]
autoboot={autoboot}
autoboot_list={autoboot_list}
bootwait={bootwait}
noticker={noticker}
verification=1
autohosoff={autohosoff}
autonogc={autonogc}
bootprotect={bootprotect}
updater2p={updater2p}
backlight={backlight}

;Switch Customizer
;Github: https://github.com/6A-Realm/Bootlogo-Generator

;--- Custom Firmware ---
[CFW (SYSNAND)]
emummc_force_disable=1
fss0=atmosphere/package3
atmosphere=1
logopath=bootloader/bootlogo.bmp
icon=bootloader/res/icon_payload.bmp
;

[CFW (EMUMMC)]
emummcforce=1
fss0=atmosphere/package3
atmosphere=1
logopath=bootloader/bootlogo.bmp
icon=bootloader/res/icon_payload.bmp
;

;--- Stock ---
[Stock (SYSNAND)]
emummc_force_disable=1
fss0=atmosphere/package3
stock=1
icon=bootloader/res/icon_switch.bmp
;
"""
            st.code(config, language = "ini")

            # Create zip file
            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                zip_file.writestr("bootloader/hekate_ipl.ini", str.encode(config, "utf-8"))
            st.download_button("✅ Click here to download", zip_buffer, file_name = "hekate_configs.zip", use_container_width = True, key = 9)
