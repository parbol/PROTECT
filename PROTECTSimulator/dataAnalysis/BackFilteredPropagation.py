from tools.ActiveVolume import ActiveVolume
from tools.TrackFinder import TrackFinder
from tools.Track import Track
import tools.matching_tracks
import ROOT as r
import numpy as np
import subprocess
import os


def unit_vector(p0, p1):
    direction = p1 - p0
    norm = np.linalg.norm(direction)
    if norm == 0:
        return direction
    return direction / norm


if __name__=='__main__':

#    av = ActiveVolume([-9.6, -9.6, -9.6], [9.6, 9.6, 9.6], [10, 10, 10])
    av = ActiveVolume([0.0, 0.0, 0.0], [19.2, 19.2, 19.2], [50, 50, 50])
    eff = 0

    root_files = ["output_20_evs.root"]
    N_events = 0
    eff_total = 0


    for rootfile in root_files:
        if not os.path.exists("output_20_evs.root"):
            newroot = subprocess.run([
                "python3", "makeHLTuple.py",
                "-i", rootfile,
                "-c", "../test/test.json",
                "-o", "output_20_evs.root"])

        rootfile = "output_20_evs.root"
        f = r.TFile(rootfile)
        ev = f.Get("events")
        n_entries = ev.GetEntries()
        print(f"Archivo root: {rootfile}, entrada: {n_entries}")

        all_pairs = []

        for i in range(n_entries):
            ev.GetEntry(i)

            if not hasattr(ev, "layer"):
                continue

            nlayers = 4
            tf = TrackFinder(ev, nlayers)

            #Track pairing
            print(f"Longitud tracks1: {len(tf.tracks1)},longitud tracks2: {len(tf.tracks2)}")
            pairs = tools.matching_tracks.match_by_time(tf.tracks1, tf.tracks2)
            print(f"Track nº {i}")
            all_pairs.extend(pairs)


    """
        global_eff = tools.matching_tracks.efficiency(all_pairs)
        print(f"Efficiency matching by time in z = 0: {global_eff:.2f}")

        N_events = len(all_pairs)

        for i, track in enumerate(all_pairs):
            print(f"\ntraza n:{i}")
            #Energy loss and density
            p0 = np.array([track[0].hits[-1][0], track[0].hits[-1][1], track[0].hits[-1][2]])
            v0 = np.array([track[0].bx, track[0].by, track[0].bz])
            print(f"punto inicial {p0}, vector {v0}")
            crossed_voxels, entry, exit = av.navigation(p0, v0)
            if entry is not None:
                print(f"todo bien")
#                deltaE = getattr(track, "energy", 0.0)
                E1 = track[0].hits[-1][3]
                E2 = track[1].hits[0][3]
                deltaE = E2 - E1
                print(f"Diferencia de energía del track: {deltaE}")
                print(f"\n")
                av.deposit_energy(crossed_voxels, deltaE)

            else:
                continue

        eff += global_eff

    av.print_energy_map()
    print(f"Total efficiency of the system: {eff}")


    """
