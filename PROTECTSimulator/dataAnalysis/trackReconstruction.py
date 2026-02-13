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
    ngentracks = array('i', [0])
    nmatchedtracks = array('i', [0])
    x2 = array('f', NMax*[0]) 
    y2 = array('f', NMax*[0]) 
    z2 = array('f', NMax*[0]) 
    t2 = array('f', NMax*[0]) 
    vx2 = array('f', NMax*[0]) 
    vy2 = array('f', NMax*[0]) 
    vz2 = array('f', NMax*[0]) 
    p2 = array('f', NMax*[0]) 
    chi2s = array('f', NMax*[0]) 
    genID2 = array('i', NMax*[0])
 
    t.Branch('nevent', 'nevent', 'nevent/I') 
    t.Branch('ntracks', ntracks, 'ntracks/I') 
    t.Branch('ngentracks', ngentracks, 'ngentracks/I') 
    t.Branch('nmatchedtracks', nmatchedtracks, 'nmatchedtracks/I') 
    t.Branch('x2', x2, 'x2[ntracks]/F') 
    t.Branch('y2', y2, 'y2[ntracks]/F') 
    t.Branch('z2', z2, 'z2[ntracks]/F') 
    t.Branch('t2', t2, 't2[ntracks]/F') 
    t.Branch('vx2', vx2, 'vx2[ntracks]/F') 
    t.Branch('vy2', vy2, 'vy2[ntracks]/F') 
    t.Branch('vz2', vz2, 'vz2[ntracks]/F')
    t.Branch('p2', p2, 'p2[ntracks]/F')
    t.Branch('chi2s', chi2s, 'chi2s[ntracks]/F')
    t.Branch('genID2', genID2, 'genID2[ntracks]/I')

    for ev in input.events:

        tf = TrackFinder(ev, 4)
        if not tf.isValid:
            continue
       
        nevent[0] = ev.nevent
        ntracks[0] = len(tf.tracks2)
        ngentracks[0] = tf.genTracks2
        nmatchedtracks[0] = tf.matchedTracks2

        for i, tr in enumerate(tf.tracks2):
            x2[i] = tr.x0
            y2[i] = tr.y0
            z2[i] = tr.z0
            t2[i] = tr.t0
            vx2[i] = tr.bx
            vy2[i] = tr.by
            vz2[i] = tr.bz
            p2[i] = tr.p
            genID2[i] = tr.genID
            chi2s[i] = tr.rmss
        
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
        
    output.Write()
    output.Close()
    input.Close()


 



 


