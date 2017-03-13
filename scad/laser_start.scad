

union() {
	translate(v = [0, 0, 0]) {
		rotate(a = [0, 0, 0]) {
			difference() {
				translate(v = [0, 0, 0]) {
					rotate(a = [0, 0, 0]) {
						cylinder($fn = 6, center = true, h = 8, r1 = 21, r2 = 21);
					}
				}
				translate(v = [0, 0, 0]) {
					rotate(a = [0, 0, 0]) {
						cylinder($fn = 256, center = true, h = 10, r1 = 5, r2 = 5);
					}
				}
			}
		}
	}
	union() {
		difference() {
			translate(v = [0, 0, 19.0000000000]) {
				rotate(a = [0, 0, 0]) {
					difference() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								cylinder($fn = 6, center = true, h = 30, r1 = 16, r2 = 16);
							}
						}
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								cylinder($fn = 6, center = true, h = 32, r1 = 14, r2 = 14);
							}
						}
					}
				}
			}
			translate(v = [0.0000000000, 16.0000000000, 27.0000000000]) {
				rotate(a = [0, 90, 90]) {
					cylinder($fn = 256, center = true, h = 18, r1 = 2, r2 = 2);
				}
			}
		}
		translate(v = [0, 0, 139.0000000000]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					translate(v = [0, 0, 0]) {
						rotate(a = [0, 0, 0]) {
							cylinder($fn = 6, center = true, h = 10, r1 = 16, r2 = 10);
						}
					}
					translate(v = [0, 0, -1.0250000000]) {
						rotate(a = [0, 0, 0]) {
							cylinder($fn = 6, center = true, h = 8.0500000000, r1 = 14, r2 = 8);
						}
					}
				}
			}
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
__author__ = 'Mark Weinreuter'

from config import *


def tile_blocker(tile_blocker_h_mm=5):
    top = CY(r1=block_r_mm, r2=0, h=tile_blocker_h_mm, segments=6)

    tb = make_base()
    top.bottom = block_base_h_mm / 2
    tb += top
    scad_render_to_file(tb, "scad/tile_blocker.scad")


def laser_start():
    ls = make_base(True)
    t_h_mm = 30
    l_r = 2
    l_t_off = 5 + l_r
    t_r_mm = block_r_mm - 5
    turret = CY(t_r_mm, t_h_mm, segments=6)
    c2 = CY(t_r_mm - 2, t_h_mm + 2, segments=6)
    turret = W(turret - c2, d=t_h_mm)
    turret.bottom = ls.top
    l_hole = CY(l_r, t_r_mm*1+2,segments=256)
    # rotate cylinder in place
    l_hole.ry = 90
    l_hole.rz = 90
    # offset the cylinder
    l_hole.z = turret.top - l_t_off
    l_hole.x = math.cos(90/180*math.pi) * t_r_mm
    l_hole.y = math.sin(90/180*math.pi) * t_r_mm

    top_h_mm = 10
    top = CY(r1=t_r_mm, r2=10,h=top_h_mm,segments=6)
    topC = CY(r1=t_r_mm-2, r2=10-2,h=top_h_mm -1.95,segments=6)
    topC.bottom = top.bottom -0.05
    top = W(top - topC, d=top_h_mm)
    top.bottom = turret.top + 100
    ls += (turret  - l_hole)  + top()

    scad_render_to_file(ls(), "scad/laser_start.scad")


laser_start()
 
 
************************************************/
