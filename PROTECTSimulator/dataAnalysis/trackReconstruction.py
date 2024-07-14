import json, sys, optparse
import ROOT as r
from array import array



class Track:

    def __init__(self):

        self.x0 = 0
        self.y0 = 0
        self.z0 = 0
        self.bx = 0
        self.by = 0
        self.bz = 0
        self.hits = []

    def insertHit(self, x, y, z, t):

        hit = [x, y, z, t]
        self.hits.append(hit)

    def build(self):

        t,x, y,z = 0.
        t2,x2,y2,z2 = 0.
        xt, yt, zt = 0.

        for h in self.hits:
            x = x + h[0]
            x2 = x2 + h[0]**2
            y = y + h[1]
            y2 = y2 + h[1]**2
            z = z + h[2]
            z2 = z2 + h[2]**2
            t = t + h[3]
            t2 = t2 + h[3]**2
            xt = xt + h[0]*h[3]
            yt = yt + h[1]*h[3]
            zt = zt + h[2]*h[3]

        x = x/len(self.hits)
        x2 = x2/len(self.hits)
        y = y/len(self.hits)
        y2 = y2/len(self.hits)
        z = z/len(self.hits)
        z2 = z2/len(self.hits)
        t = t/len(self.hits)
        t2 = t2/len(self.hits)
        xt = xt/len(self.hits)
        yt = yt/len(self.hits)
        zt = zt/len(self.hits)

        self.bx = (xt - x * t)/(t2-t*t)
        self.by = (yt - y * t)/(t2-t*t)
        self.bz = (zt - z * t)/(t2-t*t)
        self.x0 = x - self.bx*t
        self.y0 = y - self.by*t
        self.z0 = z - self.bz*t



class TrackFinder:

    def __init__(self, ev):

        layers1 = []
        layers2 = []
        for i in range(0, 4):
            layers1.append([])
            layers2.append([])
              
        for i in range(0, ev.nhits):
            if ev.det[i] == 0:
                layers1[ev.layer[i]].append(i)
            if ev.det[i] == 1:
                layers2[ev.layer[i]].append(i)

           
                
                




    





def correctNumberOfHits(ev):

    if ev.nhits < 8:
        return False
    seq = [0, 1, 2, 3, 4, 5, 6, 7]    
    counter = 0
    for i in range(0, ev.nhits):
        n = ev.det[i] * 4 + ev.layer[i]
        if n in seq:
            seq.remove(n)
            counter = counter + 1
    
    if counter == 8:
        return True
    return False



if __name__ == '__main__':

    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputFile', default='output.root', help='Output ROOT file')
    (opts, args) = parser.parse_args()

    try:
        input = r.TFile(opts.inputFile)
    except:
        print('Cannot open input file')
        sys.exit()


    try:
        output = r.TFile(opts.outputFile, 'RECREATE')
    except:
        print('Cannot open output file')
        sys.exit()


   
    for ev in input.events:

        if not correctNumberOfHits(ev):
            continue





        for i in range(0, ev.nhits):

   


