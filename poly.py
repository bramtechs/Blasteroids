import sys


class Polygon:
    def __init__(self):
        self.vertices = []

    def update(self, delta):
        self.vertices = self.gen_vertices()

    def draw(self, screen, color):
        pass

    def gen_vertices(self) -> []:
        return []

        # https://www.youtube.com/watch?v=7Ik2vowGcU0

    def overlaps(self, other) -> bool:
        poly1 = self
        poly2 = other

        for shape in range(2):
            if shape == 1:
                poly1 = other
                poly2 = self

            for a in range(len(poly1.vertices)):
                b = (a + 1) % len(poly1.vertices)

                # get the normal of the edge
                axis_proj = (
                    -(poly1.vertices[b][1] - poly1.vertices[a][1]),
                    poly1.vertices[b][0] - poly1.vertices[a][0]
                )

                # work out min and max 1D points for self
                min_r1 = sys.float_info.max
                max_r1 = sys.float_info.min

                for p in range(len(poly1.vertices)):
                    q = poly1.vertices[p][0] * axis_proj[0] + poly1.vertices[p][1] * axis_proj[1]
                    min_r1 = min(min_r1, q)
                    max_r1 = max(max_r1, q)

                # work out min and max 1D points for other
                min_r2 = sys.float_info.max
                max_r2 = sys.float_info.min

                for p in range(len(poly2.vertices)):
                    q = poly2.vertices[p][0] * axis_proj[0] + poly2.vertices[p][1] * axis_proj[1]
                    min_r2 = min(min_r2, q)
                    max_r2 = max(max_r2, q)

                # check if extents of shadows overlap
                if not (max_r2 >= min_r1 and max_r1 >= min_r2):
                    return False
        return True
