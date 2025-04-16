# Alignment Mark Array Generator for KLayout

This script generates a GDS file containing a grid of cross-shaped alignment marks labeled by row and column. This script was created to explore and get familiar with KLayout’s Python API and batch processing workflow.

## Features

- Square array of alignment marks
- Configurable dimensions and spacing
- Label generation using `TextGenerator`
- Unit conversion across `in`, `mm`, `µm`, `um`, and `nm`
- Automatic file versioning to prevent overwrites
- Author attribution embedded as a label in the final row

## Output

- GDS files are saved in an `output/` directory relative to the script.
- If a file with the default name already exists, a numeric suffix is appended.

## Prerequisites

- [KLayout](https://www.klayout.de/) (used for layout generation and rendering)
- Python scripting is handled via KLayout’s built-in `pya` module
- Visual Studio Code (optional, for debugging and automation)

## Running the Script

### Method 1: KLayout Batch Mode

Run the script directly with:

```bash
/Applications/KLayout.app/Contents/MacOS/klayout -b -r square-of-alignment-marks.py
```

### Method 2: Visual Studio Code (Recommended for Iteration)

This project includes optional VS Code configuration files under `.vscode/`:

- **`launch.json`** — Enables Python debugging of the script from within VS Code.
- **`tasks.json`** — Automates running the script through KLayout’s batch interface.

To use:

1. Open the project folder in VS Code.
2. Use `Run Task` to trigger GDS generation.
3. Use `Run > Start Debugging` (F5) to test Python logic inside VS Code.

## Attribution

The last row of the array includes a centered label:

```text
Created By: William Veith
```

This serves as a digital signature for traceability and versioning.

## Purpose

This is a basic, practical script for:

- Learning the KLayout scripting interface
- Testing layout automation techniques
- Creating consistent training/test samples for lithography tools
