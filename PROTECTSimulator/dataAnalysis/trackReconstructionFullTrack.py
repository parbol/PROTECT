from tools.Track import Track
from tools.TrackFinder import TrackFinder
import math
import json, sys, optparse
import ROOT as r
from array import array




def reset(x, n):

    for i in range(0, n):
        x[i] = 0



if __name__ == '__main__':

    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputFile', default='output.root', help='Output ROOT file')
    (opts, args) = parser.parse_args()
    
    c = 29.9792458 #cm/ns 
    mp = 938.27208943 #MeV
    try:
        input = r.TFile(opts.inputFile)
    except:
        print('Cannot open input file')
        sys.exit()


    try:
        output = r.TFile(opts.outputFile, 'RECREATE')
    except:
        print('Cannot open output file')
        sys.exit()

    NMax = 10
    t = r.TTree('events', 'events') 
    nevent = array('i', [0]) 
    ntracks = array('i', [0])
    ntracks1 = array('i', [0])
    ngentracks1 = array('i', [0])
    nmatchedtracks1 = array('i', [0])
    ntracks2 = array('i', [0])
    ngentracks2 = array('i', [0])
    nmatchedtracks2 = array('i', [0])
    x1 = array('f', NMax*[0])
    y1 = array('f', NMax*[0])
    z1 = array('f', NMax*[0])
    t1 = array('f', NMax*[0])
    vx1 = array('f', NMax*[0])
    vy1 = array('f', NMax*[0])
    vz1 = array('f', NMax*[0])
    x2 = array('f', NMax*[0])
    y2 = array('f', NMax*[0])
    z2 = array('f', NMax*[0])
    t2 = array('f', NMax*[0])
    vx2 = array('f', NMax*[0])
    vy2 = array('f', NMax*[0])
    vz2 = array('f', NMax*[0])
    p1 = array('f', NMax*[0])
    p2 = array('f', NMax*[0])
    chi1s = array('f', NMax*[0])
    chi2s = array('f', NMax*[0])
    genID1 = array('i', NMax*[0])
    genID2 = array('i', NMax*[0])

    t.Branch('nevent', 'nevent', 'nevent/I')
    t.Branch('ntracks', ntracks, 'ntracks/I')
    t.Branch('ntracks1', ntracks1, 'ntracks1/I')
    t.Branch('ngentracks1', ngentracks1, 'ngentracks1/I')
    t.Branch('nmatchedtracks1', nmatchedtracks1, 'nmatchedtracks1/I')
    t.Branch('ntracks2', ntracks2, 'ntracks2/I')
    t.Branch('ngentracks2', ngentracks2, 'ngentracks2/I')
    t.Branch('nmatchedtracks2', nmatchedtracks2, 'nmatchedtracks2/I')
    t.Branch('x1', x1, 'x1[ntracks]/F') 
    t.Branch('y1', y1, 'y1[ntracks]/F') 
    t.Branch('z1', z1, 'z1[ntracks]/F') 
    t.Branch('t1', t1, 't1[ntracks]/F') 
    t.Branch('vx1', vx1, 'vx1[ntracks]/F') 
    t.Branch('vy1', vy1, 'vy1[ntracks]/F') 
    t.Branch('vz1', vz1, 'vz1[ntracks]/F')
    t.Branch('x2', x2, 'x2[ntracks]/F') 
    t.Branch('y2', y2, 'y2[ntracks]/F') 
    t.Branch('z2', z2, 'z2[ntracks]/F') 
    t.Branch('t2', t2, 't2[ntracks]/F') 
    t.Branch('vx2', vx2, 'vx2[ntracks]/F') 
    t.Branch('vy2', vy2, 'vy2[ntracks]/F') 
    t.Branch('vz2', vz2, 'vz2[ntracks]/F')
    t.Branch('p1', p1, 'p1[ntracks]/F')
    t.Branch('p2', p2, 'p2[ntracks]/F')
    t.Branch('chi1s', chi1s, 'chi1s[ntracks]/F')
    t.Branch('chi2s', chi2s, 'chi2s[ntracks]/F')
    t.Branch('genID1', genID1, 'genID1[ntracks]/I')
    t.Branch('genID2', genID2, 'genID2[ntracks]/I')

    for ev in input.events:
        tf = TrackFinder(ev, 4)
        if not tf.fullTrack:
            continue
        trackColl = tf.matchTracks()
        if len(trackColl) == 0:
            continue
        nevent[0] = ev.nevent
        ntracks[0] = len(trackColl)
        ntracks1[0] = len(tf.tracks1)
        ngentracks1[0] = tf.genTracks1
        nmatchedtracks1[0] = tf.matchedTracks1
        ntracks2[0] = len(tf.tracks2)
        ngentracks2[0] = tf.genTracks2
        nmatchedtracks2[0] = tf.matchedTracks2
        for i, tr in enumerate(trackColl):
            x2[i] = tr[1].x0
            y2[i] = tr[1].y0
            z2[i] = tr[1].z0
            t2[i] = tr[1].t0
            vx2[i] = tr[1].bx
            vy2[i] = tr[1].by
            vz2[i] = tr[1].bz
            p2[i] = tr[1].p
            genID2[i] = tr[1].genID
            chi2s[i] = tr[1].rmss
            x1[i] = tr[0].x0
            y1[i] = tr[0].y0
            z1[i] = tr[0].z0
            t1[i] = tr[0].t0
            vx1[i] = tr[0].bx
            vy1[i] = tr[0].by
            vz1[i] = tr[0].bz
            p1[i] = tr[0].p
            genID1[i] = tr[0].genID
            chi1s[i] = tr[0].rmss
        
        t.Fill()

        reset(x2, ntracks[0])
        reset(y2, ntracks[0])
        reset(z2, ntracks[0])
        reset(t2, ntracks[0])
        reset(vx2, ntracks[0])
        reset(vy2, ntracks[0])
        reset(vz2, ntracks[0])
        reset(p2, ntracks[0])
        reset(genID2, ntracks[0])
        reset(chi2s, ntracks[0])
        
        reset(x1, ntracks[0])
        reset(y1, ntracks[0])
        reset(z1, ntracks[0])
        reset(t1, ntracks[0])
        reset(vx1, ntracks[0])
        reset(vy1, ntracks[0])
        reset(vz1, ntracks[0])
        reset(p1, ntracks[0])
        reset(genID1, ntracks[0])
        reset(chi1s, ntracks[0])
    output.Write()
    output.Close()
    input.Close()


 



 


