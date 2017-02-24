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
