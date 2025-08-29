from tools.ActiveVolume import ActiveVolume
from tools.TrackFinder import TrackFinder
from tools.Track import Track
import tools.matching_tracks
import ROOT as r
import numpy as np
import subprocess
import os
import optparse
import math


def unit_vector(p0, p1):
    direction = p1 - p0
    norm = np.linalg.norm(direction)
    if norm == 0:
        return direction
    return direction / norm


if __name__=='__main__':


    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    parser.add_option('-c', '--conf', action='store', type='string', dest='configurationFile', default='conf.json', help='Configuration file')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputFile', default='output.root', help='Output Directory')
    (opts, args) = parser.parse_args()


#    av = ActiveVolume([-9.6, -9.6, -9.6], [9.6, 9.6, 9.6], [10, 10, 10])
    av = ActiveVolume([0.0, 0.0, 0.0], [19.2, 19.2, 19.2], [50, 50, 50])
    eff = 0

    root_files = [f'{opts.outputFile}/RAW/{opts.inputFile}']
    N_events = 0
    eff_total = 0


    for rootfile in root_files:
        if not os.path.exists(f'{opts.outputFile}/HLT/{opts.inputFile}'):
            newroot = subprocess.run([
                "python3", "makeHLTuple.py",
                "-i", rootfile,
                "-c", opts.configurationFile,
                "-o", f'{opts.outputFile}/HLT/{opts.inputFile}'])
       
        rootfile = f'{opts.outputFile}/HLT/{opts.inputFile}'
        f = r.TFile(rootfile)
        ev = f.Get("events")
        n_entries = ev.GetEntries()
        print(f"Archivo root: {rootfile}, entrada: {n_entries}")

        nRecoTracks1 = 0
        nRecoTracks2 = 0
        nGenTracks = 0
        all_pairs = []
        n_entries = 1000
        for i in range(n_entries):
            ev.GetEntry(i)

            if not hasattr(ev, "layer"):
                continue

            nlayers = 4
            tf = TrackFinder(ev, nlayers)
            nRecoTracks1 += len(tf.tracks1)
            nRecoTracks2 += len(tf.tracks2)
            nGenTracks += tf.nGenTracks
            #Track pairing
            print(f"Longitud tracks1: {len(tf.tracks1)},longitud tracks2: {len(tf.tracks2)}")
            pairs = tools.matching_tracks.match_by_time(tf.tracks1, tf.tracks2)
            print(f"Track nº {i}")
            all_pairs.extend(pairs)


        if nGenTracks != 0:
            eff1 = nRecoTracks1/nGenTracks
            eff2 = nRecoTracks2/nGenTracks
            print('Efficiency Detector 1:', eff1)
            print('Efficiency Detector 2:', eff2)
            print('Efficiency Detector 1:', eff1, '+/-', math.sqrt(eff1 * (1.0-eff1)/nGenTracks))
            print('Efficiency Detector 2:', eff2, '+/-', math.sqrt(eff2 * (1.0-eff2)/nGenTracks))


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
