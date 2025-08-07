import math

class Track:

    def __init__(self):

        self.c = 29.9792458 #cm/ns 
        self.mp = 938.27208943 #MeV
        self.et = 0.035 #ns
        self.es = 0.038
        self.x0 = 0
        self.y0 = 0
        self.z0 = 0
        self.t0 = 0
        self.bx = 0
        self.by = 0
        self.bz = 0
        self.rmss = 0
        self.rmst = 0
        self.p = 0
        self.genID = 0
        self.hits = []

    def insertHit(self, x, y, z, t, energy, genTrackID, genID):

        hit = [x, y, z, t, energy, genTrackID, genID]
        self.hits.append(hit)

    def isGenTrack(self):

        if len(self.hits) == 0:
            return False
        gTr = self.hits[0][5] 
        gID = self.hits[0][6]
        if gID != 2212:
            return False
        for h in self.hits:
            if gTr != h[5]:
                return False
        return True

    def build(self):

        x = y = z = t = 0.
        z2 = 0.
        xz = yz = tz = 0.
        
        for h in self.hits:
            x = x + h[0]
            xz = xz + h[0] * h[2]
            y = y + h[1]
            yz = yz + h[1] * h[2]
            t = t + h[3]
            tz = tz + h[3] * h[2]
            z = z + h[2]
            z2 = z2 + h[2]**2
        x = x/len(self.hits)
        xz = xz/len(self.hits)
        y = y/len(self.hits)
        yz = yz/len(self.hits)
        t = t/len(self.hits)
        tz = tz/len(self.hits)
        z = z/len(self.hits)
        z2 = z2/len(self.hits)
        deltaz = z2 - z*z
        alphax = (xz - x * z) / deltaz
        alphay = (yz - y * z) / deltaz
        alphat = (tz - t * z) / deltaz
        
        self.x0 = x - alphax * z
        self.y0 = y - alphay * z
        self.t0 = t - alphat * z
        self.z0 = 0.0
        self.bx = (alphax/alphat) / self.c
        self.by = (alphay/alphat) / self.c
        self.bz = (1.0/alphat) / self.c
        beta = math.sqrt(self.bx*self.bx+self.by*self.by+self.bz*self.bz)
        if beta >= 1.0:
            beta = -1
        else:
            gamma = 1.0/math.sqrt(1.0 - beta*beta)
            self.p = beta * gamma * self.mp
        xplus = yplus = tplus = 0.0
        for h in self.hits:
            xplus = xplus + (h[0]-self.x0-alphax*h[2])**2
            yplus = yplus + (h[1]-self.y0-alphay*h[2])**2
            tplus = tplus + (h[3]-self.t0-alphat*h[2])**2
        self.rmss = math.sqrt((xplus+yplus)/len(self.hits))
        self.rmst = math.sqrt(tplus/len(self.hits))
        self.genID = self.hits[0][6]

    def print(self):

        print('Track parameters: (' + str(self.x0) + ', ', str(self.y0) + ', ' + str(self.z0) + ') + (' + str(self.bx) + ', ' + str(self.by) + ', ' + str(self.bz) + ') * t')
        print('Hits:')
        for h in self.hits:
            print('x:', h[0], 'y:', h[1], 'z:', h[2], 't:', h[3])


