from pathlib import Path
import pya  # type: ignore
import math

"""Standard Wafer Sizes
Industry Name |	Diameter (mm) | Diameter (in) | Thickness (µm)
2-inch        | 50.8          | 2.0           | 275
3-inch        | 76.2          | 3.0           | 375
100 mm        | 100           | 3.94          | 525
125 mm        | 125           | 4.92          | 625
150 mm        | 150           | 5.91          | 675
200 mm        | 200           | 7.87          | 725
300 mm        | 300           | 11.81         | 775
450 mm        | 450           | 17.72         | 925
"""
# === Pattern Parameters ===
label_dimensions = {"size": 5, "unit": "um"}

cross_dimensions = {"size": 15, "line_width": 2, "unit": "um"}

cross_array_dimensions = {"spacing": 1000, "unit": "um"}

substrate_dimensions = {"size": 76.2, "unit": "mm"}

pattern_dimensions = {"size": substrate_dimensions["size"] / math.sqrt(2), "unit": "mm"}


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


def get_max_square_size():
    return substrate_dimensions["size"] / math.sqrt(2)


def get_pattern_size():
    spacing = convert_units(
        cross_array_dimensions["spacing"], cross_array_dimensions["unit"], "nm"
    )
    total_size = convert_units(
        pattern_dimensions["size"], pattern_dimensions["unit"], "nm"
    )
    return math.ceil(total_size / spacing)


def get_cross_shape():
    width = convert_units(
        cross_dimensions["line_width"], cross_dimensions["unit"], "nm"
    )
    size = convert_units(cross_dimensions["size"], cross_dimensions["unit"], "nm")

    vertical = {
        "left": width / 2 * -1,
        "bottom": size / 2 * -1,
        "right": width / 2,
        "top": size / 2,
    }

    horizontal = {
        "left": size / 2 * -1,
        "bottom": width / 2 * -1,
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
    return region


def get_label_length(label):
    size = convert_units(label_dimensions["size"], label_dimensions["unit"], "nm")
    return len(label) * (size / 2 + 250) / 2


def write_to_gds(layout):
    """Writes file. Filename is based on substrate dimensions, indexes name if already exists"""
    directory = Path("output").expanduser()
    directory.mkdir(parents=True, exist_ok=True)

    base_name = f"{substrate_dimensions['size']}{substrate_dimensions['unit']}_wafer_alignmentMarks"
    path = directory / f"{base_name}.gds"

    i = 1
    new_path = path
    while new_path.exists():
        new_path = directory / f"{base_name}_{i}.gds"
        i += 1

    layout.write(str(new_path))
    print(f"Done! Layout saved to: {new_path}")


layout = pya.Layout()
top_cell = layout.create_cell("TOP")
cross_cell = layout.create_cell("CROSS")
layer_cross = layout.insert_layer(pya.LayerInfo(1, 0))
layer_text = layout.insert_layer(pya.LayerInfo(2, 0))

for polygon in get_cross_shape().each():
    cross_cell.shapes(layer_cross).insert(polygon)


# === Generate array with labels as polygon shapes ===
text_gen = pya.TextGenerator.default_generator()
total_size = get_pattern_size()
spacing = convert_units(
    cross_array_dimensions["spacing"], cross_array_dimensions["unit"], "nm"
)

label_size_um = convert_units(label_dimensions["size"], label_dimensions["unit"], "um")

digits = {
    char: text_gen.text(char, layout.dbu, label_size_um)
    for char in [str(d) for d in range(10)] + ['R','C']
}

def build_label_region(label: str, digits: dict, digit_spacing: int) -> pya.Region:
    """Assemble a Region for a label string from pre-rendered digit Regions."""
    x_offset = 0
    label_region = pya.Region()

    for char in label:
        digit_region = digits[char].transformed(pya.Trans(pya.Point(x_offset, 0)))
        label_region += digit_region
        bbox = digits[char].bbox()
        x_offset += bbox.width() + digit_spacing

    return label_region

for row in range(total_size):
    for col in range(total_size):
        x = col * spacing
        y = row * spacing

        if row == total_size - 1:
            # === Final row: Insert author text once in the middle column ===
            if col == total_size // 2:
                text = "Created By: William Veith"
                text_region = text_gen.text(text, layout.dbu, label_size_um * 400)
                text_bbox = text_region.bbox()
                # Center the text at (x, y), with a little upward offset
                text_region = text_region.transformed(
                    pya.Trans(pya.Point(int(x - text_bbox.width() // 2), int(y + label_size_um * 2)))
                )
                top_cell.shapes(layer_text).insert(text_region)
            continue  # Skip crosses + label placement for this row

        # === Crosses and Labels for all other rows ===
        cross_instance = pya.CellInstArray(
            cross_cell.cell_index(), pya.Trans(pya.Point(x, y))
        )
        top_cell.insert(cross_instance)

        label_str = f"R{row}C{col}"
        label_region = build_label_region(label_str, digits, digit_spacing=350)

        cross_size = convert_units(cross_dimensions["size"], cross_dimensions["unit"], "nm")
        y_offset = cross_size + label_size_um 
        label_region = label_region.transformed(
            pya.Trans(pya.Point(x - label_region.bbox().width() // 2, y - y_offset))
        )

        top_cell.shapes(layer_text).insert(label_region)
        
write_to_gds(layout)