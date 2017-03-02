

difference() {
	union() {
		cylinder($fn = 6, center = true, h = 8, r = 21);
		translate(v = [0, 0, -6.0000000000]) {
			cylinder($fn = 256, center = true, h = 4, r = 5);
		}
	}
	rotate(a = [0, 0, [0, 0, 150]]) {
		translate(v = [0, 0, 4.0000000000]) {
			cube(center = true, size = [63, 8, 8]);
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
__author__ = 'Mark Weinreuter'

from solid.utils import *

from config import *

mirror_thickness = 8

c = cylinder(block_r_mm, h=block_base_h_mm, center=True, segments=6)
c1 = cylinder(block_hole_r_mm, h=block_hole_h_mm, center=True, segments=256)

cut = cube([block_r_mm * 3, mirror_thickness, block_base_h_mm], center=True)

rotz = lambda z: rotate([0, 0, z])

cut = rotz([0, 0, 90 + 60])(up(block_base_h_mm / 2)(cut))

# holes_rots = (60, 60 + 180, 60 + 90, (60 + 90 + 180))
# holes = []
# for rot in holes_rots:
#    holes.append(
#        up(block_base_h_mm / 2)(rotate([0, 0, rot])(left(connector_dist_mm)(cylinder(connector_r_mm, h=block_base_h_mm, center=True, segments=256)))))


cable_hole = cylinder(cable_r_mm, h=block_base_h_mm * 10, center=True)
base = c + down((block_base_h_mm + block_hole_h_mm) / 2)(c1)
# base -= cable_hole
# for h in holes:
#    base -= h

turret_w = 30
turret_height = 50
turret_th = 10
t = cube([turret_w, turret_w, turret_height], center=True)
t_cutout = cube([turret_w - 2 * turret_th, turret_w, turret_height], center=True)
t -= translate([0, turret_th, -turret_th])(t_cutout)

base -= cut

scad_render_to_file(t, "scad/block_turret.scad")
scad_render_to_file(base, "scad/block_base.scad")
 
 
************************************************/
