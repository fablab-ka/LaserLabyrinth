#! /usr/bin/env python3

__author__ = 'Mark Weinreuter'

from boxmaker import *

from config import *

# make some template shapes
grid = rect(grid_w_mm, grid_h_mm)
r_block = rect(block_r_mm * 2, block_r_mm * 2)
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
    y = grid.back + block_r_mm + block_pad_mm

    for h in range(grid_h_count):
        x = grid.left + block_r_mm + block_pad_mm

        for w in range(grid_w_count):
            hole_shape.position = x, y
            grid -= hole_shape
            x += block_r_mm * 2 + block_pad_mm

        y += block_r_mm * 2 + block_pad_mm

    return grid


# make 2 layers with holes
grid1 = make_holes(grid, c_small)
grid2 = make_holes(grid, r_block)

write_svg("svg/grid_layer0.svg", grid)
write_svg("svg/grid_layer1.svg", grid1)
write_svg("svg/grid_layer2.svg", grid2)
