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

        layer1Complete = True
        for l in layers2:
            if len(l) == 0:
                return False
        for l in layers1:
            if len(l) == 0:
                layer1Complete = False
        
        if layer1Complete:
            tracks1 = self.runDetector(layers1, ev)
        tracks2 = self.runDetector(layers2, ev)
       
        self.track1 = Track() 
        for layer in bestTrack1:
            self.track1.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer])
        self.track2 = Track() 
        for layer in bestTrack2:
            self.track2.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer])
        self.track1.build()
        self.track2.build()

    
    def runDetector(self, layers, ev):
        
        #First we make all the possible tracks with chi2 smaller than a given threshold
        chi2threshold = 1.0
        theElement = (0)
        cartesian = itertools.product(*layers)
        for element in cartesian:
            t = Track()
            for layer in element:
                t.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer])
            t.build()
            if t.chi2 < chi2threshold:
                tracks.append(t)
        #We sort the list by chi2
        listOfHits = []
         
        return theElement


        


