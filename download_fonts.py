"""Descarga las fuentes Google Fonts necesarias para el proyecto."""

import urllib.request
from pathlib import Path

FONTS_DIR = Path("assets/fonts")

FONTS = {
    "ArchitectsDaughter-Regular.ttf": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/"
        "architectsdaughter/ArchitectsDaughter-Regular.ttf"
    ),
    "Caveat-Variable.ttf": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/"
        "caveat/Caveat%5Bwght%5D.ttf"
    ),
    "ComicNeue-Regular.ttf": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/"
        "comicneue/ComicNeue-Regular.ttf"
    ),
    "Montserrat-Variable.ttf": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/"
        "montserrat/Montserrat%5Bwght%5D.ttf"
    ),
}


def download_fonts() -> None:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in FONTS.items():
        dest = FONTS_DIR / filename
        if dest.exists():
            print(f"Ya existe: {filename}")
            continue
        print(f"Descargando: {filename} ...")
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"  OK: {filename}")
        except Exception as e:
            print(f"  ERROR descargando {filename}: {e}")

    print("Descarga de fuentes completada.")


if __name__ == "__main__":
    download_fonts()
