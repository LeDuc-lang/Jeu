import base64
import os
import zipfile

import pyxel
from pyxel.cli import _complete_extension, _check_file_exists, _check_dir_exists, _check_file_under_dir

EXCLUDED_FILES = {"README.md", "build.py", "requirements.txt"}
EXCLUDED_DIRS = {"__pycache__", "builds", ".git", ".idea"}


def package_pyxel_app(app_name, app_dir, startup_script_file, output_dir="builds"):
    """Génère un fichier .pyxapp contenant tout le projet, en excluant seulement les fichiers inutiles."""
    startup_script_file = _complete_extension(startup_script_file, "package", ".py")
    _check_dir_exists(app_dir)
    _check_file_exists(startup_script_file)
    _check_file_under_dir(startup_script_file, app_dir)

    # Vérifier et créer le dossier de sortie
    os.makedirs(output_dir, exist_ok=True)

    app_dir = os.path.abspath(app_dir)
    pyxel_app_file = os.path.join(output_dir, f"{app_name}{pyxel.APP_FILE_EXTENSION}")

    with zipfile.ZipFile(pyxel_app_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(app_dir):
            # Exclure les dossiers inutiles
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

            for file in files:
                if file in EXCLUDED_FILES or file.endswith(".pyc"):
                    continue  # On ignore ces fichiers

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, app_dir)  # Chemin relatif pour éviter d'écraser tout

                zf.write(file_path, arcname)
                print(f"✅ Ajouté au zip: '{arcname}'")

    print(f'✅ Fichier Pyxel packagé: {pyxel_app_file}')
    return pyxel_app_file  # Retourne le chemin du fichier généré


def create_html_from_pyxel_app(pyxel_app_file, output_dir="builds"):
    """Génère un fichier HTML qui exécute le jeu Pyxel dans WASM."""
    pyxel_app_file = _complete_extension(pyxel_app_file, "app2html", pyxel.APP_FILE_EXTENSION)

    if not os.path.exists(pyxel_app_file):
        raise FileNotFoundError(f"🚨 ERREUR: Le fichier '{pyxel_app_file}' n'existe pas !")

    with open(pyxel_app_file, "rb") as f:
        base64_string = base64.b64encode(f.read()).decode()

    pyxel_app_name = os.path.splitext(os.path.basename(pyxel_app_file))[0]

    os.makedirs(output_dir, exist_ok=True)

    dependencies = ["numpy", "matplotlib", "scipy"]
    packages_str = ",".join(dependencies)

    html_file = os.path.join(output_dir, f"{pyxel_app_name}.html")

    with open(html_file, "w") as f:
        f.write(
            "<!DOCTYPE html>\n"
            '<script src="https://cdn.jsdelivr.net/gh/kitao/pyxel/wasm/pyxel.js"></script>\n'
            "<script>\n"
            f'launchPyxel({{ command: "play", name: "{pyxel_app_name}{pyxel.APP_FILE_EXTENSION}", '
            f'gamepad: "enabled", packages: "{packages_str}", base64: "{base64_string}" }});\n'
            "</script>\n"
        )

    print(f'✅ HTML généré: {html_file}')


# Exécution du script
app_name = "space_settler"
pyxapp_path = package_pyxel_app(app_name, os.curdir, "main.py", "builds")
create_html_from_pyxel_app(pyxapp_path, "builds")
