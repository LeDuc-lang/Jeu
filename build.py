import os
import shutil

from pyxel.cli import *
from pyxel.cli import _complete_extension, _check_file_exists, _check_dir_exists, _check_file_under_dir, _files_in_dir


def _make_metadata_comment(startup_script_file):
    METADATA_FIELDS = ["title", "author", "desc", "site", "license", "version"]
    metadata = {}
    metadata_pattern = re.compile(r"#\s*(.+?)\s*:\s*(.+)")
    with open(startup_script_file, "r", encoding="utf8") as f:
        for line in f:
            match = metadata_pattern.match(line)
            if match:
                key, value = match.groups()
                key = key.strip().lower()
                if key in METADATA_FIELDS:
                    metadata[key] = value.strip()
    if not metadata:
        return ""
    metadata_comment = ""
    max_key_len = max(len(key) for key in metadata)
    max_value_len = max(len(value) for _, value in metadata.items())
    border = "-" * min((max_key_len + max_value_len + 3), 80)
    metadata_comment = border + "\n"
    for key in METADATA_FIELDS:
        if key in metadata:
            value = metadata[key]
            metadata_comment += f"{key.ljust(max_key_len)} : {value}\n"
    metadata_comment += border
    return metadata_comment

def create_html_from_pyxel_app(pyxel_app_file):
    pyxel_app_file = _complete_extension(
        pyxel_app_file, "app2html", pyxel.APP_FILE_EXTENSION
    )
    _check_file_exists(pyxel_app_file)
    base64_string = ""
    with open(pyxel_app_file, "rb") as f:
        base64_string = base64.b64encode(f.read()).decode()
    pyxel_app_name = os.path.splitext(os.path.basename(pyxel_app_file))[0]
    with open(f'builds/{pyxel_app_name}.html', "w") as f:
        f.write(
            "<!DOCTYPE html>\n"
            '<script src="https://cdn.jsdelivr.net/gh/kitao/pyxel/wasm/pyxel.js">'
            "</script>\n"
            "<script>\n"
            f'launchPyxel({{ command: "play", name: "{pyxel_app_name}{pyxel.APP_FILE_EXTENSION}", '
            f'gamepad: "enabled", packages: "numpy", base64: "{base64_string}" }});\n'
            "</script>\n"
        )
    print(f'pyxel app "{pyxel_app_name}" created.\n pyxel app file: "{pyxel_app_file}"')


package_pyxel_app(os.curdir, "main.py")
shutil.move(os.curdir + "/NDC 2024.pyxapp", os.curdir + "/builds/NDC 2024.pyxapp")
create_html_from_pyxel_app(os.curdir + '/builds/NDC 2024.pyxapp')
