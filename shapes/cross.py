import pya  # type: ignore
from .utils import convert_units

def get_cross_shape(
    cross_size: float = 10,
    line_width: float = 2,
    units: str = "um"
) -> 'pya.Polygon':
    """
    Generate a single polygon representing a centered cross ("plus sign") shape.

    The cross is composed of a vertical and a horizontal rectangle, both centered at the origin (0, 0).
    The rectangles are combined and returned as a single polygon, suitable for direct insertion
    into a KLayout cell.

    Args:
        cross_size (float): The full length of each cross arm, measured from end to end (default: 10).
        line_width (float): The width of each cross arm (default: 2).
        units (str): The units for cross_size and line_width. Supported values: "in", "mm", "um", "µm", "nm".

    Returns:
        pya.Polygon: The merged cross shape as a single polygon object.

    Raises:
        RuntimeError: If the merged region does not result in exactly one polygon.

    Example:
        polygon = get_cross_shape(15, 2, "um")
        cell.shapes(layer).insert(polygon)
    """
    size = convert_units(cross_size, units, "nm")
    width = convert_units(line_width, units, "nm")

    vertical = {
        "left": -width / 2,
        "bottom": -size / 2,
        "right": width / 2,
        "top": size / 2,
    }

    horizontal = {
        "left": -size / 2,
        "bottom": -width / 2,
        "right": size / 2,
        "top": width / 2,
    }

    vertical_box = pya.Box(
        vertical["left"], vertical["bottom"], vertical["right"], vertical["top"]
    )
    horizontal_box = pya.Box(
        horizontal["left"], horizontal["bottom"], horizontal["right"], horizontal["top"]
    )

    region = pya.Region(vertical_box) + pya.Region(horizontal_box)
    region.merge()

    polygons = list(region.each())
    if len(polygons) != 1:
        raise RuntimeError(f"Expected one polygon, got {len(polygons)}")
    return polygons[0]