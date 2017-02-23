

difference() {
	union() {
		cylinder($fn = 8, center = true, h = 10, r = 20);
		translate(v = [0, 0, -7.5000000000]) {
			cylinder($fn = 256, center = true, h = 5, r = 10);
		}
	}
	cylinder(center = true, h = 100, r = 4);
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
__author__ = 'Mark Weinreuter'

from solid.utils import *

from config import *

c = cylinder(block_size_half_mm, h=block_base_h_mm, center=True, segments=edge_count)
c1 = cylinder(block_hole_r_mm, h=block_hole_h_mm, center=True, segments=256)
cable_hole = cylinder(cable_r_mm, h=block_base_h_mm*10, center=True)
base = c + down((block_base_h_mm + block_hole_h_mm) / 2)(c1)
base -= cable_hole

scad_render_to_file(base, "scad/block_base.scad")
 
 
************************************************/
