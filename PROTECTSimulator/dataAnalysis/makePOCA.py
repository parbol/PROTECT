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


    data = dict()
    data['hxy'] = [40, -5, 5, 40, -5, 5]
    data['hxz'] = [40, -5, 5, 20, -2, 2]
    data['hyz'] = [40, -5, 5, 20, -2, 2]
    pEstimator = POCAEstimator(input.events, data, 0.00)
    pEstimator.loop()
    pEstimator.MakePlot()
    input.Close()


 



 


