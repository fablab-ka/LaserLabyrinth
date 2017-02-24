

difference() {
	difference() {
		difference() {
			difference() {
				union() {
					cylinder($fn = 6, center = true, h = 10, r = 20);
					translate(v = [0, 0, -7.5000000000]) {
						cylinder($fn = 256, center = true, h = 5, r = 10);
					}
				}
				translate(v = [0, 0, 5.0000000000]) {
					rotate(a = [0, 0, 60]) {
						translate(v = [-12.5000000000, 0, 0]) {
							cylinder($fn = 256, center = true, h = 10, r = 2.5000000000);
						}
					}
				}
			}
			translate(v = [0, 0, 5.0000000000]) {
				rotate(a = [0, 0, 240]) {
					translate(v = [-12.5000000000, 0, 0]) {
						cylinder($fn = 256, center = true, h = 10, r = 2.5000000000);
					}
				}
			}
		}
		translate(v = [0, 0, 5.0000000000]) {
			rotate(a = [0, 0, 150]) {
				translate(v = [-12.5000000000, 0, 0]) {
					cylinder($fn = 256, center = true, h = 10, r = 2.5000000000);
				}
			}
		}
	}
	translate(v = [0, 0, 5.0000000000]) {
		rotate(a = [0, 0, 330]) {
			translate(v = [-12.5000000000, 0, 0]) {
				cylinder($fn = 256, center = true, h = 10, r = 2.5000000000);
			}
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
__author__ = 'Mark Weinreuter'

from solid.utils import *

from config import *

c = cylinder(block_r_mm, h=block_base_h_mm, center=True, segments=6)
c1 = cylinder(block_hole_r_mm, h=block_hole_h_mm, center=True, segments=256)

holes_rots = (60, 60 + 180, 60 + 90, (60+ 90 + 180))
holes = []
for rot in holes_rots:
    holes.append(up(block_base_h_mm/2)(rotate([0, 0, rot])(left(connector_dist_mm)(cylinder(connector_r_mm, h=block_base_h_mm, center=True, segments=256)))))

cable_hole = cylinder(cable_r_mm, h=block_base_h_mm * 10, center=True)
base = c + down((block_base_h_mm + block_hole_h_mm) / 2)(c1)
# base -= cable_hole
for h in holes:
    base -= h

scad_render_to_file(base, "scad/block_base.scad")
print("done")
 
 
************************************************/
