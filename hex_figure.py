from laserbox import *
from laserbox.export import to_openscad

from config import *

__author__ = 'Mark Weinreuter'

g_plain = Ngon(6, figure_r_mm)
g_height = g_plain.height
b_th = 3
# the side boards touch on the inner edge
# => calc the inner radius (radius of the 6gon where the height is reduced by the board thickness)
r_inner = (g_plain.height - b_th) / math.cos(math.pi / 6)
inner = Ngon(6, r_inner)

sl_inner = inner.side
bump_w = sl_inner / 2
print("Hex figur radii:", figure_r_mm, g_plain.height, r_inner, inner.height)

cut = Poly()
tab = tbumps_w(2, b_th + 2, b_th, wo=1.5 + 0.025)
for i in range(6):
    b = g_plain.align_on_side(Poly(tab.to_polygon()), i, height_fac=-1)
    cut += b

g_tab_holes = cut
g_plain -= cut
print(g_plain[0])
g_blocker2 = g_plain.clone()
g_blocker4 = g_plain.clone()

wiggle = .0
r_laser = 3.01

# Side board with bumps at top/bottom an laser hole
bump = tbumps_w(2, b_th + 2, b_th, wo=1.5 + wiggle)  # rect(bump_w - wiggle, b_th)
side_tall = rect(sl_inner - side_wiggle, figure_height_mm)

# smaller board influenced by the dual mirror which is 40mm tall
side_small = rect(sl_inner - side_wiggle, 40 - 2 * b_th)  # TODO: hier ggf. 41

bump.back = side_tall.front
side_tall += bump
bump.front = side_tall.back
side_tall += bump

bump.back = side_small.front
side_small += bump
bump.front = side_small.back
side_small += bump

# slit for inner cable board
w_slit = 10
slit = rect(w_slit + wiggle, b_th + wiggle)
slit.y = side_tall.back + 10 + b_th
side_tall_slit = side_tall - slit
slit_bar = rect(w_slit, (g_height * 2))

# laser hole
laser_hole = circle(r_laser, 32)
side_tall_hole = side_tall - laser_hole
light_slit = rect(3, 10)
light_slit.back = laser_hole.y
side_tall_target = side_tall_hole.clone() - light_slit

# redefine laser hole
laser_hole = circle(r_laser + 2, 32)

# laser hole and slit
side_tall_slit_hole = side_tall_slit - laser_hole

# the laser hole is in the middle: 25mm + b_th
b_off = 0  # .5? compensate for the "unterlegscheibe"
laser_hole.y = side_small.back + figure_height_mm / 2 + b_th + b_off
side_small_hole = side_small - laser_hole

# Inner board as a stopper and cable guide
hole_ib = circle(2)
inner_board = rect(w_slit, 2 * g_height)
inner_board -= hole_ib
hole_ib.y = 10
inner_board -= hole_ib
g_power = g_plain.clone()

g_9v = g_plain.clone()
b9v = rect(27, 17)
hole = circle(2.05)
hole.y = -13
b9v.back = -6
g_9v -= hole
hole = circle(3, 32)
hole.position = b9v.right, b9v.y
b9v += hole
b9v.reset_position()
g_9v -= b9v
g_9v -= cut

"""
# Ground plate with holes for power supply
for i in range(6):
    h = circle(2)
    h.position = rotate_point(10, 0, (i + 1) * math.pi / 3 + math.pi / 6)
    # every other hole only
    if i % 2 == 0:
        g_power -= h

r_bolt = 3
g_power -= circle(r_bolt + wiggle)
"""

g_start = g_plain - rect(20, 4)  # hole for a button

g_target = g_plain - circle(3.05)  # hole for a button

# Mirror slits in 0 and 30°
mirror_slit = rect(16, .55)
# make them reflect of the surface
mirror_slit.front = 0
g_mirror1 = g_plain - mirror_slit
mirror_slit.position = 0, 0
x, y = rotate_point(0, mirror_slit.h_h, math.pi / 6)
mirror_slit.rotate(math.pi / 6)
mirror_slit.position = x, y
g_mirror2 = g_plain - mirror_slit

# dual mirror dim: 30x41x1
dualmir_slit = rect(30 + wiggle, 1.2, wiggle)
# make them reflect of the surface
dualmir_slit.front = 0
g_dual_mirror1 = g_plain - dualmir_slit
dualmir_slit.reset_position()

x, y = rotate_point(0, dualmir_slit.h_h, math.pi / 6)
dualmir_slit.rotate(math.pi / 6)
dualmir_slit.position = x, y
g_dual_mirror2 = g_plain - dualmir_slit

# placeholder
r_middle = figure_r_mm - b_th * 2
r_small = figure_r_mm - b_th * 3
con_hole = rect(b_th, b_th, wiggle + .05)
g_placeholder = g_plain - con_hole
g_ph2 = Ngon(6, r_middle) - con_hole
g_ph3 = Ngon(6, r_small) - con_hole
con = rect(b_th, 4 * b_th)

