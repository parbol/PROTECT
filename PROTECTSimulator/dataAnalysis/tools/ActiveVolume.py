import numpy as np
from tools.Voxel import Voxel


class ActiveVolume:

    def __init__(self, position, size, n_voxels):
        self.position = np.array(position)  # Centro del volumen (x, y, z)
        self.size = np.array(size)          # Tamaño del volumen (Lx, Ly, Lz)
        self.n_voxels = np.array(n_voxels)  # Número de vóxeles (nx, ny, nz)

        # Cálculo del tamaño de cada vóxel
        self.voxel_size = self.size / self.n_voxels

        # Generar lista de vóxeles
        self.voxels = self._generate_voxel_grid()

        self.AVvoxel = Voxel(0, 0, 0, position = self.position, size = self.size)

        # Tracks más probables (índices de vóxeles)
        self.track1 = []
        self.track2 = []
        self.epsilon = 10e-6
        self.deltaE = 0

    def _generate_voxel_grid(self):
        x_centers = np.linspace(-self.size[0]/2 + self.voxel_size[0]/2, self.size[0]/2 - self.voxel_size[0]/2, self.n_voxels[0])
        y_centers = np.linspace(-self.size[1]/2 + self.voxel_size[1]/2, self.size[1]/2 - self.voxel_size[1]/2, self.n_voxels[1])
        z_centers = np.linspace(-self.size[2]/2 + self.voxel_size[2]/2, self.size[2]/2 - self.voxel_size[2]/2, self.n_voxels[2])

        voxels = []
        for i, x in enumerate(x_centers):
            voxelsi = []
            for j, y in enumerate(y_centers):
                voxelsj = []
                for k, z in enumerate(z_centers):
                    voxelsj.append(Voxel(i, j, k, position = [x, y, z], size = self.voxel_size))
                voxelsi.append(voxelsj)
            voxels.append(voxelsi)

        return voxels

    def find_voxel(self, point):
        x, y, z = point

        i = int((x-self.AVvoxel.min_corner[0])/self.voxel_size[0])
        j = int((y-self.AVvoxel.min_corner[1])/self.voxel_size[1])
        k = int((z-self.AVvoxel.min_corner[2])/self.voxel_size[2])
        return [i, j, k]


    def navigation(self, origin, direction):
        origin = origin
        print(f"origin: {origin}")
        direction = direction
        crossed_voxels = []
        i = 0
        enter, exit = self.AVvoxel.intersect_plane(origin, direction)
        if enter is None and exit is None:
            print("The track does not enter the AV")
            return [], None, None
        else:
            enter_point = np.array(enter[2])
            exit_point = np.array(exit[2])
            enter_inside = enter_point + self.epsilon * np.array(direction)
            print(f"Enter point: {enter_point}, exit point: {exit_point}")
            enterx, entery, enterz = self.find_voxel(enter_inside)
            print(f"enterx: {enterx}, entery: {entery}, enterz: {enterz}")
            enter_voxel = self.voxels[enterx][entery][enterz]
            print(f'Voxel de entrada {enterx} {entery} {enterz}')
            current_voxel = enter_voxel
            print(f"Punto de entrada: {enter_point}")
#        print(f"Is inside: {self.AVvoxel.is_inside(enter_point)}")

            while self.AVvoxel.is_inside(np.array(enter_point) + self.epsilon * np.array(direction)):
                i = i+1
                print()
                print(f"Iteration: {i}")
                print(f"Punto de entrada: {enter_point}")
                cut1, cut2 = current_voxel.intersect_plane(enter_inside, direction)
                print(f"intersections: {cut1}, {cut2}")
            #guardar los indice del current voxel
                crossed_voxels.append([enterx, entery, enterz])
                t, lay, next_cut = cut1
                print(f"Cut layer: {lay}")

                if cut2 is not None and abs(cut1[0] - cut2[0]) < self.epsilon:
                    #Corta un borde
                    next_voxel1 = current_voxel.voxel_change(enterx, entery, enterz, lay)
                    next_voxel = current_voxel.voxel_change(next_voxel1[0], next_voxel1[1], next_voxel1[2], cut2[1])
                else:
                    next_voxel = current_voxel.voxel_change(enterx, entery, enterz, lay)

                print(f'Next voxel is {next_voxel[0]} {next_voxel[1]} {next_voxel[2]}')
                enterx, entery, enterz = next_voxel
                enter_point = next_cut
                enter_inside = next_cut + self.epsilon * np.array(direction)
                try:
                    current_voxel =  self.voxels[next_voxel[0]][next_voxel[1]][next_voxel[2]]
                except IndexError:
                    print(f"Exit the loop") 
                    break

            print(crossed_voxels)
            print()
            print(f"exit point though navigation:{enter_point}, exit_point:{exit_point}")

            if np.all(abs(enter_point - exit_point) < self.epsilon):
                print(f"Both second intersection and navigation exit are the same! :D")
            else:
                print(f"Second intersection and navigation exit do not match")
                sys.exit(1)
            return crossed_voxels, enter_point, exit_point


    def print(self):

        print(f'Active volume position {self.position}')
        print(f'Active volume size {self.size}')
        print(f'Active volume number of voxels {self.n_voxels}')
        print('Starting voxel count')
        for i in range(0, self.n_voxels[0]):
            for j in range(0, self.n_voxels[1]):
                for k in range(0, self.n_voxels[2]):
                    print('-----printing voxel----')
                    self.voxels[i][j][k].print()
                    print('-----------------------')




    def deposit_energy(self, crossed_voxels, total_deltaE):
        Lt = len(crossed_voxels)
        if Lt == 0:
            return
        for voxel_index in crossed_voxels:
            Li = 1
            weight = Li/Lt
            i, j, k = voxel_index
            self.voxels[i][j][k].add_energy_loss(total_deltaE, weight)



    def print_energy_map(self):
        count = 0
        for i in range(self.n_voxels[0]):
            for j in range(self.n_voxels[1]):
                for k in range(self.n_voxels[2]):
                    voxel = self.voxels[i][j][k]
                    if voxel.n_tracks > 0:
                        count += 1
                        print(f'Voxel[{i},{j},{k}], E_avg = {voxel.get_weighted_average_loss()}, Tracks = {voxel.n_tracks}')
        print(f"Total active voxels with energy: {count}")









