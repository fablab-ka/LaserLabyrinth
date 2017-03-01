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
