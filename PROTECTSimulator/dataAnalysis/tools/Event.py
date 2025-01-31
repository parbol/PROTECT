import json, sys, optparse
import ROOT as r
from array import array

class Event:

    def __init__(self, nEvent, geomConversor):
        self.geomConversor = geomConversor
        self.nEvent = nEvent
        self.det = []
        self.layer = []
        self.layerabs = []
        self.lgad = []
        self.xpad = []
        self.ypad = []
        self.toaraw = []
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
        self.layerabs.append(det_ * 4 + layer_)
        self.lgad.append(lgad_)
        self.xpad.append(xpad_)
        self.ypad.append(ypad_)
        self.toaraw.append(toa_)
        self.tot.append(tot_)
        totv = tot_
        if tot_ > 3.0:
            totv = 3.0
        toa = toa_ - 6.29937e-01 + 4.49338e-01 * tot_ - 1.23671e-01 * tot_**2 + 1.58380e-02 * tot_*tot_*tot_

        self.toa.append(toa) 
        self.charge.append(charge_)
        self.genEnergy.append(genEnergy_)
        self.gentoa.append(gentoa_)
        self.localgenx.append(genx_)
        self.localgeny.append(geny_)
        self.localgenz.append(genz_)
        self.genID.append(genID_)
        x, y, z = self.geomConversor.toGlobalMeasurement(det_, layer_, lgad_, xpad_, ypad_)
        genx, geny, genz = self.geomConversor.toGlobal(det_, layer_, lgad_, xpad_, ypad_, genx_, geny_, genz_)
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        self.genx.append(genx)
        self.geny.append(geny)
        self.genz.append(genz)

    def nHits(self):

        return len(self.det)

