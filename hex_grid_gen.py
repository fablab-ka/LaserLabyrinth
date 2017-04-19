#! /usr/bin/env python3
import svgwrite
from laserbox import *
from laserbox.export import to_openscad

from config import *

__author__ = 'Mark Weinreuter'

# make some template shapes
g_extra = 10
grid_top = Ngon(6, grid_r_mm, math.pi * 1 / 6)
r_middle = (grid_top.height + g_extra) / math.cos(math.pi / 6)
r_bottom = (grid_top.height + g_extra * 2) / math.cos(math.pi / 6)
grid_middle = Ngon(6, r_middle, math.pi * 1 / 6)
grid_bottom = Ngon(6, r_bottom, math.pi * 1 / 6)
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
r_inner = (grid_top.height - b_th) / math.cos(math.pi / 6)
dummyGrid = Ngon(6, r_inner, math.pi * 1 / 6)

wall_h_mm = 80
side = rect(dummyGrid.side - side_wiggle, wall_h_mm)
n, w = mm_to_bumps(grid_top.side - 10, 10)
bumps = tbumps_w(n, w, b_th * 3)
bumps.front = side.back
side += bumps
write_svg("svg/hg_wall.svg", side)

cut_double = Poly()
cut2 = Poly()
for i in range(1, 7):
    # to fix weird edge cases, cut off bigger chucks but only half of them!
    b1 = grid_top.align_on_side(tbumps_w(n, w, b_th), i, height_fac=-1)
    b_double = grid_top.align_on_side(tbumps_w(n, w, b_th * 2), i, height_fac=0)
    cut_double += b_double
    cut2 += b1

grid_top -= cut_double
grid_middle -= cut2
final_grid_bottom = grid_bottom - cut2
# make 2 layers with holes
final_grid_middle = make_comb_holes(grid_middle, c_small)
final_grid_top = make_comb_holes(grid_top, c_block)
# grid3 = make_comb_holes(grid, c_outer)

fs = 6
_, pos = grid_bottom.put_on_side(rect(10, 10), 5, height_fac=0)
y_pos = pos[1]

bb_w_mm = 80
bb_d_mm = 50
bb_h_mm = 40
conf = BoxConfig(walls=Sides3D(fr=False, to=False))
b_box = Box(bb_w_mm, bb_d_mm, bb_h_mm, b_th, config=conf)
bbb_size = 4
bb_cut = rect(bbb_size, b_th)
stairs = rect(20, b_th)
tmp = rect(10, b_th)
tmp.rightback = stairs.rightfront
stairs += tmp
stairs.rightback = b_box.walls[LEFT].rightback
b_box.walls[LEFT] -= stairs
stairs = rect(20, b_th)
tmp = rect(10, b_th)
tmp.leftback = stairs.leftfront
stairs += tmp
stairs.leftback = b_box.walls[RIGHT].leftback
b_box.walls[RIGHT] -= stairs

# connection pins
bb_cut.leftback = b_box.walls[RIGHT].left + 10 + (10 - bbb_size) / 2, b_box.walls[RIGHT].back
b_box.walls[RIGHT] += bb_cut
bb_cut.leftback = b_box.walls[RIGHT].left + (10 - bbb_size) / 2, b_box.walls[RIGHT].back + b_th
b_box.walls[RIGHT] += bb_cut

bb_cut.rightback = b_box.walls[LEFT].right - 10 - (10 - bbb_size) / 2, b_box.walls[RIGHT].back
b_box.walls[LEFT] += bb_cut
bb_cut.rightback = b_box.walls[LEFT].right - (10 - bbb_size) / 2, b_box.walls[RIGHT].back + b_th
b_box.walls[LEFT] += bb_cut

# lidholer
lh = square_hole(bbb_size + .1, b_th)
lh.rightback = b_box.walls[LEFT].rightfront
b_box.walls[LEFT] += lh

lh = square_hole(bbb_size + .1, b_th)
lh.leftback = b_box.walls[RIGHT].leftfront
b_box.walls[RIGHT] += lh
bb_lid = rect(bb_w_mm + 2 * b_th, bb_d_mm + b_th) # + b_th to cover front

# möpple to turn
bbl_bump = rect(b_th, bbb_size)
bbl_rem = rect(b_th, bb_lid.h_h * 2 - 3 * lh.w_h)

bbl_bump.right = bb_lid.left
bbl_bump.y = bb_lid.front - lh.w_h
bbl_rem.rightback = bb_lid.leftback
bb_lid += bbl_bump
bb_lid += bbl_rem

bbl_bump.left = bb_lid.right
bbl_rem.left = bb_lid.right

bb_lid += bbl_bump
bb_lid += bbl_rem


bb_lid.d3z = bb_h_mm / 2
b_box.extras.append(bb_lid)

# adjust bottom
bo_off = rect(bb_w_mm * 2, 20)
bo_off.front = b_box.walls[BOTTOM].front
b_box.walls[BOTTOM] -= bo_off
b_box.walls[BOTTOM].d3z -= 50
b_box.export_svg("svg/bbox.svg")
b_box.preview_openscad("scad/bbox.scad")

# cut holes to place the battery box
bb_cut = rect(b_th, bbb_size)
bb_cut.position = -bb_w_mm / 2, -y_pos + 5
final_grid_bottom -= bb_cut
bb_cut.position = bb_w_mm / 2, -y_pos + 5
final_grid_bottom -= bb_cut

bb_cut.position = -bb_w_mm / 2, -y_pos + 15
final_grid_middle -= bb_cut
bb_cut.position = bb_w_mm / 2, -y_pos + 15
final_grid_middle -= bb_cut

# Add fablab text
t = svgwrite.text.Text("", insert=(0, y_pos - 3), text_anchor="middle",
                       style="font-size:%g;font-family:'Ubuntu'line-height:1;" % fs)

t.add(svgwrite.text.TSpan("LaserLabyrinth v0.2"))
t.add(svgwrite.text.TSpan("by Fablab Karlsruhe", dx=(2,), style="font-size:3;"))
final_grid_bottom.svg_extras.append(t)

write_svg("svg/hex_grid_layer0.svg", final_grid_bottom, offset=False)
write_svg("svg/hex_grid_layer1.svg", final_grid_middle, offset=False)
write_svg("svg/hex_grid_layer2.svg", final_grid_top, offset=False)
# write_svg("svg/hex_grid_layer3.svg", grid3)


# 3D preview

final_grid_middle.d3z = b_th * 2
final_grid_top.d3z = b_th * 4
side_z = figure_height_mm
sides = []
for i in range(5):
    tmp_side = side.clone()
    tmp_side.h_h = b_th / 2
    theta, pos = dummyGrid.put_on_side(tmp_side, i, height_fac=1)
    tmp_side.d3rot = (90, 0, (theta) / math.pi * 180)
    tmp_side.d3pos = (pos[0], pos[1], side_z)
    sides.append(tmp_side)

to_openscad("scad/grid.scad", b_th, final_grid_bottom, final_grid_middle, final_grid_top, sides)

all = [final_grid_bottom, final_grid_middle, final_grid_top]
write_svg("svg/hg_all.svg", all)
