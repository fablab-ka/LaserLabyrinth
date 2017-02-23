#! /usr/bin/env python3
import math

__author__ = 'Mark Weinreuter'

from boxmaker import *

# size of the grid (amount of holes)
grid_w_count = 4
grid_h_count = 6

# block dimensions
block_size_half_mm = 20
block_hole_r_mm = 10
# distance between blocks
block_pad_mm = 5

# Rectangles are boring, make n-edge-shapes by 'misusing' a circle
edge_count = 8
angle_off = math.pi * 1 / edge_count

# size of the gameboard
grid_w_mm = grid_w_count * (block_pad_mm + block_size_half_mm * 2) + block_pad_mm
grid_h_mm = grid_h_count * (block_pad_mm + block_size_half_mm * 2) + block_pad_mm

# make some template shapes
grid = rect(grid_w_mm, grid_h_mm)
c_block = circle(block_size_half_mm, edge_count, angle_off)
c_small = circle(block_hole_r_mm, 256)


def make_holes(grid, hole_shape):
    """
    Punches holes into the given grid. Positions are specified through global
    varibales...

    :param grid:
    :type grid:
    :param hole_shape:
    :type hole_shape:
    :return:
    :rtype:
    """
    y = grid.back + block_pad_mm + block_size_half_mm

    for h in range(grid_h_count):
        x = grid.left + block_pad_mm + block_size_half_mm
        for w in range(grid_w_count):
            hole_shape.position = x, y
            grid -= hole_shape
            x += block_size_half_mm * 2 + block_pad_mm

        y += block_size_half_mm * 2 + block_pad_mm

    return grid


# make 2 layers with holes
grid1 = make_holes(grid, c_small)
grid2 = make_holes(grid, c_block)


write_svg("svg/grid_layer0.svg", grid)
write_svg("svg/grid_layer1.svg", grid1)
write_svg("svg/grid_layer2.svg", grid2)

