import ROOT as r
import itertools
from tools.Track import Track


class TrackFinder:

    def __init__(self, ev, nlayers):

        layers1 = []
        layers2 = []
        for i in range(0, nlayers):
            layers1.append([])
            layers2.append([])
              
        for i in range(0, ev.nhits):
            if ev.det[i] == 0:
                layers1[ev.layer[i]].append(i)
            if ev.det[i] == 1:
                layers2[ev.layer[i]].append(i)

        bestTrack1 = self.runDetector(layers1, ev)
        bestTrack2 = self.runDetector(layers2, ev)
        self.track1 = Track() 
        for layer in bestTrack1:
            self.track1.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer])
        self.track2 = Track() 
        for layer in bestTrack2:
            self.track2.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer])
        self.track1.build()
        self.track2.build()

    
    def runDetector(self, layers, ev):
       
        chi2Min = 1e20
        theElement = (0)
        cartesian = itertools.product(*layers)
        for element in cartesian:
            t = Track()
            for layer in element:
                t.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer])
            t.build()
            if t.chi2 < chi2Min:
                chi2Min = t.chi2
                theElement = element
        return theElement


        


