__author__ = 'Mark Weinreuter'
import math

board_thickness = 5

# block dimensions
block_r_mm = 20
block_base_h_mm = 20
block_hole_r_mm = 10
block_hole_h_mm = board_thickness

# distance between blocks
block_pad_mm = 2
cable_r_mm = 6

# HEXAGONAL GRID
block_r_pad_mm = block_r_mm + block_pad_mm
hex_block_count = 7  # must be odd!

hex_side_len = math.sin(math.pi / 6) * 2 * block_r_pad_mm
hex_side_len_half = hex_side_len / 2
hex_height_pad_mm = math.sqrt(block_r_pad_mm ** 2 - hex_side_len_half ** 2)

hex_outer_edge_pad = 4 + 2 * block_pad_mm  # ~ 4 is needed for no overlap
# Size of the hexagonal grid
grid_r_mm = hex_block_count * hex_height_pad_mm + hex_outer_edge_pad

# REGULAR GRID: (amount of holes)
grid_w_count = 6
grid_h_count = 6

# size of the gameboard
grid_w_mm = grid_w_count * (block_pad_mm + block_r_mm * 2) + block_pad_mm
grid_h_mm = grid_h_count * (block_pad_mm + block_r_mm * 2) + block_pad_mm
