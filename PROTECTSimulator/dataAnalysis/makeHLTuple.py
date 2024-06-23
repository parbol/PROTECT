import json, sys, optparse
import ROOT as r


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
        self.gentot = []
        self.getEnergy = []
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

    def add(self, det_, layer_, lgad_, xpad_, ypad_, toa_, tot_, charge_, genEnergy_, gentoa_, gentot_, genx_, geny_, genz_, genID_)
        
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
        self.gentot.append(gentot_)
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
            newEvent.add(ev.det, ev.layer, ev.lgad, ev.xpad, ev.ypad, ev.toa, ev.tot, ev.charge, ev.genEnergy, ev.gentoa, ev.gentot, ev.genx, ev.geny, ev.genz, ev.genID)
            events.append(newEvent)
            event = ev.eventNumber
            counter = counter + 1

        else:
            events[counter].add(ev.det, ev.layer, ev.lgad, ev.xpad, ev.ypad, ev.toa, ev.tot, ev.charge, ev.genEnergy, ev.gentoa, ev.gentot, ev.genx, ev.geny, ev.genz, ev.genID)
           
    f.Close()



if __name__ == '__main__':

    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    parser.add_option('-c', '--conf', action='store', type='string', dest='configurationFile', default='conf.json', help='Configuration file')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputFile', default='output.root', help='Output ROOT file')
    (opts, args) = parser.parse_args()

    events = loadEvents(opts.inputFile, opts.configurationFile)
    
    h = r.TH1F("h", "Number of hits", 12, 0, 6)
    i = r.TH1F("i", "Detector numbers", 4, 0,2)
    layerh = r.TH1F("layerh", "Layer numbers",8 , 0, 4)
    lgadh = r.TH1F("lgadh", "lgad numbers",2 , 0, 1)
    xpadh = r.TH1F("xpadh", "xpad numbers", 40, 0, 20)
    ypadh = r.TH1F("ypadh", "ypad numbers", 40, 0, 20)
    toah = r.TH1F("toah", "time of arrival", 5, 0, 2)
    toth = r.TH1F("toth", "tot", 10, -2, 0)
    chargeh = r.TH1F("chargeh", "charge values", 100, 0, 4)



    for ev in events:
        h.Fill(ev.nHits())
    for  j in detector:
        i.Fill(j)
    for j in layer:
        layerh.Fill(j)
    for j in lgad:
        lgadh.Fill(j)
    for j in xpad:
        xpadh.Fill(j)
    for j in ypad:
        ypadh.Fill(j)
    for j in  toa:
        toah.Fill(j)
    for j in tot:
        toth.Fill(j)
    for j in charge:
        chargeh.Fill(j)


    """
    hcan = r.TCanvas('hcan')
    hcan.SetLogy(1)
    h.GetXaxis().SetTitle('N. hits')
    h.GetYaxis().SetRangeUser(0.1, 1e5)
    h.SetStats(0)
    h.Draw()
    hcan.SaveAs("Nhits_ShortPlus.png")
    """
    """
    ican = r.TCanvas('ican')
    ican.SetLogy(1)
    i.GetXaxis().SetTitle('Det. number')
    i.GetYaxis().SetRangeUser(1, 1e8)
    i.SetStats(0)
    i.Draw()
    ican.SaveAs("Hitsdet.png")

    layerhcan = r.TCanvas('layerhcan')
    layerhcan.SetLogy(1)
    layerh.GetXaxis().SetTitle('Layer number')
    layerh.GetYaxis().SetRangeUser(1, 1e8)
    layerh.SetStats(0)
    layerh.Draw()
    layerhcan.SaveAs("Hitslayer.png")

    lgadhcan = r.TCanvas('lgadhcan')
    lgadhcan.SetLogy(1)
    lgadh.GetXaxis().SetTitle('Lgad number')
    lgadh.GetYaxis().SetRangeUser(1, 1e8)
    lgadh.SetStats(0)
    lgadh.Draw()
    lgadhcan.SaveAs("Hitslgad.png")

    xpadhcan = r.TCanvas('xpadhcan')
    xpadhcan.SetLogy(1)
    xpadh.GetXaxis().SetTitle('Xpad number')
    xpadh.GetYaxis().SetRangeUser(1, 1e8)
    xpadh.SetStats(0)
    xpadh.Draw()
    xpadhcan.SaveAs("Hitsxpad.png")

    ypadhcan = r.TCanvas('ypadhcan')
    ypadhcan.SetLogy(1)
    ypadh.GetXaxis().SetTitle('Ypad number')
    ypadh.GetYaxis().SetRangeUser(1, 1e8)
    ypadh.SetStats(0)
    ypadh.Draw()
    ypadhcan.SaveAs("Hitsypad.png")
    """
    toahcan = r.TCanvas('toahcan')
    toahcan.SetLogy(0)
    toah.GetXaxis().SetTitle('TOA')
    toah.GetYaxis().SetRangeUser(0,1e4)
    toah.SetStats(0)
    toah.Draw()
    toahcan.SaveAs("Hitstoa.png")

    tothcan = r.TCanvas('tothcan')
    tothcan.SetLogy(0)
    toth.GetXaxis().SetTitle('TOT')
    toth.GetYaxis().SetRangeUser(0,1e4)
    toth.SetStats(0)
    toth.Draw()
    tothcan.SaveAs("Hitstot.png")

    chargehcan = r.TCanvas('chargehcan')
    chargehcan.SetLogy(0)
    chargeh.GetXaxis().SetTitle('CHARGE')
    chargeh.GetYaxis().SetRangeUser(0,2500)
    chargeh.SetStats(0)
    chargeh.Draw()
    chargehcan.SaveAs("Hitscharge.png")





