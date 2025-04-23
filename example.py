import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pya  # type: ignore
import shapes

# Creates a new, empty layout
# Layout is now the top-level design object. (Think: the whole chip/mask design file.)
layout = pya.Layout()

# Creates cell named "TOP" 
# A cell (sometimes called a "structure" in GDSII) is a reusable building block in a layout design that 
# holds shapes (polygons, paths, text), instances of other cells, or both. "TOP" is often the master or top-level cell.
top_cell = layout.create_cell("TOP")

# Creates cell named "CROSS"
cross_cell = layout.create_cell("CROSS")

# Creates (or gets) layer with datatype (1, 0)
# A layer is a virtual sheet or plane within your design file where you can draw specific types of shapes 
# (e.g., polygons, paths, text). Each layer typically represents a different physical or process step 
# in the manufacturing of a microchip, MEMS device, or photomask.
layer_cross = layout.insert_layer(pya.LayerInfo(1, 0))

# Creates (or gets) layer with datatype (2, 0)
layer_text = layout.insert_layer(pya.LayerInfo(2, 0))

# Generate a cross shape as a single polygon using the get_cross_shape function from the shapes module
cross =  shapes.get_cross_shape()

# Insert the cross polygon directly into the 'cross_cell' on the specified 'layer_cross'
cross_cell.shapes(layer_cross).insert(cross)

# Create an instance (copy) of the 'cross_cell' at the origin (0, 0)
# This allows for efficient placement of the entire cell as a reusable object
cross_instance = pya.CellInstArray(cross_cell.cell_index(), pya.Trans(pya.Point(0, 0)))

# Insert the instance of the cross_cell into the top-level cell (top_cell)
# This is how the cross appears in the main layout hierarchy
top_cell.insert(cross_instance)

# Save the entire layout to a GDS file using the write_to_gds function from the shapes module
shapes.write_to_gds(layout)