#! /usr/bin/env python3
import svgwrite
from laserbox import *

from config import *
from hex_figure import g_placeholder, g_mirror1, g_dual_mirror2, g_mirror2, g_dual_mirror1, g_plain, g_start, g_target, g_tab_holes, plates

__author__ = 'Mark Weinreuter'

# make some template shapes
g_extra = 5
grid_top = Ngon(6, grid_r_mm + g_extra, math.pi * 1 / 6)
grid_cuts = Ngon(6, grid_r_mm, math.pi * 1 / 6)
r_bottom = (grid_top.height + g_extra) / math.cos(math.pi / 6)
grid_bottom = Ngon(6, r_bottom, math.pi * 1 / 6)
grid_shape = Ngon(6, r_bottom, math.pi * 1 / 6)
c_block = Ngon(6, figure_r_mm)
c_small = circle(grid_hole_r_mm, 54)
c_outer = circle(grid_hole_r_mm * 2, 64)
magnet_r_mm = 2.51
c_magnet = circle(magnet_r_mm, 20)

print("Grid info: (height, side, radius)", grid_bottom.height, grid_bottom.side, grid_bottom.r)
parts = plates + [g_plain]* (37-len(plates))

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
    index = 0
    if isinstance(hole_shape, Poly):
        hole_shape = (hole_shape,) * 64
    for h in range(hex_block_count // 2 + 1):

        count = hex_block_count - h
        for pre in (-1, 1):
            x = -(count - 1) * hex_height_pad_mm
            for w in range(count):
                hole_shape[index].position = x, pre * y
                # shift every second row
                # if w % 2 == 1:
                #    hole_shape.y += hex_height_pad_mm

                grid -= hole_shape[index]  # make the hole
                x += hex_height_pad_mm * 2  # block_r_pad_mm + hex_side_len_half
                index += 1
            if h == 0:
                break
        y += block_r_pad_mm + hex_side_len_half

    return grid


# Add tabs for the outer walls
# height of the grid 6gon - the thickness is the new height
r_inner = (grid_top.height - b_th) / math.cos(math.pi / 6)
dummyGrid = Ngon(6, r_inner, math.pi * 1 / 6)

wall_h_mm = figure_height_mm
grid_side = rect(dummyGrid.side - side_wiggle, wall_h_mm)
n, w = mm_to_bumps(grid_top.side - 10, 10)
bumps = tbumps_w(n, w, b_th * 2,wo=.01)
bumps.front = grid_side.back
grid_side += bumps
bumps = tbumps_w(2, w+5, b_th,wo=5)
bumps.front = grid_side.front
grid_side -= bumps


cut_double = Poly()
cut2 = Poly()
for i in range(1, 7):
    # to fix weird edge cases, cut off bigger chucks but only half of them!
    b1 = grid_cuts.align_on_side(tbumps_w(n, w, b_th), i, height_fac=-1)
    b_double = grid_cuts.align_on_side(tbumps_w(n, w, b_th * 2), i, height_fac=0)
    cut_double += b_double
    cut2 += b1

grid_top -= cut2
grid_bottom = grid_bottom - cut2

# make 2 layers with holes
final_grid_top = make_comb_holes(grid_top, parts)
grid_shadow = make_comb_holes(grid_shape, g_tab_holes)
final_grid_bottom = make_comb_holes(grid_bottom, c_magnet)
# grid3 = make_comb_holes(grid, c_outer)

fs = 6
_, pos = grid_bottom.put_on_side(rect(10, 10), 5, height_fac=0)
y_pos = pos[1]

# Add fablab text
t = svgwrite.text.Text("", insert=(0, y_pos - 3), text_anchor="middle",
                       style="font-size:%g;font-family:'Ubuntu'line-height:1;" % fs)

t.add(svgwrite.text.TSpan("LaserLabyrinth v0.2"))
t.add(svgwrite.text.TSpan("by Fablab Karlsruhe", dx=(2,), style="font-size:3;"))
#final_grid_bottom.svg_extras.append(t)

# 3D preview
final_grid_top.d3z = b_th * 4
side_z = figure_height_mm
sides = []
for i in range(5):
    tmp_side = grid_side.clone()
    tmp_side.h_h = b_th / 2
    theta, pos = dummyGrid.put_on_side(tmp_side, i, height_fac=1)
    tmp_side.d3rot = (90, 0, (theta) / math.pi * 180)
    tmp_side.d3pos = (pos[0], pos[1], side_z)
    sides.append(tmp_side)

if __name__ == "__main__":
    # grid layers
    write_svg("svg/hg_bottom.svg", final_grid_bottom, offset=False)
    write_svg("svg/hg_top.svg", final_grid_top, offset=False)
    write_svg("svg/hg_shadow.svg", grid_shadow, offset=False)

    write_svg("svg/hg_wall.svg", grid_side)
    # all = [final_grid_bottom, final_grid_middle, final_grid_top, side]
    # write_svg("svg/hg_all.svg", all)

    # battery holder
    # b_box.export_svg("svg/bbox.svg")

    # to_openscad("scad/grid.scad", b_th, final_grid_bottom, final_grid_middle, final_grid_top, sides)
    # b_box.preview_openscad("scad/bbox.scad")
