import json, sys, optparse
from tools.POCAEstimator import POCAEstimator
import ROOT as r




if __name__=='__main__':

    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', default='input.root', help='Input ROOT File')
    (opts, args) = parser.parse_args()
    
    try:
        input = r.TFile(opts.inputFile)
    except:
        print('Cannot open input file')
        sys.exit()


    tdrStyle =  r.TStyle("tdrStyle","Style for P-TDR")
    tdrStyle.SetCanvasBorderMode(0)
    #tdrStyle.SetPadTopMargin(0.05)
    #tdrStyle.SetPadBottomMargin(0.13)
    #tdrStyle.SetPadLeftMargin(0.16)
    tdrStyle.SetPadRightMargin(0.2)
    tdrStyle.cd()
    data = dict()
    data['hxy'] = [80, -12, 12, 80, -12, 12]
    data['hxz'] = [80, -12, 12, 20, -2, 2]
    data['hyz'] = [80, -12, 12, 20, -2, 2]
    pEstimator = POCAEstimator(input.events, data, -0.01)
    pEstimator.loop()
    pEstimator.MakePlot()
    input.Close()


 



 


