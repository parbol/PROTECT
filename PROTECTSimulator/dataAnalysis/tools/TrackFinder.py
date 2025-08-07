from tools.Track import Track
import sys
import itertools

class TrackFinder:

    def __init__(self, ev, nlayers):

        self.isValid = True
        self.tracks1 = []
        self.tracks2 = []
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
        layer2Complete = True
        for l in layers2:
            if len(l) == 0:
                layer2Complete = False
                break
        for l in layers1:
            if len(l) == 0:
                layer1Complete = False
                break
        if not layer2Complete:
            self.isValid = False
        else:
            if layer1Complete:
                self.tracks1 = self.runDetector(layers1, ev)
            self.tracks2 = self.runDetector(layers2, ev)
            #self.makeAssociation(tracks1, tracks2)
        if len(self.tracks2) == 0:
            self.isValid = False

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
        rmssthreshold = 1.0 #cm
        rmstthreshold = 0.22 #ns
        theElement = (0)
        cartesian = itertools.product(*layers)
        for element in cartesian:
            t = Track()
            for layer in element:
                t.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer], ev.genTrackID[layer], ev.genID[layer])
            t.build()
            if not t.isGenTrack():
                continue
            if t.rmst < rmstthreshold and t.rmss < rmssthreshold:
                tracks.append(t)
        #We sort the list by chi2
        sortedTracks = sorted(tracks, key=lambda track: track.rmss)
        #Finally we remove tracks that are using hits that have been already used
        listOfHits = []
        finalTracks = []
        for i in range(0, len(sortedTracks)): 
            if self.addHitToList(listOfHits, sortedTracks[i]):
                finalTracks.append(sortedTracks[i])
        return finalTracks


        


