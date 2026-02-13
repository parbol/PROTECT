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
from collections import Counter



def save_data(GenTracks, nRecoTracks0, nRecoTracks1, goodReco0, goodReco1, pairs, acc0, acc1, eff_reco0, eff_reco1, eff_pairs, file = "data.npz"):
    print(GenTracks, nRecoTracks0, nRecoTracks1, goodReco0, goodReco1, pairs, acc0, acc1, eff_reco0, eff_reco1, eff_pairs)
    if os.path.exists(file):
        old = np.load(file)
        list_GenTracks = old["GenTracks"].tolist()
        list_nRecoTracks0 = old["nRecoTracks0"].tolist()
        list_nRecoTracks1 = old["nRecoTracks1"].tolist()
        list_goodReco0 = old["goodReco0"].tolist()
        list_goodReco1 = old["goodReco1"].tolist()
        list_pairs = old["pairs"].tolist()
        list_acc0 = old["acc0"].tolist()
        list_acc1 = old["acc1"].tolist()
        list_eff_reco0 = old["eff_reco0"].tolist()
        list_eff_reco1 = old["eff_reco1"].tolist()
        list_eff_pairs = old["eff_pairs"].tolist()

    else:
        list_GenTracks = []
        list_nRecoTracks0 = []
        list_nRecoTracks1 = []
        list_goodReco0 = []
        list_goodReco1 = []
        list_pairs = []
        list_acc0 = []
        list_acc1 = []
        list_eff_reco0 = []
        list_eff_reco1 = []
        list_eff_pairs = []

    list_GenTracks.append(GenTracks)
    list_nRecoTracks0.append(nRecoTracks0)
    list_nRecoTracks1.append(nRecoTracks1)
    list_goodReco0.append(goodReco0)
    list_goodReco1.append(goodReco1)
    list_pairs.append(pairs)
    list_acc0.append(acc0)
    list_acc1.append(acc1)
    list_eff_reco0.append(eff_reco0)
    list_eff_reco1.append(eff_reco1)
    list_eff_pairs.append(eff_pairs)


    np.savez(file,
             GenTracks = list_GenTracks,
             nRecoTracks0 = list_nRecoTracks0,
             nRecoTracks1 = list_nRecoTracks1,
             goodReco0 = list_goodReco0,
             goodReco1 = list_goodReco1,
             pairs = list_pairs,
             acc0 = list_acc0,
             acc1 = list_acc1,
             eff_reco0 = list_eff_reco0,
             eff_reco1 = list_eff_reco1,
             eff_pairs = list_eff_pairs)


if __name__=='__main__':


    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    parser.add_option('-c', '--conf', action='store', type='string', dest='configurationFile', default='conf.json', help='Configuration file')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputFile', default='output.root', help='Output Directory')
    (opts, args) = parser.parse_args()


    av = ActiveVolume([0.0, 0.0, 0.0], [19.2, 19.2, 19.2], [50, 50, 50])
    eff = 0
    goodReco1 = 0
    goodReco2 = 0



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
        for i in range(n_entries):
            ev.GetEntry(i)

            if not hasattr(ev, "layer"):
                continue

            nlayers = 4
            tf = TrackFinder(ev, nlayers)
#            nRecoTracks1 += len(tf.tracks1)
#            nRecoTracks2 += len(tf.tracks2)

            for tr in tf.tracks1:
                gen_ids1 = []
                for h in tr.hits:
                    gen_id = h[5]
                    gen_ids1.append(gen_id)
                counts = Counter(gen_ids1)
                if any(count == 4 for count in counts.values()):
                    goodReco1 += 1
                nRecoTracks1 += 1

            for tr in tf.tracks2:
                gen_ids2 = []
                for h in tr.hits:
                    gen_id = h[5]
                    gen_ids2.append(gen_id)
                counts = Counter(gen_ids2)
                if any(count >= 4 for count in counts.values()):
                    goodReco2 += 1
                nRecoTracks2 += 1

#            print(goodReco1, goodReco2)

            #Track pairing
            print(f"Longitud tracks1: {len(tf.tracks1)},longitud tracks2: {len(tf.tracks2)}")
            pairs = tools.matching_tracks.match_by_time(tf.tracks1, tf.tracks2)
            print(f"Shot nº {i}")
            all_pairs.extend(pairs)
            pairing = len(all_pairs)

            if tf.nGenTracks < 16:
                nGenTracks += tf.nGenTracks

#        nReco = len(all_pairs)
        print("nRecoTrack", nRecoTracks1, nRecoTracks2)
        print("goodReco", goodReco1)
        print("goodReco",goodReco2)
        print("GenTracks", nGenTracks)
        print("pairing", pairing)
#Acceptancy: número de trazas reconstruidas / n de protones detectados
#Efficiency: número de trazas bien emparejadas / número de trazas reconstruidas

        eff1 = goodReco1/nRecoTracks1
        eff2 = goodReco2/nRecoTracks2
        if nGenTracks != 0:
            acc1 = nRecoTracks1/nGenTracks
            acc2 = nRecoTracks2/nGenTracks
            print('Acceptancy Detector 1:', acc1, '+/-', math.sqrt(acc1 * (1.0-acc1)/nGenTracks))
            print('Acceptancy Detector 2:', acc2, '+/-', math.sqrt(acc2 * (1.0-acc2)/nGenTracks))
        print('Efficiency of Reco Detector 1:', eff1, '+/-', math.sqrt(eff1 * (1.0-eff1)/nRecoTracks1))
        print('Efficiency of Reco Detector 2:', eff2, '+/-', math.sqrt(eff2 * (1.0-eff2)/nRecoTracks2))



        global_eff = tools.matching_tracks.efficiency(all_pairs)
        print(f"Efficiency matching by time in z = 0: {global_eff} +/- {math.sqrt(global_eff * (1.0 - global_eff) / len(all_pairs))}")

        save_data(nGenTracks, nRecoTracks1, nRecoTracks2, goodReco1, goodReco2, pairing, acc1, acc2, eff1, eff2, global_eff)
    """
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
