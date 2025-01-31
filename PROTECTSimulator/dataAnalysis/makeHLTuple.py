import json, sys, optparse
import ROOT as r
from array import array
from tools.Event import Event
from tools.GeometryConversor import GeometryConversor
from tools.EventLoader import EventLoader



def insert(a, b, N):

    for i in range(0, N):
        if i < len(b):
            a[i] = b[i]
        else:
            a[i] = 0



if __name__ == '__main__':

    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    parser.add_option('-c', '--conf', action='store', type='string', dest='configurationFile', default='conf.json', help='Configuration file')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputFile', default='output.root', help='Output ROOT file')
    (opts, args) = parser.parse_args()
 
    loader = EventLoader(opts.inputFile, opts.configurationFile)
    events = loader.loadEvents()
    
    try:
        output = r.TFile(opts.outputFile, 'RECREATE')
    except:
        print('Cannot open output file')
        sys.exit()


    t = r.TTree('events', 'events')
    Nmax = 20 
    nhits = array('i', [0])
    nevent = array('i', [0])
    det = array('i', Nmax*[0])
    layer = array('i', Nmax*[0])
    lgad = array('i', Nmax*[0])
    xpad = array('i', Nmax*[0])
    ypad = array('i', Nmax*[0])
    toaraw = array('f', Nmax*[0])
    toa = array('f', Nmax*[0])
    tot = array('f', Nmax*[0])
    charge = array('f', Nmax*[0]) 
    genEnergy = array('f', Nmax*[0])
    gentoa = array('f', Nmax*[0])
    genID = array('i', Nmax*[0])
    x = array('f', Nmax*[0])
    y = array('f', Nmax*[0])
    z = array('f', Nmax*[0])
    genx = array('f', Nmax*[0])
    geny = array('f', Nmax*[0])
    genz = array('f', Nmax*[0])
    localgenx = array('f', Nmax*[0])
    localgeny = array('f', Nmax*[0])
    localgenz = array('f', Nmax*[0])

    t.Branch('nhits', nhits, 'nhits/I')
    t.Branch('nevent', 'nevent', 'nevent/I')
    t.Branch('det', det, 'det[nhits]/I')
    t.Branch('layer', layer, 'layer[nhits]/I')
    t.Branch('lgad', lgad, 'lgad[nhits]/I')
    t.Branch('xpad', xpad, 'xpad[nhits]/I')
    t.Branch('ypad', ypad, 'ypad[nhits]/I')
    t.Branch('toaraw', toaraw, 'toaraw[nhits]/F')
    t.Branch('toa', toa, 'toa[nhits]/F')
    t.Branch('tot', tot, 'tot[nhits]/F')
    t.Branch('charge', charge, 'charge[nhits]/F')
    t.Branch('genEnergy', genEnergy, 'genEnergy[nhits]/F')
    t.Branch('gentoa', gentoa, 'gentoa[nhits]/F')
    t.Branch('genID', genID, 'genID[nhits]/I')
    t.Branch('x', x, 'x[nhits]/F')
    t.Branch('y', y, 'y[nhits]/F')
    t.Branch('z', z, 'z[nhits]/F')
    t.Branch('genx', genx, 'genx[nhits]/F')
    t.Branch('geny', geny, 'geny[nhits]/F')
    t.Branch('genz', genz, 'genz[nhits]/F')
    t.Branch('localgenx', localgenx, 'localgenx[nhits]/F')
    t.Branch('localgeny', localgeny, 'localgeny[nhits]/F')
    t.Branch('localgenz', localgenz, 'localgenz[nhits]/F')

    
    for ev in events:
        nhits[0] = len(ev.det)
        if nhits[0] > Nmax:
            print('Too long event')
            continue
        nevent[0] = ev.nEvent
        insert(det, ev.det, Nmax)
        insert(layer, ev.layer, Nmax)
        insert(lgad, ev.lgad, Nmax)
        insert(xpad, ev.xpad, Nmax)
        insert(ypad, ev.ypad, Nmax)
        insert(charge, ev.charge, Nmax)
        insert(toaraw, ev.toaraw, Nmax)
        insert(toa, ev.toa, Nmax)
        insert(tot, ev.tot, Nmax)
        insert(genEnergy, ev.genEnergy, Nmax)
        insert(gentoa, ev.gentoa, Nmax)
        insert(genID, ev.genID, Nmax)
        insert(x, ev.x, Nmax)
        insert(y, ev.y, Nmax)
        insert(z, ev.z, Nmax)
        insert(genx, ev.genx, Nmax)
        insert(geny, ev.geny, Nmax)
        insert(genz, ev.genz, Nmax)
        insert(localgenx, ev.localgenx, Nmax)
        insert(localgeny, ev.localgeny, Nmax)
        insert(localgenz, ev.localgenz, Nmax)
        t.Fill()

    output.Write()
    output.Close()




   


