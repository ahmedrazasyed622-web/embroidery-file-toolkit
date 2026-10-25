# Embroidery File Toolkit

A free and open-source Python toolkit for inspecting machine embroidery files.

## Current Features

- Identify common embroidery file extensions
- Read basic Tajima DST header information
- Extract design label and header metadata
- Estimate design width and height from DST header bounds
- Count basic stitch, jump, and color-change records
- Detect the DST end marker

## Supported Formats

| Format | Current Support |
|---|---|
| DST | Basic metadata analysis |
| PES | Extension identification only |
| JEF | Extension identification only |
| PEC | Extension identification only |
| EXP | Extension identification only |

Other formats are not fully parsed yet.

## Requirements

- Python 3
- No additional packages required

## Usage

Run the tool with a DST embroidery file:

```bash
python embroidery_info.py design.dst
