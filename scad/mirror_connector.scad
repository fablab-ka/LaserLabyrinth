

union() {
	translate(v = [0, -29.0000000000, 0]) {
		rotate(a = [0, 0, 0]) {
			cube(center = true, size = [31.5000000000, 6, 4.1000000000]);
		}
	}
	difference() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				cube(center = true, size = [49, 52, 4.1000000000]);
			}
		}
		translate(v = [0, 0, 2.0500000000]) {
			rotate(a = [0, 0, 0]) {
				cube(center = true, size = [45, 48, 4.2000000000]);
			}
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
from solid.objects import *
from solid.solidpython import scad_render_to_file

from config import *

__author__ = 'Mark Weinreuter'


mirror_w = 45
mirror_h = 48
mirror_th = 2.1
h = 7.95  # mirror_th * 2
d = h  # mirror_th * 2


def side(w):
    h2 = h / 2
    w2 = w / 2 - h2
    w2h = w2 + h

    points = [(-w2h, -h2), (w2h, -h2), (w2, h2), (-w2, h2)]
    bar = linear_extrude(d, center=True)(polygon(points))
    cut = trans(y=mirror_th)(c(w, mirror_th * 2, mirror_th))

    print(points)

    return bar - cut


pos_fac = .8
left = trans(mirror_w * pos_fac)(rot(x=90)(side(mirror_h)))
right = trans(-mirror_w * pos_fac)(rot(x=90)(side(mirror_h)))
top = trans(y=-mirror_h * pos_fac)(rot(x=90)(side(mirror_w)))
bottom = trans(y=mirror_h * pos_fac)(rot(x=90)(side(mirror_w)))

con = left + right + bottom + top
scad_render_to_file(con, "scad/mirror_connector_old.scad")

frame_th = 2
frame = C(mirror_w + 2 * frame_th, mirror_h + 2 * frame_th, mirror_th + frame_th)
mirror = C(mirror_w, mirror_h, mirror_th * 2)
mirror.z = frame.top
mir_con2 = frame - mirror

cut_fit = C(mirror_slit_width, 6, mirror_th + frame_th)
cut_fit.front = frame.back

mir_con2 = cut_fit + mir_con2
scad_render_to_file(mir_con2, "scad/mirror_connector.scad")
 
 
************************************************/
