__author__ = 'Mark Weinreuter'

from config import *


def ground_pipe():
    pass


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
    t_th = 2
    t_r_mm = block_r_mm - 5
    turret = CY(t_r_mm, t_h_mm, segments=6)
    c2 = CY(t_r_mm - t_th, t_h_mm + 2, segments=6)
    turret = W(turret - c2, d=t_h_mm)
    turret.bottom = ls.top
    l_hole = CY(l_r, t_r_mm * 1 + 2, segments=256)
    # rotate cylinder in place
    l_hole.ry = 90
    l_hole.rz = 90
    # offset the cylinder
    l_hole.z = turret.top - l_t_off
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
    top = W((top + top_con) -CY(r1=1.2,h=20,segments=256)(), d=top_h_mm)

    top.bottom = turret.top + 10
    ls += (turret - l_hole) + (top() )

    scad_render_to_file(ls(), "scad/laser_start.scad")


laser_start()
