import numpy as np
import itertools
from .ActiveVolume import ActiveVolume 


def time_at_z0(track):
    time = track.t0 + (-track.z0) / (track.bz)
    return time


def match_by_time(tracks1, tracks2):
    time_pairs = []
    used = set()
    max_dt = 0.5
    for t1 in tracks1:
        t1_time = time_at_z0(t1)
        best_t2 = None
        min_dt = float("inf")
        for i, t2 in enumerate(tracks2):
            if i in used:
                continue
            t2_time = time_at_z0(t2)
            dt = abs(t1_time - t2_time)
            if dt < min_dt and dt < max_dt:
                min_dt = dt
                best_t2 = i

        if best_t2 is not None:
            time_pairs.append((t1, tracks2[best_t2]))
            used.add(best_t2)
        print(f"best time for is {min_dt}")
    return time_pairs



def efficiency(pairs):
    correct = 0
    total = len(pairs)
    for t1, t2 in pairs:
        if hasattr(t1, 'genTrackID') and hasattr(t2, 'genTrackID'):
            if t1.genTrackID == t2.genTrackID:
                correct += 1
        print(f"Match genTrackID1 = {getattr(t1, 'genTrackID')}, genTrackID2 = {getattr(t2, 'genTrackID')}")
    return correct / total if total > 0 else 0


