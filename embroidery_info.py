
"""Embroidery File Toolkit
Read basic information from machine embroidery files.
"""

from pathlib import Path
import re
import sys

SUPPORTED_FORMATS = {
    ".dst": "Tajima DST",
    ".pes": "Brother PES",
    ".jef": "Janome JEF",
    ".pec": "Brother PEC",
    ".exp": "Melco EXP",
}


def identify_format(file_path):
    """Identify a file format from its extension."""
    extension = Path(file_path).suffix.lower()
    return SUPPORTED_FORMATS.get(
        extension, "Unknown embroidery format"
    )


def get_header_number(fields, key):
    """Read a numeric value from a DST header field."""
    value = fields.get(key)

    if value is None:
        return None

    match = re.search(r"[+-]?\d+", value)
    return int(match.group()) if match else None


def read_dst_info(file_path):
    """Read basic metadata and count DST stitch commands."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    data = path.read_bytes()

    if len(data) < 512:
        raise ValueError("File is too small to contain a DST header.")

    header = data[:512].decode("ascii", errors="replace")

    if not header.startswith("LA:"):
        raise ValueError("This does not look like a standard DST file.")

    fields = {}

    for line in header.replace("\r", "\n").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()

    body = data[512:]
    usable_length = len(body) - (len(body) % 3)

    sewn_stitches = 0
    jumps = 0
    color_changes = 0
    records_read = 0
    end_found = False

    for offset in range(0, usable_length, 3):
        b0, b1, b2 = body[offset:offset + 3]

        if (b0, b1, b2) == (0, 0, 0xF3):
            end_found = True
            break

        records_read += 1

        if (b2 & 0xC0) == 0xC0:
            color_changes += 1
        elif b2 & 0x80:
            jumps += 1
        else:
            sewn_stitches += 1

    plus_x = get_header_number(fields, "+X")
    minus_x = get_header_number(fields, "-X")
    plus_y = get_header_number(fields, "+Y")
    minus_y = get_header_number(fields, "-Y")

    width_mm = None
    height_mm = None

    if plus_x is not None and minus_x is not None:
        width_mm = (abs(plus_x) + abs(minus_x)) / 10

    if plus_y is not None and minus_y is not None:
        height_mm = (abs(plus_y) + abs(minus_y)) / 10

    return {
        "file_name": path.name,
        "file_size_bytes": len(data),
        "design_label": fields.get("LA", "").strip(),
        "header_stitch_count": get_header_number(fields, "ST"),
        "header_color_changes": get_header_number(fields, "CO"),
        "width_mm": width_mm,
        "height_mm": height_mm,
        "sewn_stitches_detected": sewn_stitches,
        "jump_records": jumps,
        "color_change_records": color_changes,
        "records_read": records_read,
        "end_marker_found": end_found,
    }


def main():
    if len(sys.argv) < 2:
        print("Embroidery File Toolkit")
        print("-----------------------")
        print("Supported formats:", ", ".join(SUPPORTED_FORMATS))
        print("Usage: python embroidery_info.py design.dst")
        print("Detailed analysis is currently available for DST.")
        return

    path = Path(sys.argv[1])

    if not path.is_file():
        print(f"Error: File not found: {path}")
        return

    print("Embroidery File Toolkit")
    print("-----------------------")
    print(f"File name: {path.name}")
    print(f"File size: {path.stat().st_size} bytes")
    print(f"Detected format: {identify_format(path)}")

    if path.suffix.lower() != ".dst":
        print("Detailed analysis is currently available for DST files.")
        return

    try:
        info = read_dst_info(path)

        print(f"Design label: {info['design_label'] or 'Not provided'}")
        print(f"Header stitch count: {info['header_stitch_count']}")
        print(f"Header color changes: {info['header_color_changes']}")
        print(f"Sewn stitch records detected: {info['sewn_stitches_detected']}")
        print(f"Jump records: {info['jump_records']}")
        print(f"Color-change records detected: {info['color_change_records']}")

        if info["width_mm"] is not None:
            width = info["width_mm"]
            print(f"Design width: {width:.1f} mm ({width / 25.4:.2f} inches)")
        else:
            print("Design width: Not available in header")

        if info["height_mm"] is not None:
            height = info["height_mm"]
            print(f"Design height: {height:.1f} mm ({height / 25.4:.2f} inches)")
        else:
            print("Design height: Not available in header")

        print(f"End marker found: {info['end_marker_found']}")

    except (OSError, ValueError) as error:
        print(f"Error reading DST file: {error}")


if __name__ == "__main__":
    main()
