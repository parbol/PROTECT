import json, sys, os, optparse
import ROOT as r
from tools.Event import Event
from tools.GeometryConversor import GeometryConversor
from tools.EventLoader import EventLoader



def makePlots1D(plots, dir):

    for name, tup in plots.items():
       
        h = tup[0]
        xlabel = tup[1]
        ymin = tup[2]
        ymax = tup[3]
        poption = tup[4]

        canvasName = name + '_can'
        fileName = dir + '/' + name + '.png'
        can = r.TCanvas(canvasName)
        h.GetXaxis().SetTitle(xlabel)
        if ymin != ymax:
            h.GetXaxis().SetRangeUser(ymin, ymax)
        h.Draw(poption)
        can.SaveAs(fileName)


if __name__=='__main__':
  
    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    parser.add_option('-c', '--conf', action='store', type='string', dest='configurationFile', default='conf.json', help='Configuration file')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputDir', default='output.root', help='Output directory')
    (opts, args) = parser.parse_args()


    if os.path.isdir(opts.outputDir):
        print('Output directory is not empty')
        sys.exit()
    else:
        os.mkdir(opts.outputDir)

    ##################################################
    ###############Definition of plots################
    ################################################## 

    plots1D = dict()
    nhits = r.TH1F("nhits", "Number of hits", 40,  0, 40)
    plots1D['nhits'] = (nhits, 'N. Hits', 0, 0, '')

    detectorN = r.TH1F("detectorN", "Detector number", 4, 0, 2)
    plots1D['detectorN'] = (detectorN, 'Det. Number', 0, 0, '')

    layerN = r.TH1F("layerN", "Layer number", 9 , 0, 9)
    plots1D['layerN'] = (layerN, 'Layer Number', 0, 0, '')

    toa = r.TH1F("toa", "Time of Arrival", 200, -20, 50)
    plots1D['toa'] = (toa, 'ToA [ns]', 0, 0, '')

    tot = r.TH1F("tot", "Time over threshold", 200, -20, 50)
    plots1D['tot'] = (tot, 'ToT [ns]', 0, 0, '')

    charge = r.TH1F("charge", "Charge deposition", 200, -20, 50)
    plots1D['charge'] = (charge, 'charge [fC]', 0, 0, '')
    
    genEnergy = r.TH1F("genEnergy", "Energy of particle", 10000, 948, 962)
    plots1D['genEnergy'] = (genEnergy, 'energy [MeV]', 0, 0, '')
      
    #layerOccupancy = r.TH1F("layerOccupancy", "Layer occupancy", 9, 0, 9 )
    #plots1D['layerOccupancy'] = (layerOccupancy, "Layer occupancy", 0, 0, '')
    
    timeResolution = r.TH1F("timeResolution", "Time Resolution", 200, -0.3, 0.3)
    plots1D['timeResolution'] = (timeResolution, "Time Resolution [ns]", 0, 0, '')


    ##################################################
    ##################Start looping###################
    ################################################## 
    loader = EventLoader(opts.inputFile, opts.configurationFile)
    events = loader.loadEvents()

    for ev in events:
        plots1D['nhits'][0].Fill(ev.nHits())
        for i in range(0, len(ev.det)):
            plots1D['detectorN'][0].Fill(ev.det[i])
            plots1D['layerN'][0].Fill(ev.layer[i]) 
            plots1D['toa'][0].Fill(ev.toa[i])
            plots1D['tot'][0].Fill(ev.tot[i]) 
            plots1D['charge'][0].Fill(ev.charge[i]) 
            plots1D['genEnergy'][0].Fill(ev.genEnergy[i]) 
            plots1D['timeResolution'][0].Fill(ev.toa[i]-ev.gentoa[i]) 

    #################################################
    ##################Start plotting#################
    ################################################# 
    makePlots1D(plots1D, opts.outputDir)
   



