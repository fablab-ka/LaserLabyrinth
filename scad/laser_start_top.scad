

translate(v = [0, 0, 77.0000000000]) {
	rotate(a = [0, 0, 0]) {
		difference() {
			union() {
				translate(v = [0, 0, 0]) {
					rotate(a = [0, 0, 0]) {
						difference() {
							translate(v = [0, 0, 0]) {
								rotate(a = [0, 0, 0]) {
									cylinder($fn = 6, center = true, h = 10, r1 = 21, r2 = 10);
								}
							}
							translate(v = [0, 0, -1.0100000000]) {
								rotate(a = [0, 0, 0]) {
									cylinder($fn = 6, center = true, h = 8, r1 = 18.6000000000, r2 = 8);
								}
							}
						}
					}
				}
				translate(v = [0, 0, -5.0000000000]) {
					rotate(a = [0, 0, 0]) {
						difference() {
							translate(v = [0, 0, 0]) {
								rotate(a = [0, 0, 0]) {
									cylinder($fn = 6, center = true, h = 5, r1 = 19.3000000000, r2 = 19.3000000000);
								}
							}
							translate(v = [0, 0, 0]) {
								rotate(a = [0, 0, 0]) {
									cylinder($fn = 6, center = true, h = 7, r1 = 18.6000000000, r2 = 18.6000000000);
								}
							}
						}
					}
				}
			}
			translate(v = [0, 0, 0]) {
				rotate(a = [0, 0, 0]) {
					cylinder($fn = 256, center = true, h = 20, r1 = 2.5000000000, r2 = 2.5000000000);
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


def ground_pipe():
    fit = 0.05
    pipe = CY(block_hole_r_mm-fit, block_hole_h_mm, segments=256)
    c = CY(cable_r_mm, block_hole_h_mm+2, segments=256)
    scad_render_to_file(pipe-c, "scad/cable_pipe.scad")


def tile_blocker(tile_blocker_h_mm=5):
    top = CY(r1=block_r_mm, r2=0, h=tile_blocker_h_mm, segments=6)

    tb = make_base()
    top.bottom = block_base_h_mm / 2
    tb += top
    scad_render_to_file(tb, "scad/tile_blocker.scad")


def laser_start():
    ls = make_base(True)
    t_h_mm = 50
    l_r = 3.25
    l_b_off = t_h_mm/1.5
    t_th = 1.2
    t_r_mm = block_r_mm
    turret = CY(t_r_mm, t_h_mm, segments=6)
    c2 = CY(t_r_mm - t_th, t_h_mm + 2, segments=6)
    turret = W(turret - c2, d=t_h_mm)
    turret.bottom = ls.top
    l_hole = CY(l_r, t_r_mm * 1 + 2, segments=256)
    # rotate cylinder in place
    l_hole.ry = 90
    l_hole.rz = 90
    # offset the cylinder
    l_hole.z = turret.bottom + l_b_off
    l_hole.x = math.cos(90 / 180 * math.pi) * t_r_mm
    l_hole.y = math.sin(90 / 180 * math.pi) * t_r_mm

    top_h_mm = 10
    con_h_mm = 5
    top = CY(r1=t_r_mm, r2=10, h=top_h_mm, segments=6)
    # hollow out the top
    topC = CY(r1=t_r_mm - t_th*2, r2=10 - 2, h=top_h_mm - 2, segments=6)
    topC.bottom = top.bottom - 0.01  # just for a better preview
    top_con = CY(r1=t_r_mm - t_th - 0.5, h=con_h_mm, segments=6)
    top_con_hole = CY(r1=t_r_mm - t_th * 2, h=con_h_mm+2, segments=6)
    top_con = W(top_con-top_con_hole, h=con_h_mm)
    top_con.top = top.bottom

    top = W(top - topC, d=top_h_mm)
    top = W((top + top_con) -CY(r1=2.5,h=20,segments=256)(), d=top_h_mm)

    top.bottom = turret.top + 20
    ls += (turret - l_hole)

    scad_render_to_file(ls(), "scad/laser_start.scad")
    scad_render_to_file(top(), "scad/laser_start_top.scad")



laser_start()
ground_pipe()
 
 
************************************************/
