

difference() {
	translate(v = [0, 0, 0]) {
		rotate(a = [0, 0, 0]) {
			cylinder($fn = 6, center = true, h = 8, r1 = 21, r2 = 21);
		}
	}
	translate(v = [0, 0, 4.0000000000]) {
		rotate(a = [0, 0, 60]) {
			cube(center = true, size = [32.0000000000, 4.5000000000, 8]);
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
__author__ = 'Mark Weinreuter'

from config import *

cut = C(mirror_slit_width +.5, mirror_thickness+.5, block_base_h_mm)
cut.rz = 90
cut.z = block_base_h_mm / 2
base = make_base()

mir_tile1 = base - cut
cut.rz = 60
mir_tile2 = base - cut

scad_render_to_file(mir_tile1, "scad/mirror_tile1.scad")
scad_render_to_file(mir_tile2, "scad/mirror_tile2.scad")

# holes_rots = (60, 60 + 180, 60 + 90, (60 + 90 + 180))
# holes = []
# for rot in holes_rots:
#    holes.append(
#        up(block_base_h_mm / 2)(rotate([0, 0, rot])(left(connector_dist_mm)(cylinder(connector_r_mm, h=block_base_h_mm, center=True, segments=256)))))


cable_hole = cylinder(cable_r_mm, h=block_base_h_mm * 10, center=True)
# base -= cable_hole
# for h in holes:
#    base -= h

turret_w = 30
turret_height = 50
turret_th = 10
t = cube([turret_w, turret_w, turret_height], center=True)
t_cutout = cube([turret_w - 2 * turret_th, turret_w, turret_height], center=True)
t -= translate([0, turret_th, -turret_th])(t_cutout)

scad_render_to_file(t, "scad/block_turret.scad")
 
 
************************************************/
