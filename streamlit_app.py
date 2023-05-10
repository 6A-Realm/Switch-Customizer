from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import streamlit as st
from PIL import Image
from ips import Patch


# File name
file_name = "boot-logo.zip"

# Image ratios
base_width = 308
base_height = 350

# Build Id: offset
patch_info = {
    # AM patches
    "C79F22F18169FCD3B3698A881394F6240385CDB1": 1668164,
    "01890C643E9D6E17B2CDA77A9749ECB9A4F676D6": 1962240,
    "C088ADC91417EBAE6ADBDF3E47946858CAFE1A82": 1962240,
    "3EC573CB22744A993DFE281701E9CBFE66C03ABD": 1716480,

    # Vi patches
    "7B4123290DE2A6F52DE4AB72BEA1A83D11214C71": 1831168,
    "723DF02F6955D903DF7134105A16D48F06012DB1": 1835264,
    "967F4C3DFC7B165E4F7981373EC1798ACA234A45": 1573120,
    "98446A07BC664573F1578F3745C928D05AB73349": 1589504,
    "0767302E1881700608344A3859BC57013150A375": 1593600,
    "7C5894688EDA24907BC9CE7013630F365B366E4A": 1593600,
    "7421EC6021AC73DD60A635BC2B3AD6FCAE2A6481": 1536256,
    "96529C3226BEE906EE651754C33FE3E24ECAE832": 1544448,
    "D689E9FAE7CAA4EC30B0CD9B419779F73ED3F88B": 1655040,
    "65A23B52FCF971400CAA4198656D73867D7F1F1D": 1655040,
    "B295D3A8F8ACF88CB0C5CE7C0488CC5511B9C389": 1696000,
    "82EE58BEAB54C1A9D4B3D9ED414E84E31502FAC6": 1708288,
    "AFEAACF3E88AB539574689D1458060657E81E088": 1716480,
    "7E9BB552AAEFF82363D1E8C97B5C6B95E3989E1A": 1704192,
    "BA15B407573B8CECF0FAE2B367D3103A2A1E821C": 2191616,
}

# Choose an image prompt
input = st.file_uploader("Choose an image:", accept_multiple_files=False, type=["png", "jpg", "jpeg"])

if input is not None:

    # Open Image
    open_f = Image.open(BytesIO(input.read())).convert("RGBA")

    # Resize image if needed
    if open_f.size != (base_width, base_height):
        open_f = open_f.resize((base_width, base_height), Image.LANCZOS)

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
        tmp_p = Patch()
        for r in base_patch.records:
            tmp_p.add_record(r.offset + offset, r.content, r.rle_size)
        zip_file.writestr(f"{build_id}.ips", bytes(tmp_p))

    # Prompt download button
    st.download_button("Click here to download", zip_buffer, file_name = file_name)