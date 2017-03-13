from solid import *

__author__ = 'Mark Weinreuter'
import math

board_thickness = 4

# block dimensions
block_r_mm = 21  # the current gameboard hexagons have a radius of about 43mm

block_base_h_mm = board_thickness * 2
block_hole_r_mm = 5
block_hole_h_mm = board_thickness

# mirror
mirror_thickness = 4
mirror_slit_width = block_r_mm * 1.5

# distance between blocks
block_pad_mm = 2
cable_r_mm = 3
connector_r_mm = 2.5
connector_dist_mm = block_r_mm - connector_r_mm * 3

# HEXAGONAL GRID
block_r_pad_mm = block_r_mm + block_pad_mm
hex_block_count = 7  # must be odd!

hex_side_len = math.sin(math.pi / 6) * 2 * block_r_pad_mm
hex_side_len_half = hex_side_len / 2
hex_height_pad_mm = math.sqrt(block_r_pad_mm ** 2 - hex_side_len_half ** 2)

hex_outer_edge_pad = 4 + 8 * block_pad_mm  # ~ 4 is needed for no overlap
# Size of the hexagonal grid
grid_r_mm = hex_block_count * hex_height_pad_mm + hex_outer_edge_pad

c = lambda w, h, d: cube([w, h, d], center=True)
trans = lambda x=0, y=0, z=0: translate([x, y, z])
rot = lambda x=0, y=0, z=0: rotate([x, y, z])
rotz = lambda z: rotate([0, 0, z])


class W(object):
    def __init__(self, obj, w=0, h=0, d=0):
        self.w2 = w / 2
        self.h2 = h / 2
        self.d2 = d / 2
        self.obj = obj
        self.right = self.w2
        self.left = -self.w2
        self.f = self.h2
        self.ba = -self.h2
        self.t = self.d2
        self.b = -self.d2
        self.x = 0
        self.y = 0
        self.z = 0
        self.rx = 0
        self.ry = 0
        self.rz = 0

    @property
    def top(self):
        return self.z + self.d2

    @top.setter
    def top(self, val):
        self.z = val - self.d2

    @property
    def bottom(self):
        return self.z - self.d2

    @bottom.setter
    def bottom(self, val):
        self.z = val + self.d2

    @property
    def front(self):
        return self.y + self.h2

    @front.setter
    def front(self, val):
        self.y = val - self.h2

    @property
    def back(self):
        return self.y - self.h2

    @back.setter
    def back(self, val):
        self.y = val + self.h2

    def __sub__(self, other):
        return self() - other()

    def __add__(self, other):
        return self() + other()

    def __call__(self, *args, **kwargs):
        return translate([self.x, self.y, self.z])(rotate([self.rx, self.ry, self.rz])((self.obj)))


class C(W):
    def __init__(self, w, h, d):
        super().__init__(cube([w, h, d], center=True), w, h, d)


class CY(W):
    def __init__(self, r1, h, r2=None, segments=None):
        if r2 is None:
            r2 = r1
        super().__init__(cylinder(r1=r1, r2=r2, h=h, segments=segments, center=True), r1 * 2, r1 * 2, h)


def make_base(hole=False):
    c = CY(block_r_mm, block_base_h_mm, segments=6)
    if hole:
        c1 = CY(block_hole_r_mm, block_base_h_mm + 2, segments=256)
        c = W(c - c1, block_r_mm * 2, block_r_mm * 2, block_base_h_mm)

    return c
