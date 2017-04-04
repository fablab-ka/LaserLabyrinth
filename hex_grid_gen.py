#! /usr/bin/env python3
from laserbox import *

from config import *

__author__ = 'Mark Weinreuter'

# make some template shapes

grid = Ngon(6, grid_r_mm, math.pi * 1 / 6)
c_block = circle(figure_r_mm, 6)
c_small = circle(grid_hole_r_mm, 54)
c_outer = circle(grid_hole_r_mm * 2, 64)


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

    y = 0  # grid.back + block_pad_mm + hex_height_pad_mm

    for h in range(hex_block_count // 2 + 1):

        count = hex_block_count - h
        for pre in (-1, 1):
            x = -(count - 1) * hex_height_pad_mm
            for w in range(count):
                hole_shape.position = x, pre * y
                # shift every second row
                # if w % 2 == 1:
                #    hole_shape.y += hex_height_pad_mm

                grid -= hole_shape  # make the hole
                x += hex_height_pad_mm * 2  # block_r_pad_mm + hex_side_len_half

        y += block_r_pad_mm + hex_side_len_half

    return grid


# Add tabs for the outer walls
# height of the grid 6gon - the thickness is the new height
r_inner = (grid.height - board_thickness) / math.cos(math.pi / 6)
dummyGrid = Ngon(6, r_inner)

wall_h_mm = 80
side = rect(dummyGrid.side, wall_h_mm)
n, w = mm_to_bumps(grid.side - 10, 10)
bumps = tbumps_w(n, w, board_thickness * 3)
bumps.front = side.back
side += bumps
write_svg("svg/hg_wall.svg", side)

cut = Poly()
for i in range(1, 7):
    # to fix weird edge cases, cut off bigger chucks but only half of them!
    b2 = grid.align_on_side(tbumps_w(n, w, board_thickness * 2), i, height_fac=0)
    cut += b2

grid -= cut

# make 2 layers with holes
grid1 = make_comb_holes(grid, c_small)
grid2 = make_comb_holes(grid, c_block)
grid3 = make_comb_holes(grid, c_outer)

write_svg("svg/hex_grid_layer0.svg", grid, offset=False)
write_svg("svg/hex_grid_layer1.svg", grid1)
write_svg("svg/hex_grid_layer2.svg", grid2)
# write_svg("svg/hex_grid_layer3.svg", grid3)
