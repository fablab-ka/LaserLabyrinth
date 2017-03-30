import math

__author__ = 'Mark Weinreuter'

from boxmaker import *
import Polygon

Polygon.setTolerance(.01)
r = 21.1
ground = Hexagon(r)
g_height = ground.height
b_th = 3
r_inner = (ground.height - b_th) / math.cos(math.pi / 6)
inner = Hexagon(r_inner)

sl_inner = inner.side
bump_w = sl_inner / 2
print(r, ground.height, r_inner, inner.height)
# some wierd shit if I do this in a list/loop???
b1 = rect(bump_w, b_th)
b2 = rect(bump_w, b_th)
b3 = rect(bump_w, b_th)
b4 = rect(bump_w, b_th)
b5 = rect(bump_w, b_th)
b6 = rect(bump_w, b_th)
for i, b in enumerate([b1, b2, b3, b4, b5, b6]):
    ground.align_on_side(b, i, height_fac=-1)

ground -= b1
ground -= b2
ground -= b3
ground -= b4
ground -= b5
ground -= b6

write_svg("svg/g_plain.svg", ground)


h_mm = 50
wiggle = .05
r_laser = 4

# Side board with bumps at top/bottom an laser hole
bump = rect(bump_w - wiggle, b_th)
side_board = rect(sl_inner - .1, h_mm)  # .1 to add "some space" maybe remove?

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
hole_ib.position = rotate_point(10,0,math.pi/6)
g_power = ground - hole_ib

r_bolt = 3
g_power -= circle(r_bolt + wiggle)
write_svg("svg/g_power.svg", g_power)

# Mirror slits in 0 and 30°
mirror_slit = rect(24, .8)
g_mirror1 = ground - mirror_slit
mirror_slit.rotate(math.pi / 6)
g_mirror2 = ground - mirror_slit
write_svg("svg/g_mir_both_dirs.svg", [g_mirror1, g_mirror2])
