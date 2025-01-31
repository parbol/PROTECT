import json, sys, optparse
import ROOT as r
from array import array
import sys
from tools.Event import Event
from tools.GeometryConversor import GeometryConversor


class EventLoader:

    def __init__(self, inputFile, configuration):
        self.inputFile = inputFile
        self.configuration = configuration
             
    def loadEvents(self):

        try:
            f = r.TFile(self.inputFile)
        except:
            print('Input file does not exist or it is corrupt')
            sys.exit()

        geomConversor = GeometryConversor(self.configuration)
   
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

        
        