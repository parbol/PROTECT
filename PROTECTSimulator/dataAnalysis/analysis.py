import ROOT as r


class Event:

    def __init__(self, nEvent):
        self.nEvent = nEvent
        self.det = []
        self.layer = []
        self.lgad = []
        self.xpad = []
        self.ypad = []
        self.toa = []
        self.tot = []
        self.charge = []

    def add(self, det_, layer_, lgad_, xpad_, ypad_, toa_, tot_, charge_):
        self.det.append(det_)
        self.layer.append(layer_)
        self.lgad.append(lgad_)
        self.xpad.append(xpad_)
        self.ypad.append(ypad_)
        self.toa.append(toa_)
        self.tot.append(tot_)
        self.charge.append(charge_)

    def nHits(self):

        return len(self.det)

if __name__=='__main__':

    f = r.TFile('output_0.5m.root')
    
    
    events = []
    event = -1
    counter = -1
    detector = []
    layer = []
    lgad = []
    xpad = []
    ypad = []
    toa = []
    tot = []
    charge = []

    for ev in f.hits:
        if event != ev.eventNumber:
            newEvent = Event(ev.eventNumber)
            newEvent.add(ev.det, ev.layer, ev.lgad, ev.xpad, ev.ypad, ev.toa, ev.tot, ev.charge)
            events.append(newEvent)
            event = ev.eventNumber
            counter = counter + 1
            detector.append(ev.det)
            layer.append(ev.layer)
            lgad.append(ev.lgad)
            xpad.append(ev.xpad)
            ypad.append(ev.ypad)
            toa.append(ev.toa)
            tot.append(ev.tot)
            charge.append(ev.charge)

        else:
            events[counter].add(ev.det, ev.layer, ev.lgad, ev.xpad, ev.ypad, ev.toa, ev.tot, ev.charge)
            detector.append(ev.det)
            layer.append(ev.layer)
            lgad.append(ev.lgad)
            xpad.append(ev.xpad)
            ypad.append(ev.ypad)
            toa.append(ev.toa)
            tot.append(ev.tot)
            charge.append(ev.charge)
    f.Close()

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





