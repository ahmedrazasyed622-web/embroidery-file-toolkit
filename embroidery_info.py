"""
Embroidery File Toolkit
Basic utilities for reading embroidery file information.
"""

from pathlib import Path


SUPPORTED_FORMATS = {
    ".dst": "Tajima DST",
    ".pes": "Brother PES",
    ".jef": "Janome JEF",
    ".pec": "Brother PEC",
    ".exp": "Melco EXP",
}


def identify_format(file_path):
    """Identify the embroidery file format from its extension."""
    extension = Path(file_path).suffix.lower()

    return SUPPORTED_FORMATS.get(
        extension,
        "Unknown embroidery format"
    )


def get_file_info(file_path):
    """Return basic information about an embroidery file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return {
        "file_name": path.name,
        "file_size_bytes": path.stat().st_size,
        "format": identify_format(file_path),
    }


if __name__ == "__main__":
    print("Embroidery File Toolkit")
    print("-----------------------")
    print("Supported formats:")

    for extension, name in SUPPORTED_FORMATS.items():
        print(f"{extension.upper()}: {name}")
