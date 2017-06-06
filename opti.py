import math
from laserbox.export import lines2path, bboxes_to_size, to_svg, write_svg
from laserbox.util import align_column

__author__ = 'Mark Weinreuter'

from hex_figure import sides_small, side_tall, align_row

s1 = side_tall.clone()
s2 = side_tall.clone()

s1.right = s2.left
l1 = s1.to_lines()
l2 = s2.to_lines()

sides = list(map(lambda s: s.clone() , sides_small))
align_row(sides,0,0)
list(map(lambda x: print(x.left), sides))
write_svg("test2.svg", sides)

last =sides[0].to_lines()
ps = [lines2path(last)]
bbs = [last.bbox]
for side in sides[1:]:
    ls = side.to_lines()
    last.hide_duplicates(ls)
    last = ls
    ps.append(lines2path(last))
    bbs.append(last.bbox)

size = bboxes_to_size(bbs)
to_svg("test.svg", size, ps)
