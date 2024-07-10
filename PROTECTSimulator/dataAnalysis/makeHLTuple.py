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

    def add(self, det_, layer_, lgad_, xpad_, ypad_, toa_, tot_, charge_, genEnergy_, gentoa_, genx_, geny_, genz_, genID_)
        
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
        x, y, z = self.geomConversor(det_, layer_, lgad_, xpad_, ypad_, 0.0, 0.0, 0.0)
        genx, geny, genz = self.geomConversor(det_, layer_, lgad_, xpad_, ypad_, genx_, geny_, genz_)
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
            with open(configuration, 'r') as cinput:
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
        xlgad = self.data['Detectors'][det]['Layers'][layer]['Sensors']['xPosSensor']
        ylgad = self.data['Detectors'][det]['Layers'][layer]['Sensors']['yPosSensor']
        zlgad = self.data['Detectors'][det]['Layers'][layer]['Sensors']['zPosSensor']
        xborder = self.data['Detectors'][det]['Layers'][layer]['Sensors']['xborder']
        yborder = self.data['Detectors'][det]['Layers'][layer]['Sensors']['yborder']
        interpadx = self.data['Detectors'][det]['Layers'][layer]['Sensors']['interPadx']
        interpady = self.data['Detectors'][det]['Layers'][layer]['Sensors']['interPady']
        xsize = self.data['Detectors'][det]['Layers'][layer]['Sensors']['xSizeSensor']
        ysize = self.data['Detectors'][det]['Layers'][layer]['Sensors']['ySizeSensor']

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



if __name__ == '__main__':

    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    parser.add_option('-c', '--conf', action='store', type='string', dest='configurationFile', default='conf.json', help='Configuration file')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputFile', default='output.root', help='Output ROOT file')
    (opts, args) = parser.parse_args()

    events = loadEvents(opts.inputFile, opts.configurationFile)
    

   


