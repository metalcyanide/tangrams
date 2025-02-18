from matplotlib import pyplot
from math import sin, cos
from shapely.geometry import Polygon, Point, LineString
from shapely import affinity
from descartes.patch import PolygonPatch

import polygonrep

polygons = polygonrep.create_tanpieces()


from figures import SIZE, BLUE, GRAY, set_limits, add_origin

fig = pyplot.figure(1, figsize=SIZE, dpi=90)

a = polygonrep.create_polygon([1,1,1,1],[90,90,90,90])
b = polygonrep.create_polygon([1,1,1,1],[135,45,135,45])

triangle = a.union(b)
# 1
ax = fig.add_subplot(121)

patch = PolygonPatch(b, facecolor=GRAY, edgecolor=GRAY,
                     alpha=0.5, zorder=1)
triangle_a = affinity.scale(triangle, xfact=1.5, yfact=-1)
patch_a = PolygonPatch(triangle_a, facecolor=BLUE, edgecolor=BLUE,
                       alpha=0.5, zorder=2)
ax.add_patch(patch)
ax.add_patch(patch_a)

add_origin(ax, triangle, 'center')

ax.set_title("a) xfact=1.5, yfact=-1")

set_limits(ax, 0, 5, 0, 4)

# 2
ax = fig.add_subplot(122)

patch = PolygonPatch(triangle, facecolor=GRAY, edgecolor=GRAY,
                     alpha=0.5, zorder=1)
triangle_b = affinity.scale(triangle, xfact=2, origin=(1, 1))
patch_b = PolygonPatch(triangle_b, facecolor=BLUE, edgecolor=BLUE,
                       alpha=0.5, zorder=2)
ax.add_patch(patch)
ax.add_patch(patch_b)

add_origin(ax, triangle, (1, 1))

ax.set_title("b) xfact=2, origin=(1, 1)")

set_limits(ax, 0, 5, 0, 4)

pyplot.show()