from laserbox import *

from config import *
from hex_grid_gen import grid_side

__author__ = 'Mark Weinreuter'

from hex_figure import side_small, side_small_hole, side_tall, side_tall_hole

side_small.rotate(math.pi / 2)
side_small_hole.rotate(math.pi / 2)

side_tall.rotate(math.pi / 2)
side_tall_hole.rotate(math.pi / 2)


def align_column(data, pad=2, outer_pad=None, max_size=600):
    outer_pad = outer_pad if outer_pad is not None else pad

    max_w = -1
    total = 0
    parts = []
    for p in data:
        if not isinstance(p, (tuple, list)):
            parts.append((p, 1))
        else:
            parts.append(p)

    for p in parts:
        total += p[1]

    index, p_index = 0, 0
    x = outer_pad
    last = Poly()
    last.front = outer_pad - pad  # make first tile have outer padding
    container = []
    cp = parts[index][0]

    for i in range(total):

        if p_index == parts[index][1]:
            index += 1
            p_index = 0
            cp = parts[index][0]

        p_index += 1

        part = cp  # .clone()
        max_w = max(max_w, part.w_h * 2)
        part.leftback = x, last.front + pad
        last = part

        if part.front >= max_size - outer_pad:
            x += max_w + pad
            max_w = part.w_h * 2
            part.leftback = x, outer_pad

        container.append(part)
    return container


def align_row(data, pad=2, outer_pad=None, max_size=600):
    outer_pad = outer_pad if outer_pad is not None else pad

    max_h = -1
    total = 0
    parts = []
    for p in data:
        if not isinstance(p, (tuple, list)):
            parts.append((p, 1))
        else:
            parts.append(p)

    for p in parts:
        total += p[1]

    index, p_index = 0, 0
    y = outer_pad
    last = Poly()
    last.left = outer_pad - pad  # make first tile have outer padding
    container = Poly()
    cp = parts[index][0]

    for i in range(total):

        if p_index == parts[index][1]:
            index += 1
            p_index = 0
            cp = parts[index][0]

        p_index += 1

        part = cp  # .clone()
        max_h = max(max_h, part.h_h * 2)
        part.leftback = last.right + pad, y
        last = part

        if part.front >= max_size - outer_pad:
            y += max_h + pad
            max_h = part.h_h * 2
            part.leftback = outer_pad, y

        container += part
    return container


sides_small = align_column(
    [(side_tall, c_side_tall), (side_tall_hole, c_side_hole_tall),
     (side_small, c_side_small), (side_small_hole, c_side_hole_small)])
walls = align_column([(grid_side, 6)], max_size=300, pad=2)
# sides_small.reset_position()
# grid = align_column([final_grid_bottom, walls, final_grid_top, final_grid_middle])
write_svg("svg/all.svg", [sides_small, walls])  # align_row([grid, sides_small]))
