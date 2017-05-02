from laserbox import *

from config import *
from hex_grid_gen import grid_side

__author__ = 'Mark Weinreuter'

from hex_figure import side_small, side_small_hole, side_tall, side_tall_hole

side_small.rotate(math.pi / 2)
side_small_hole.rotate(math.pi / 2)

side_tall.rotate(math.pi / 2)
side_tall_hole.rotate(math.pi / 2)

sides_small = duplicate(
    [(side_tall, c_side_tall), (side_tall_hole, c_side_hole_tall),
     (side_small, c_side_small), (side_small_hole, c_side_hole_small)])
sides_small = align_column(sides_small, combine=True)
walls = duplicate([(grid_side, 6)])
# walls = [rect(100, 100), circle(100)]
walls = align_column(walls, pad=2, combine=True)

# sides_small.reset_position()
# grid = align_column([final_grid_bottom, walls, final_grid_top, final_grid_middle])
align_row([walls, sides_small])
write_svg("svg/all.svg", [walls, sides_small])
