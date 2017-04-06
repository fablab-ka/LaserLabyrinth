#! /usr/bin/env python3
import svgwrite
from laserbox import *
from laserbox.export import to_openscad

from config import *

__author__ = 'Mark Weinreuter'

# make some template shapes

g_extra = 10
grid_top = Ngon(6, grid_r_mm, math.pi * 1 / 6)
grid_middle = Ngon(6, grid_r_mm + g_extra, math.pi * 1 / 6)
grid_bottom = Ngon(6, grid_r_mm + g_extra * 2, math.pi * 1 / 6)
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
r_inner = (grid_top.height - board_thickness) / math.cos(math.pi / 6)
dummyGrid = Ngon(6, r_inner, math.pi * 1 / 6)

wall_h_mm = 80
side = rect(dummyGrid.side - side_wiggle, wall_h_mm)
n, w = mm_to_bumps(grid_top.side - 10, 10)
bumps = tbumps_w(n, w, board_thickness * 3)
bumps.front = side.back
side += bumps
write_svg("svg/hg_wall.svg", side)



cut_double = Poly()
cut2 = Poly()
for i in range(1, 7):
    # to fix weird edge cases, cut off bigger chucks but only half of them!
    b1 = grid_top.align_on_side(tbumps_w(n, w, board_thickness), i, height_fac=-1)
    b_double = grid_top.align_on_side(tbumps_w(n, w, board_thickness * 2), i, height_fac=0)
    cut_double += b_double
    cut2 += b1

grid_top -= cut_double
grid_middle -= cut2
final_grid_bottom = grid_bottom -cut2
# make 2 layers with holes
final_grid_middle = make_comb_holes(grid_middle, c_small)
final_grid_top = make_comb_holes(grid_top, c_block)
#grid3 = make_comb_holes(grid, c_outer)

fs = 6
theta, pos = grid_bottom.get_side_info(rect(10, 10), 5,height_fac=-0.45)
print(pos)
t = svgwrite.text.Text("LaserLabyrinth v0.2 ♥ Fablab Ka",insert=(0, pos[1]),text_anchor="middle", style="font-size:%g;font-family:'Arial'"%fs)
final_grid_bottom.svg_extras.append(t)


write_svg("svg/hex_grid_layer0.svg", final_grid_bottom, offset=False)
exit()
write_svg("svg/hex_grid_layer1.svg", final_grid_middle)
write_svg("svg/hex_grid_layer2.svg", final_grid_top)
# write_svg("svg/hex_grid_layer3.svg", grid3)


# 3D preview

final_grid_middle.d3z = board_thickness * 2
final_grid_top.d3z = board_thickness * 4
side_z = figure_height_mm
sides = []
for i in range(5):
    tmp_side = side.clone()
    tmp_side.h_h = board_thickness / 2
    theta, pos = dummyGrid.get_side_info(tmp_side, i, height_fac=1)
    tmp_side.d3rot = (90, 0, (theta) / math.pi * 180)
    tmp_side.d3pos = (pos[0], pos[1], side_z)
    sides.append(tmp_side)

to_openscad("scad/grid.scad", board_thickness, final_grid_bottom, final_grid_middle, final_grid_top, sides)