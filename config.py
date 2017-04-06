import math

__author__ = 'Mark Weinreuter'

board_thickness = 4

# block dimensions
figure_r_mm = 21  # the current gameboard hexagons have a radius of about 43mm
figure_height_mm = 50
grid_hole_r_mm = 5

# mirror
mirror_thickness = 4
mirror_slit_width = figure_r_mm * 1.5

# distance between blocks
block_pad_mm = 2
cable_r_mm = 1.5
connector_r_mm = 2.5
connector_dist_mm = figure_r_mm - connector_r_mm * 3

# HEXAGONAL GRID
block_r_pad_mm = figure_r_mm + block_pad_mm
hex_block_count = 7  # must be odd!

hex_side_len = math.sin(math.pi / 6) * 2 * block_r_pad_mm
hex_side_len_half = hex_side_len / 2
hex_height_pad_mm = math.sqrt(block_r_pad_mm ** 2 - hex_side_len_half ** 2)

hex_outer_edge_pad = 4 + 8 * block_pad_mm  # ~ 4 is needed for no overlap
# Size of the hexagonal grid
grid_r_mm = hex_block_count * hex_height_pad_mm + hex_outer_edge_pad



side_wiggle = .1  # .1 to add "some space" maybe remove?
