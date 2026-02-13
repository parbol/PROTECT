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
        self.tmean = 0
        self.bx = 0
        self.by = 0
        self.bz = 0
        self.rmss = 0
        self.p = 0
        self.genID = 0
        self.genTrackID = 0
        self.hits = []
        self.det = 0
        self.isGen = False

    def insertHit(self, x, y, z, t, energy, genTrackID, genID, det):

        if len(self.hits) == 0:
            self.det = det
        hit = [x, y, z, t, energy, genTrackID, genID, det]
        self.hits.append(hit)

    def isGenTrack(self):

        if len(self.hits) == 0:
            return False
        gTr = self.hits[0][5] 
        gID = self.hits[0][6]
        for h in self.hits:
            if h[6] != 2212:
                return False
        for h in self.hits:
            if gTr != h[5]:
                return False
        return True

    def build(self):

        self.isGen = self.isGenTrack()
        x = y = z = t = 0.
        t2 = 0.
        xt = yt = zt = 0.

        for h in self.hits:
            x = x + h[0]
            xt = xt + h[0] * h[3]
            y = y + h[1]
            yt = yt + h[1] * h[3]
            z = z + h[2]
            zt = zt + h[2] * h[3]
            t = t + h[3]
            t2 = t2 + h[3]**2
        
        x = x/len(self.hits)
        xt = xt/len(self.hits)
        y = y/len(self.hits)
        yt = yt/len(self.hits)
        z = z/len(self.hits)
        zt = zt/len(self.hits)
        t = t/len(self.hits)
        t2 = t2/len(self.hits)
        
        deltat = t2 - t*t
        alphax = (xt - x * t) / deltat
        alphay = (yt - y * t) / deltat
        alphaz = (zt - z * t) / deltat
        
        self.x0 = x - alphax * t
        self.y0 = y - alphay * t
        self.z0 = z - alphaz * t
        self.t0 = 0
        self.bx = alphax / self.c
        self.by = alphay / self.c
        self.bz = alphaz / self.c
        self.tmean = t
        beta = math.sqrt(self.bx*self.bx+self.by*self.by+self.bz*self.bz)
        if beta >= 1.0:
            beta = -1
        else:
            gamma = 1.0/math.sqrt(1.0 - beta*beta)
            self.p = beta * gamma * self.mp
        xplus = yplus = zplus = 0.0
        for h in self.hits:
            xplus = xplus + (h[0]-self.x0-alphax*h[3])**2
            yplus = yplus + (h[1]-self.y0-alphay*h[3])**2
            zplus = zplus + (h[2]-self.z0-alphaz*h[3])**2
        self.rmss = math.sqrt((xplus+yplus+zplus)/len(self.hits))
        self.genID = self.hits[0][6]
        self.genTrackID = self.hits[0][5]

    def print(self):

        print('Track parameters: (' + str(self.x0) + ', ', str(self.y0) + ', ' + str(self.z0) + ') + (' + str(self.bx) + ', ' + str(self.by) + ', ' + str(self.bz) + ') * t')
        print('Hits:')
        for h in self.hits:
            print('x:', h[0], 'y:', h[1], 'z:', h[2], 't:', h[3])


