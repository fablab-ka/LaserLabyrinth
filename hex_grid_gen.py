#! /usr/bin/env python3

__author__ = 'Mark Weinreuter'

from boxmaker import *

from config import *

# make some template shapes

import boxmaker
grid = boxmaker.circle(grid_r_mm, 6, math.pi * 1/6)
c_block = boxmaker.circle(block_r_mm, 6)
c_small = boxmaker.circle(block_hole_r_mm, 256)
c_outer = boxmaker.circle(block_hole_r_mm*2, 256)



def make_comb_holes(grid, hole_shape):
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

    y = 0#grid.back + block_pad_mm + hex_height_pad_mm

    for h in range(hex_block_count //2+1):

        count = hex_block_count - h
        for pre in (-1, 1):
            x = -(count -1) * hex_height_pad_mm
            for w in range(count):
                hole_shape.position = x,  pre * y
                # shift every second row
                #if w % 2 == 1:
                #    hole_shape.y += hex_height_pad_mm

                grid -= hole_shape  # make the hole
                x += hex_height_pad_mm * 2#block_r_pad_mm + hex_side_len_half

        y += block_r_pad_mm + hex_side_len_half

    return grid


twa

grid_side_len
tbumps_w()


# make 2 layers with holes
grid1 = make_comb_holes(grid, c_small)
grid2 = make_comb_holes(grid, c_block)
grid3 = make_comb_holes(grid, c_outer)

write_svg("svg/hex_grid_layer0.svg", grid)
write_svg("svg/hex_grid_layer1.svg", grid1)
write_svg("svg/hex_grid_layer2.svg", grid2)
write_svg("svg/hex_grid_layer3.svg", grid3)


