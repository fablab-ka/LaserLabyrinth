import math

from laserbox import *

from config import figure_height_mm, figure_r_mm

__author__ = 'Mark Weinreuter'

ground = Ngon(6, figure_r_mm)
g_height = ground.height
b_th = 3
# the side boards touch on the inner edge
# => calc the inner radius (radius of the 6gon where the height is reduced by the board thickness)
r_inner = (ground.height - b_th) / math.cos(math.pi / 6)
inner = Ngon(6, r_inner)

sl_inner = inner.side
bump_w = sl_inner / 2
print(figure_r_mm, ground.height, r_inner, inner.height)
# some wierd shit if I do this in a list/loop???
cut = Poly()
tab = tbumps_w(2, b_th + 2, b_th, wo=1.5)
for i in range(6):
    b = ground.align_on_side(Poly(tab.to_polygon()), i, height_fac=-1)
    cut += b

ground -= cut

write_svg("svg/g_plain.svg", ground)

wiggle = .05
r_laser = 3

# Side board with bumps at top/bottom an laser hole

bump = tbumps_w(2, b_th + 2, b_th, wo=1.5 + wiggle)  # rect(bump_w - wiggle, b_th)
side_board = rect(sl_inner - .1, figure_height_mm)  # .1 to add "some space" maybe remove?

bump.back = side_board.front
side_board += bump
bump.front = side_board.back
side_board += bump
write_svg("svg/side_plain.svg", side_board)

# slit for inner cable board
w_slit = 10
slit = rect(w_slit + wiggle, b_th + wiggle)
slit.y = side_board.back + 10
s_side = side_board - slit
write_svg("svg/side_slit.svg", s_side)

# laser hole
laser_hole = circle(r_laser, 256)
h_side = side_board - laser_hole
write_svg("svg/side_hole.svg", h_side)

# laser hole and slit
s_side -= laser_hole
write_svg("svg/side_slit_hole.svg", s_side)

# Inner board as a stopper and cable guide
hole_ib = circle(2)
inner_board = rect(w_slit, 2 * g_height)
inner_board -= hole_ib
hole_ib.y = 10
inner_board -= hole_ib
write_svg("svg/inner_board.svg", inner_board)

# Ground plate with holes for power supply
hole_ib.position = rotate_point(10, 0, math.pi / 6)
g_power = ground - hole_ib

r_bolt = 3
g_power -= circle(r_bolt + wiggle)
write_svg("svg/g_power.svg", g_power)

# Mirror slits in 0 and 30°
mirror_slit = rect(24, .75)
g_mirror1 = ground - mirror_slit
mirror_slit.rotate(math.pi / 6)
g_mirror2 = ground - mirror_slit
write_svg("svg/g_mir_both_dirs.svg", [g_mirror1, g_mirror2])

# dual mirror dim: 30x41x1
dualmir_slit = rect(30 + wiggle, 1, wiggle)
g_dual_mirror1 = ground - dualmir_slit
dualmir_slit.rotate(math.pi / 6)
g_dual_mirror2 = ground - mirror_slit
write_svg("svg/g_dual_mir_both_dirs.svg", [g_dual_mirror1, g_dual_mirror2])

# placeholder
r_middle = figure_r_mm - b_th * 2
r_small = figure_r_mm - b_th * 3
con_hole = rect(b_th, b_th, wiggle)
g_ph1 = ground - con_hole
g_ph2 = Ngon(6, r_middle) - con_hole
g_ph3 = Ngon(6, r_small) - con_hole
con = rect(b_th, 5 * b_th)
write_svg("svg/place_holder.svg", [g_ph1, g_ph2, g_ph3, con])
