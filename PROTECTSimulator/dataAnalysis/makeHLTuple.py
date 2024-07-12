import json, sys, optparse
import ROOT as r
from array import array

class Event:

    def __init__(self, nEvent, geomConversor):
        self.geomConversor = geomConversor
        self.nEvent = nEvent
        self.det = []
        self.layer = []
        self.lgad = []
        self.xpad = []
        self.ypad = []
        self.toa = []
        self.tot = []
        self.gentoa = []
        self.genEnergy = []
        self.genID = []
        self.localgenx = []
        self.localgeny = []
        self.localgenz = []
        self.x = []
        self.y = []
        self.z = []
        self.genx = []
        self.geny = []
        self.genz = []
        self.charge = []

    def add(self, det_, layer_, lgad_, xpad_, ypad_, toa_, tot_, charge_, genEnergy_, gentoa_, genx_, geny_, genz_, genID_):
        
        self.det.append(det_)
        self.layer.append(layer_)
        self.lgad.append(lgad_)
        self.xpad.append(xpad_)
        self.ypad.append(ypad_)
        self.toa.append(toa_)
        self.tot.append(tot_)
        self.charge.append(charge_)
        self.genEnergy.append(genEnergy_)
        self.gentoa.append(gentoa_)
        self.localgenx.append(genx_)
        self.localgeny.append(geny_)
        self.localgenz.append(genz_)
        self.genID.append(genID_)
        x, y, z = self.geomConversor.toGlobal(det_, layer_, lgad_, xpad_, ypad_, 0.0, 0.0, 0.0)
        genx, geny, genz = self.geomConversor.toGlobal(det_, layer_, lgad_, xpad_, ypad_, genx_, geny_, genz_)
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        self.genx.append(genx)
        self.geny.append(geny)
        self.genz.append(genz)

    def nHits(self):

        return len(self.det)


class GeometryConversor:

    def __init__(self, name):
        
        try:
            with open(name, 'r') as cinput:
                self.data = json.load(cinput)
        except:
            print('Configuration file is not valid')
            sys.exit()
        cinput.close()

        
    def toGlobal(self, det, layer, lgad, xpad, ypad, x, y, z):

        #This method is still hardcoded for a vertical detector 
        xdet = self.data['Detectors'][det]['xPosDetector']        
        ydet = self.data['Detectors'][det]['yPosDetector']
        zdet = self.data['Detectors'][det]['zPosDetector']
        xlayer = self.data['Detectors'][det]['Layers'][layer]['xPosLayer']
        ylayer = self.data['Detectors'][det]['Layers'][layer]['yPosLayer']
        zlayer = self.data['Detectors'][det]['Layers'][layer]['zPosLayer']
        xlgad = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['xPosSensor']
        ylgad = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['yPosSensor']
        zlgad = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['zPosSensor']
        xborder = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['xborder']
        yborder = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['yborder']
        interpadx = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['interPadx']
        interpady = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['interPady']
        xsize = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['xSizeSensor']
        ysize = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['ySizeSensor']
        realx = x + xdet + xlayer + xlgad + xborder + xsize / 2.0 + xpad * (xsize + interpadx) 
        realy = y + ydet + ylayer + ylgad + yborder + ysize / 2.0 + ypad * (ysize + interpady)
        realz = z + zdet + zlayer + zlgad

        return realx, realy, realz 


def loadEvents(inputFile, configuration):

    try:
        f = r.TFile(inputFile)
    except:
        print('Input file does not exist or it is corrupt')
        sys.exit()

    geomConversor = GeometryConversor(configuration)
   
    events = []
    event = -1
    counter = -1

    for ev in f.hits:
        if event != ev.eventNumber:
            newEvent = Event(ev.eventNumber, geomConversor)
            newEvent.add(ev.det, ev.layer, ev.lgad, ev.xpad, ev.ypad, ev.toa, ev.tot, ev.charge, ev.genEnergy, ev.gentoa, ev.genx, ev.geny, ev.genz, ev.genID)
            events.append(newEvent)
            event = ev.eventNumber
            counter = counter + 1
        else:
            events[counter].add(ev.det, ev.layer, ev.lgad, ev.xpad, ev.ypad, ev.toa, ev.tot, ev.charge, ev.genEnergy, ev.gentoa, ev.genx, ev.geny, ev.genz, ev.genID)

    f.Close()
    return events


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

    events = loadEvents(opts.inputFile, opts.configurationFile)

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


    h = r.TH1F('h', '', 100, -1, 1)
    charge = r.TH1F('charge', '', 100, 0, 10)
    
    for ev in events:
        nhits[0] = len(ev.det)
        if nhits[0] > Nmax:
            print('Too long event')
            continue
        nevent[0] = ev.nEvent
        h.Fill(ev.toa[0]-ev.gentoa[0])
        charge.Fill(ev.charge[0])
        insert(det, ev.det, Nmax)
        insert(layer, ev.layer, Nmax)
        insert(lgad, ev.lgad, Nmax)
        insert(xpad, ev.xpad, Nmax)
        insert(ypad, ev.ypad, Nmax)
        insert(charge, ev.charge, Nmax)
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

    c = r.TCanvas('c','c')
    h.Draw()
    c.SaveAs("plot.png")
    c2 = r.TCanvas('c2','c2')
    charge.Draw()
    c2.SaveAs("charge.png")
    output.Write()
    output.Close()




   


