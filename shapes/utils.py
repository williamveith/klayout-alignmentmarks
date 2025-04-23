from pathlib import Path
import pya  # type: ignore

def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a length value between different units of measurement.

    Supported units:
        - "in"  : inches
        - "mm"  : millimeters
        - "um"  : micrometers
        - "µm"  : micrometers (alternate symbol)
        - "nm"  : nanometers (base unit)

    The function internally normalizes all conversions to nanometers.

    Args:
        value (float): The numeric value to convert.
        from_unit (str): The unit of the input value.
        to_unit (str): The desired output unit.

    Returns:
        float: The converted value in the target unit.
    """
    factors = {
        "in": 25.4e6,
        "mm": 1e6,
        "um": 1e3,
        "µm": 1e3,
        "nm": 1,
    }
    return value * factors[from_unit.lower()] / factors[to_unit.lower()]

def write_to_gds(
    layout: 'pya.Layout',
    filename: str = "Experimental Pattern",
    overwrite_existing: bool = True
) -> Path:
    """
    Write the given KLayout layout to a GDS file in the 'output' directory.

    Args:
        layout (pya.Layout): The layout object to write.
        filename (str): The base filename (without extension).
        overwrite_existing (bool): If False, increment filename to avoid overwrite.

    Returns:
        Path: The final file path used.
    """
    directory = Path("output").expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    
    path = directory / f"{filename}.gds"
    
    if not overwrite_existing:
        i = 1
        while path.exists():
            path = directory / f"{filename}_{i}.gds"
            i += 1
    
    layout.write(str(path))
    print(f"Done! Layout saved to: {path}")
    return path