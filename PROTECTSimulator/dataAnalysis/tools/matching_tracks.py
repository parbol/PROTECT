import numpy as np
import itertools
from .ActiveVolume import ActiveVolume 


def time_at_z0(track):
    time = track.t0 + (-track.z0) / (track.bz)
    return time


def match_by_time(tracks1, tracks2):
    
    max_dt = 1.5
    
    theElement = (0)
    tracks = [tracks1, tracks2]
    cartesian = itertools.product(*tracks)
    newlist = []
    print('===============================')
    for element in cartesian:
        t1 = time_at_z0(element[0])
        t2 = time_at_z0(element[1])
        print('Det1:', element[0].genTrackID, 'Det2:', element[1].genTrackID, 'DT:', abs(t1-t2)) 
        print('Track 1 hits')
        for h in element[0].hits:
            print(h[5])
        print('Track 2 hits')
        for h in element[1].hits:
            print(h[5])

        if abs(t1-t2) > max_dt:
            continue
        if not element[0].isGenTrack() or not element[1].isGenTrack():
            continue
        newlist.append([element[0], element[1], abs(t1-t2)])
    sortedList = sorted(newlist, key=lambda element: element[2])
    usedTracks1 = set()
    usedTracks2 = set()
    finalList = []
    for tr in sortedList:
        if tr[0] in usedTracks1 or tr[1] in usedTracks2:
            continue
        print('Det 1 gen track id', tr[0].genTrackID, 'matches Det 2 gen track id', tr[1].genTrackID, 'Time', tr[2])
        finalList.append([tr[0], tr[1]])
        usedTracks1.add(tr[0])
        usedTracks2.add(tr[1])

    return finalList


def efficiency(pairs):
    correct = 0
    total = len(pairs)
    for t1, t2 in pairs:
        if hasattr(t1, 'genTrackID') and hasattr(t2, 'genTrackID'):
            if t1.genTrackID == t2.genTrackID:
                correct += 1
#        print(f"Match genTrackID1 = {getattr(t1, 'genTrackID')}, genTrackID2 = {getattr(t2, 'genTrackID')}")
    return correct / total if total > 0 else 0


