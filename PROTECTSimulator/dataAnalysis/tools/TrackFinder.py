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
        
        self.makeAssociation(tracks1, tracks2)
        return tracks1, tracks2


    def makeAssociation(self, tracks1, tracks2):

        thresholdScore = 1.0
        for i, tr in enumerate(tracks2):
            tr.associator = i
        if len(tracks1) != 0:
            for i, tr2 in enumerate(tracks2):
                for j, tr1 in enumerate(tracks1):
                    if i == j:
                        continue
                    score = self.compatibility(tr1, tr2)
                    if score > thresholdScore:
                        continue
                     

    def addHitToList(self, listOfHits, track):

        newhits = []
        for hit in track.hits:
            if hit not in listOfHits:
                newhits.append(hit)
            else:
                return False
        listOfHits.append(newhits)
        return True
    
    def runDetector(self, layers, ev):
        
        tracks = []
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
        sortedTracks = sorted(tracks, key=lambda track: track.chi2)
        #Finally we remove tracks that are using hits that have been already used
        listOfHits = []
        finalTracks = []
        for i in range(0, len(sortedTracks)): 
            if self.addHitToList(listOfHits, sortedTracks[i]):
                finalTracks.append(sortedTracks[i])
        return finalTracks


        


