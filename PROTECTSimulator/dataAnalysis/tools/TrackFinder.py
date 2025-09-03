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
            self.tracks1 = self.runDetector(layers1, ev)
        if layer2Complete:
            self.tracks2 = self.runDetector(layers2, ev)
        if len(self.tracks1) != 0 and len(self.tracks2) != 0:
            self.fullTrack = True
        if len(self.tracks2) == 0:
            self.isValid = False


    def time_at_z0(self, track):
          
        time = track.t0 + (-track.z0) / (track.bz)
        return time

    def match_by_time(self):

        max_dt = 1.5
        theElement = (0)
        tracks = [self.tracks1, self.tracks2]
        cartesian = itertools.product(*tracks)
        newlist = []
        for element in cartesian:
            t1 = self.time_at_z0(element[0])
            t2 = self.time_at_z0(element[1])

            if abs(t1-t2) > max_dt:
                continue
      
            newlist.append([element[0], element[1], abs(t1-t2)])
  
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
        rmssthreshold = 1.0 #cm
        rmstthreshold = 0.22 #ns
        theElement = (0)
        cartesian = itertools.product(*layers)
        for element in cartesian:
            t = Track()
            for layer in element:
                t.insertHit(ev.x[layer], ev.y[layer], ev.z[layer], ev.toa[layer], ev.genEnergy[layer], ev.genTrackID[layer], ev.genID[layer])
            t.build()
            if t.rmst < rmstthreshold and t.rmss < rmssthreshold:
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

        return finalTracks




    def printHits(self, ev):

        print('---------------------List of hits------------------------')
#        for i, det in enumerate(ev.det):
#            print('det:', ev.det[i], 'layer:', ev.layer[i], 'x:', ev.x[i], 'y:', ev.y[i], 'z:', ev.z[i], 't:', ev.toa[i], 'genTrack:', ev.genTrackID[i], 'genID:', ev.genID[i])

