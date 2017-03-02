

union() {
	union() {
		union() {
			translate(v = [36.0000000000, 0, 0]) {
				rotate(a = [0, 0, 90]) {
					difference() {
						linear_extrude(center = true, height = 7.9500000000) {
							polygon(paths = [[0, 1, 2, 3]], points = [[-31.9500000000, -3.9750000000], [31.9500000000, -3.9750000000], [24.0000000000, 3.9750000000], [-24.0000000000, 3.9750000000]]);
						}
						translate(v = [0, 2.0500000000, 0]) {
							cube(center = true, size = [63.9000000000, 4.1000000000, 2.0500000000]);
						}
					}
				}
			}
			translate(v = [-36.0000000000, 0, 0]) {
				rotate(a = [0, 0, -90]) {
					difference() {
						linear_extrude(center = true, height = 7.9500000000) {
							polygon(paths = [[0, 1, 2, 3]], points = [[-31.9500000000, -3.9750000000], [31.9500000000, -3.9750000000], [24.0000000000, 3.9750000000], [-24.0000000000, 3.9750000000]]);
						}
						translate(v = [0, 2.0500000000, 0]) {
							cube(center = true, size = [63.9000000000, 4.1000000000, 2.0500000000]);
						}
					}
				}
			}
		}
		translate(v = [0, 38.4000000000, 0]) {
			rotate(a = [0, 0, 180]) {
				difference() {
					linear_extrude(center = true, height = 7.9500000000) {
						polygon(paths = [[0, 1, 2, 3]], points = [[-30.4500000000, -3.9750000000], [30.4500000000, -3.9750000000], [22.5000000000, 3.9750000000], [-22.5000000000, 3.9750000000]]);
					}
					translate(v = [0, 2.0500000000, 0]) {
						cube(center = true, size = [60.9000000000, 4.1000000000, 2.0500000000]);
					}
				}
			}
		}
	}
	translate(v = [0, -38.4000000000, 0]) {
		rotate(a = [0, 0, 0]) {
			difference() {
				linear_extrude(center = true, height = 7.9500000000) {
					polygon(paths = [[0, 1, 2, 3]], points = [[-30.4500000000, -3.9750000000], [30.4500000000, -3.9750000000], [22.5000000000, 3.9750000000], [-22.5000000000, 3.9750000000]]);
				}
				translate(v = [0, 2.0500000000, 0]) {
					cube(center = true, size = [60.9000000000, 4.1000000000, 2.0500000000]);
				}
			}
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
from solid.objects import *
from solid.solidpython import scad_render_to_file

__author__ = 'Mark Weinreuter'

c = lambda w, h, d: cube([w, h, d], center=True)
trans = lambda x=0, y=0, z=0: translate([x, y, z])
rot = lambda x=0, y=0, z=0: rotate([x, y, z])

mirror_w = 45
mirror_h = 48
mirror_th = 2.05
h = 7.95  # mirror_th * 2
d = h  # mirror_th * 2


def side(w):
    w2 = w / 2
    h2 = h / 2
    w2h = w2 + h

    points = [(-w2h, -h2), (w2h, -h2), (w2, h2), (-w2, h2)]
    bar = linear_extrude(d, center=True)(polygon(points))
    cut = trans(y=mirror_th)(c(2 * w2h, mirror_th * 2, mirror_th))

    return bar - cut


pos_fac = .8
left = trans(mirror_w * pos_fac)(rot(z=90)(side(mirror_h)))
right = trans(-mirror_w * pos_fac)(rot(z=-90)(side(mirror_h)))
top = trans(y=-mirror_h * pos_fac)(rot(z=0)(side(mirror_w)))
bottom = trans(y=mirror_h * pos_fac)(rot(z=180)(side(mirror_w)))

con = left + right + bottom + top
scad_render_to_file(con, "scad/mirror_connector.scad")
 
 
************************************************/