f_start = [[g_9v, g_start], [side_tall_slit, side_tall_slit_hole] + [side_tall] * 4]
f_target = [[g_target, g_plain], [side_tall_hole] * 6]

f_mir1 = [[g_mirror1, g_mirror1], [side_small_hole] * 2 + [side_small] * 4]
f_mir2 = [[g_mirror2, g_mirror2], [side_small_hole] * 2 + [side_small] * 4]

f_dmir1 = [[g_dual_mirror1, g_dual_mirror1], [side_small_hole] * 4 + [side_small] * 2]
f_dmir2 = [[g_dual_mirror2, g_dual_mirror2], [side_small_hole] * 4 + [side_small] * 2]

f_blocker2 = [[g_blocker2, g_plain], [side_small_hole] * 4 + [side_small] * 2]
f_blocker4 = [[g_blocker4, g_plain], [side_small_hole] * 2 + [side_small] * 4]

f_placeholder = [[g_placeholder], [g_ph2, g_ph3]]

plates = f_start[0] * c_start + f_target[0] * c_target + f_mir1[0] * c_mir1 + f_mir2[0] * c_mir2 + \
         f_dmir1[0] * c_dmir1 + f_dmir2[0] * c_dmir2 + f_blocker2[0] * c_dir_blocker2 + f_blocker4[0] * c_dir_blocker4 + f_placeholder[
                                                                                                                             0] * c_placeholder

sides_tall = f_start[1] * c_start + f_target[1] * c_target
sides_small = f_mir1[1] * c_mir1 + f_mir2[1] * c_mir2 + f_dmir1[1] * c_dmir1 + f_dmir2[1] * c_dmir2 + \
              f_blocker4[1] * c_dir_blocker4 + f_blocker2[1] * c_dir_blocker2

if __name__ == "__main__":
    write_svg("svg/side_hole.svg", side_tall_hole)
    write_svg("svg/side_plain.svg", side_tall)
    write_svg("svg/side_slit.svg", side_tall_slit)
    write_svg("svg/side_slit_hole.svg", side_tall_slit_hole)
    write_svg("svg/side_target.svg", side_tall_target)

    write_svg("svg/slit_bar.svg", slit_bar)
    write_svg("svg/ssm_plain.svg", side_small)
    write_svg("svg/ssm_hole.svg", side_small_hole)

    write_svg("svg/slit_board.svg", inner_board)

    write_svg("svg/g_power.svg", g_power)
    write_svg("svg/g_9v.svg", g_9v)

    write_svg("svg/g_start.svg", g_start)
    write_svg("svg/g_target.svg", g_target)
    write_svg("svg/g_plain.svg", g_plain)
    write_svg("svg/g_mir_both_dirs.svg", [g_mirror1, g_mirror2])

    write_svg("svg/g_dual_mir_both_dirs.svg", [g_dual_mirror1, g_dual_mirror2])

    ex = {"extras": {"max_width": figure_r_mm * 2 * 3 + 1}}
    write_svg("svg/all_start.svg", [g_power, g_plain, side_tall_hole, side_tall, side_tall, side_tall, side_tall, side_tall],
              align=ex)

    write_svg("svg/place_holder.svg", [g_placeholder, g_ph2, g_ph3, con])

    hf_all_plates = [g_plain, g_power, g_start, g_target, g_mirror1, g_mirror2, g_dual_mirror1, g_dual_mirror2, g_placeholder]

    # rotation only for export!
    side_tall.rotate(math.pi / 2)
    side_tall_hole.rotate(math.pi / 2)
    side_small.rotate(math.pi / 2)
    side_small_hole.rotate(math.pi / 2)
    hf_all_sides = [side_tall, side_tall_hole, side_small, side_small_hole]

    align_row(hf_all_plates, max_size=160)
    align_column(hf_all_sides)
    write_svg("svg/hf_plates.svg", hf_all_plates)
    write_svg("svg/hf_sides.svg", hf_all_sides)

    # 3D preview
    if False:
        side_z = figure_height_mm / 2 + b_th
        sides = []
        for i in range(6):
            tmp_side = side_tall_hole.clone() if i % 3 == 0 else side_tall.clone()
            tmp_side.h_h = b_th / 2
            theta, pos = inner.place_on_side(i, normal_off=tmp_side.h_h)
            tmp_side.d3rot = (90, 0, (theta) / math.pi * 180)
            tmp_side.d3pos = (pos[0], pos[1], side_z)
            sides.append(tmp_side)
        top = g_plain.clone()
        top.d3z = figure_height_mm + b_th * 2
        to_openscad("scad/hex_figure.scad", b_th, g_plain, top, sides)
