class Track:

    def __init__(self):

        self.x0 = 0
        self.y0 = 0
        self.z0 = 0
        self.bx = 0
        self.by = 0
        self.bz = 0
        self.chi2 = 0
        self.hits = []
        self.xt = 0
        self.yt = 0
        self.zt = 0
        self.t = 0
        self.t2 = 0

    def insertHit(self, x, y, z, t, energy):

        hit = [x, y, z, t, energy]
        self.hits.append(hit)

    def build(self):

        x = y = z = 0.
        x2 = y2 = z2 = 0.
        
        for h in self.hits:
            x = x + h[0]
            x2 = x2 + h[0]**2
            y = y + h[1]
            y2 = y2 + h[1]**2
            z = z + h[2]
            z2 = z2 + h[2]**2
            self.t = self.t + h[3]
            self.t2 = self.t2 + h[3]**2
            self.xt = self.xt + h[0]*h[3]
            self.yt = self.yt + h[1]*h[3]
            self.zt = self.zt + h[2]*h[3]
        x = x/len(self.hits)
        x2 = x2/len(self.hits)
        y = y/len(self.hits)
        y2 = y2/len(self.hits)
        z = z/len(self.hits)
        z2 = z2/len(self.hits)
        self.t = self.t/len(self.hits)
        self.t2 = self.t2/len(self.hits)
        self.xt = self.xt/len(self.hits)
        self.yt = self.yt/len(self.hits)
        self.zt = self.zt/len(self.hits)

        self.bx = (self.xt - x * self.t)/(self.t2-self.t*self.t)
        self.by = (self.yt - y * self.t)/(self.t2-self.t*self.t)
        self.bz = (self.zt - z * self.t)/(self.t2-self.t*self.t)
        self.x0 = x - self.bx*self.t
        self.y0 = y - self.by*self.t
        self.z0 = z - self.bz*self.t

        xplus = yplus = zplus = 0.0
        for h in self.hits:
            xplus = xplus + (h[0]-self.x0-self.bx*h[3])**2
            yplus = yplus + (h[1]-self.y0-self.by*h[3])**2
            zplus = zplus + (h[2]-self.z0-self.bz*h[3])**2
        self.chi2 = xplus+yplus+zplus    


    def print(self):

        print('Track parameters: (' + str(self.x0) + ', ', str(self.y0) + ', ' + str(self.z0) + ') + (' + str(self.bx) + ', ' + str(self.by) + ', ' + str(self.bz) + ') * t')
        print('Hits:')
        for h in self.hits:
            print('x:', h[0], 'y:', h[1], 'z:', h[2], 't:', h[3])


