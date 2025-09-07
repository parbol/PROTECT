from tools.Track import Track
import sys
import itertools

class TrackFinder:

    def __init__(self, ev, nlayers):

        
        self.nGenTracks = max(ev.genTrackID)
        self.isValid = True
        self.fullTrack = False
        self.tracks1 = []
        self.tracks2 = []
        self.genTracks1 = 0
        self.genTracks2 = 0
        self.matchedTracks1 = 0
        self.matchedTracks2 = 0
        self.genTracks2 = 0
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
        if layer1Complete:
            self.tracks1, self.genTracks1 = self.runDetector(layers1, ev)
            self.matchedTracks1 = 0
            for t in self.tracks1:
                if t.isGen:
                    self.matchedTracks1 += 1
        if layer2Complete:
            self.tracks2, self.genTracks2 = self.runDetector(layers2, ev)
            self.matchedTracks2 = 0
            for t in self.tracks2:
                if t.isGen:
                    self.matchedTracks2 += 1
        if len(self.tracks1) != 0 and len(self.tracks2) != 0:
            self.fullTrack = True
        if len(self.tracks2) == 0:
            self.isValid = False

    def deltaX(self, track1, track2):
          
        t = (track1.tmean + track2.tmean)/2.0
        x1 = track1.x0 + track1.bx * track1.c * t
        y1 = track1.y0 + track1.by * track1.c * t
        z1 = track1.z0 + track1.bz * track1.c * t
        x2 = track2.x0 + track2.bx * track2.c * t
        y2 = track2.y0 + track2.by * track2.c * t
        z2 = track2.z0 + track2.bz * track2.c * t

        deltax = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
        return deltax

    def matchTracks(self):

        max_dx = 5
        theElement = (0)
        tracks = [self.tracks1, self.tracks2]
        cartesian = itertools.product(*tracks)
        newlist = []
        for element in cartesian:
            
            dx = self.deltaX(element[0], element[1])
            if dx > max_dx:
                continue
            newlist.append([element[0], element[1], dx])
  
        sortedList = sorted(newlist, key=lambda element: element[2])
        usedTracks1 = set()
        usedTracks2 = set()
        finalList = []
        for tr in sortedList:
             if tr[0] in usedTracks1 or tr[1] in usedTracks2:
                 continue
             finalList.append([tr[0], tr[1]])
             usedTracks1.add(tr[0])
             usedTracks2.add(tr[1])
        return finalList


    def runDetector(self, layers, ev):

        tracks = []
        #First we make all the possible tracks with chi2 smaller than a given threshold
        rmssthreshold1 = 0.69 #cm  3-sigma
        rmssthreshold2 = 1.21 #cm  3-sigma
        theElement = (0)
        cartesian = itertools.product(*layers)
        genTracks = 0
        for element in cartesian:
            t = Track()
            for layer in element:
                t.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer], ev.genTrackID[layer], ev.genID[layer], ev.det[layer])
            t.build()
            if t.isGen:
                genTracks += 1
            rmssthreshold = 0
            if t.det == 0:
                rmssthreshold = rmssthreshold1
            else:
                rmssthreshold = rmssthreshold2
            if t.rmss < rmssthreshold:
                tracks.append(t)
        #We sort the list by chi2
        sortedTracks = sorted(tracks, key=lambda track: track.rmss)
        #Finally we remove tracks that are using hits that have been already used
        usedHits = set()
        finalTracks = []
        for tr in sortedTracks:
            hit_tuples = [tuple(hit) for hit in tr.hits]
            if any(hit in usedHits for hit in hit_tuples):
                continue

            finalTracks.append(tr)
            usedHits.update(hit_tuples)
        return finalTracks, genTracks




    def printHits(self, ev):

        print('---------------------List of hits------------------------')
#        for i, det in enumerate(ev.det):
#            print('det:', ev.det[i], 'layer:', ev.layer[i], 'x:', ev.x[i], 'y:', ev.y[i], 'z:', ev.z[i], 't:', ev.toa[i], 'genTrack:', ev.genTrackID[i], 'genID:', ev.genID[i])

