

union() {
	union() {
		union() {
			translate(v = [40, 0, 0]) {
				rotate(a = [0, 0, 90]) {
					difference() {
						linear_extrude(center = true, height = 8) {
							polygon(paths = [[0, 1, 2, 3]], points = [[-38.0000000000, -4.0000000000], [38.0000000000, -4.0000000000], [30.0000000000, 4.0000000000], [-30.0000000000, 4.0000000000]]);
						}
						translate(v = [0, 4, 0]) {
							cube(center = true, size = [76.0000000000, 8, 4]);
						}
					}
				}
			}
			translate(v = [-40, 0, 0]) {
				rotate(a = [0, 0, -90]) {
					difference() {
						linear_extrude(center = true, height = 8) {
							polygon(paths = [[0, 1, 2, 3]], points = [[-38.0000000000, -4.0000000000], [38.0000000000, -4.0000000000], [30.0000000000, 4.0000000000], [-30.0000000000, 4.0000000000]]);
						}
						translate(v = [0, 4, 0]) {
							cube(center = true, size = [76.0000000000, 8, 4]);
						}
					}
				}
			}
		}
		translate(v = [0, 60, 0]) {
			rotate(a = [0, 0, 180]) {
				difference() {
					linear_extrude(center = true, height = 8) {
						polygon(paths = [[0, 1, 2, 3]], points = [[-28.0000000000, -4.0000000000], [28.0000000000, -4.0000000000], [20.0000000000, 4.0000000000], [-20.0000000000, 4.0000000000]]);
					}
					translate(v = [0, 4, 0]) {
						cube(center = true, size = [56.0000000000, 8, 4]);
					}
				}
			}
		}
	}
	translate(v = [0, -60, 0]) {
		rotate(a = [0, 0, 0]) {
			difference() {
				linear_extrude(center = true, height = 8) {
					polygon(paths = [[0, 1, 2, 3]], points = [[-28.0000000000, -4.0000000000], [28.0000000000, -4.0000000000], [20.0000000000, 4.0000000000], [-20.0000000000, 4.0000000000]]);
				}
				translate(v = [0, 4, 0]) {
					cube(center = true, size = [56.0000000000, 8, 4]);
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

mirror_w = 40
mirror_h = 60
mirror_th = 4
h = mirror_th * 2
d = mirror_th * 2


def side(w):
    w2 = w / 2
    h2 = h / 2
    w2h = w2 + h

    points = [(-w2h, -h2), (w2h, -h2), (w2, h2), (-w2, h2)]
    bar = linear_extrude(d, center=True)(polygon(points))
    cut = trans(y=mirror_th)(c(2 * w2h, mirror_th * 2, mirror_th))

    return bar - cut


left = trans(mirror_w)(rot(z=90)(side(mirror_h)))
right = trans(-mirror_w)(rot(z=-90)(side(mirror_h)))
top = trans(y=-mirror_h)(rot(z=0)(side(mirror_w)))
bottom = trans(y=mirror_h)(rot(z=180)(side(mirror_w)))

con = left + right + bottom + top
scad_render_to_file(con, "scad/mirror_connector.scad")
 
 
************************************************/
