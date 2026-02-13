import numpy as np

class Voxel:
    def __init__(self, i, j, k, position, size):
        self.i = i
        self.j = j
        self.k = k
        self.position = position  # Centro del voxel (x, y, z)
        self.size = size          # Tamaño del voxel (lx, ly, lz)
        self.epsilon = 10e-6

        self.min_corner = self.position - self.size / 2
        self.max_corner = self.position + self.size / 2

        self.density = None       # Se calculará después
        self.total_energy_loss = 0.0
        self.n_tracks = 0

        self.total_energy_loss = 0.0
        self.total_weight = 0.0

    def is_inside(self, point):
        point = np.array(point)
        return np.all(point >= self.min_corner) and np.all(point < self.max_corner)
        #min_corner y max_corner tienen que cambiar para cada voxel


    def intersect_plane(self, origin, direction):

        origin = np.array(origin)
        direction = np.array(direction)

        intersections = []
        for axis in range(3):
            for side in [0, 1]:  # 0: min, 1: max
                if abs(direction[axis]) < 1e-10:
                    continue  # Paralelo, no intersecta
                if side == 0:
                    coord = self.min_corner[axis]
                    plane_id = 2 * axis     # xmin, ymin, zmin
                else:
                    coord = self.max_corner[axis]
                    plane_id = 2 * axis + 1  # xmax, ymax, zmax
                t = (coord - origin[axis]) / direction[axis]
                point = origin + t * direction
                print(f"t: {t},lay: {plane_id}, punto: {point}")


                if plane_id % 2 < self.epsilon:
                    if direction[axis] < 0:
                        if self.is_inside(point - self.epsilon * direction) and t > 0:
#                        print(f"Inside: {self.is_inside(point + self.epsilon * direction)}")
                            intersections.append((t, plane_id, point))
#                elif plane_id % 2 > self.epsilon:
                    elif direction[axis] > 0:
                        if self.is_inside(point + self.epsilon * direction) and t > 0:
#                        print(f"Inside: {self.is_inside(point + self.epsilon * direction)}")
                            intersections.append((t, plane_id, point))
                elif plane_id % 2 > self.epsilon:
                    if direction[axis] < 0:
                        if self.is_inside(point + self.epsilon * direction) and t > 0:
#                        print(f"Inside: {self.is_inside(point + self.epsilon * direction)}")
                            intersections.append((t, plane_id, point))
                    elif direction[axis] > 0:
                        if self.is_inside(point - self.epsilon * direction) and t > 0:
                            intersections.append((t, plane_id, point))


        intersections_sorted = sorted(intersections, key=lambda x: x[0])
        print(f"sorted: {intersections_sorted}")


        if not self.is_inside(origin):
            if len(intersections_sorted) == 0:
                return None, None
            elif len(intersections_sorted) == 1:
                return intersections_sorted[0], None
            elif len(intersections_sorted) == 2:
#                    print(f"\n cuts: {intersections_sorted[0], intersections_sorted[1]}")
                return intersections_sorted[0], intersections_sorted[1]
            else:
                if abs(intersections_sorted[0][0] - intersections_sorted[1][0]) < self.epsilon:
                    return intersections_sorted[0], intersections_sorted[2]
                else:
                    return intersections_sorted[0], intersections_sorted[1]

        else:
            if len(intersections_sorted) >= 2:
                if abs(intersections_sorted[1][0] - intersections_sorted[0][0]) < self.epsilon: #corta por la esquina
                    return intersections_sorted[0], intersections_sorted[2]
                else:
                    return intersections_sorted[0], intersections_sorted[1]
            elif len(intersections_sorted) == 1:
#                print(f"Intersections: {intersections_sorted[0]}")
                return intersections_sorted[0], None

            else:
                print(9)
                return None, None



    def voxel_change(self, i, j, k, param):
        if param == 0:
            i = i-1
        if param == 1:
            i = i+1
        if param == 2:
            j = j-1
        if param == 3:
            j = j+1
        if param == 4:
            k = k-1
        if param == 5:
            k = k+1

        return [i, j, k]


    def find_voxel(self, point):
        x, y, z = point

        i = int((x-self.min_corner[0])/self.size[0])
        j = int((y-self.min_corner[1])/self.size[1])
        k = int((z-self.min_corner[2])/self.size[2])
        return [i, j, k]


    def print(self):

        print(f'Voxel {self.i}, {self.j}, {self.k}')
        print(f'Position: {self.position}')
        print(f'Size: {self.size}')



    def add_energy_loss(self, deltaE, weight):
        self.total_energy_loss += deltaE * weight
        self.total_weight += weight
        self.n_tracks += 1


    def get_weighted_average_loss(self):
        if self.total_weight == 0:
            return 0.0
        E_weighted = self.total_energy_loss / self.n_tracks
#        print(E_weighted)
        return E_weighted

