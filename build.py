import base64
import os
import zipfile

import pyxel
from pyxel.cli import _complete_extension, _check_file_exists, _check_dir_exists, _check_file_under_dir, \
    _files_in_dir

EXCLUDED_FILES = {"README.md", "build.py", "requirements.txt"}
EXCLUDED_DIRS = {"__pycache__", "builds", ".git", ".idea"}

dependencies = ["numpy", "matplotlib", "scipy"]

packages_str = f'"{','.join(dependencies)}"'


# app_name = "space_settler"

def package_pyxel_app(app_dir, startup_script_file):
    """Génère un pyxel package"""
    startup_script_file = _complete_extension(startup_script_file, "package", ".py")
    _check_dir_exists(app_dir)
    _check_file_exists(startup_script_file)
    _check_file_under_dir(startup_script_file, app_dir)

    app_dir = os.path.abspath(app_dir)
    setting_file = os.path.join(app_dir, pyxel.APP_STARTUP_SCRIPT_FILE)
    with open(setting_file, "w") as f:
        f.write(os.path.relpath(startup_script_file, app_dir))
    pyxel_app_file = os.path.basename(app_dir) + pyxel.APP_FILE_EXTENSION
    app_parent_dir = os.path.dirname(app_dir)
    with zipfile.ZipFile(
            f'builds/{pyxel_app_file}',
            "w",
            compression=zipfile.ZIP_DEFLATED,
    ) as zf:
        files = [setting_file] + _files_in_dir(app_dir)
        for file_path in files:
            if os.path.basename(file_path) == pyxel_app_file or any(file_name in file_path for file_name in EXCLUDED_FILES) or any(
                    dir_name in file_path for dir_name in EXCLUDED_DIRS):
                continue
            arcname = os.path.relpath(file_path, app_parent_dir)
            zf.write(file_path, arcname)
            print(f"added '{arcname}'")
    os.remove(setting_file)

    return f'builds/{pyxel_app_file}'


def create_html_from_pyxel_app(pyxel_app_file, output_dir="builds"):
    """Génère un fichier HTML qui exécute le jeu Pyxel dans WASM."""
    pyxel_app_file = _complete_extension(pyxel_app_file, "app2html", pyxel.APP_FILE_EXTENSION)

    if not os.path.exists(pyxel_app_file):
        raise FileNotFoundError(f"🚨 ERREUR: Le fichier '{pyxel_app_file}' n'existe pas !")

    with open(pyxel_app_file, "rb") as f:
        base64_string = base64.b64encode(f.read()).decode()

    pyxel_app_name = os.path.splitext(os.path.basename(pyxel_app_file))[0]

    os.makedirs(output_dir, exist_ok=True)

    html_file = os.path.join(output_dir, f"{pyxel_app_name}.html")

    with open(html_file, "w") as f:
        f.write(
            "<!DOCTYPE html>\n"
            '<script src="https://cdn.jsdelivr.net/gh/kitao/pyxel/wasm/pyxel.js"></script>\n'
            "<script>\n"
            f'launchPyxel({{ command: "play", name: "{pyxel_app_name}{pyxel.APP_FILE_EXTENSION}", '
            f'gamepad: "enabled", packages: {packages_str}, base64: "{base64_string}" }});\n'
            "</script>\n"
        )

    print(f'✅ HTML généré: {html_file}')


# Avex les methodes par défaut
# package_pyxel_app(os.curdir, "main.py")
# create_html_from_pyxel_app(os.curdir+"/spacesettler clone.pyxapp")

# Exécution du script
pyxapp_path = package_pyxel_app(os.curdir, "main.py")
print(pyxapp_path)
create_html_from_pyxel_app(pyxapp_path, "builds")
