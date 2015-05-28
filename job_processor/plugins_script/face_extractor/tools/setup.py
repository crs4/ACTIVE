from distutils.core import setup
import py2exe

setup(
    version = "0.1",
    description = "extraction of faces from given image",
    name = "extract faces from image",

    options = {
            "py2exe":{
            "dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe"],
        }
    },

    # targets to build
    console = ["call_extract_faces_from_image.py"],
    )
