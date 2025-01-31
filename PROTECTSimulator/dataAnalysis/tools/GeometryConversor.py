import json, sys, optparse
import ROOT as r
from array import array



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
        
        realx = x + xdet + xlayer + xlgad    
        realy = y + ydet + ylayer + ylgad   
        realz = z + zdet + zlayer + zlgad

        return realx, realy, realz 

    def toGlobalMeasurement(self, det, layer, lgad, xpad, ypad):

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
        xsize = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['xSizeSensor']
        ysize = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['ySizeSensor']
        nPadx = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['nPadx']
        nPady = self.data['Detectors'][det]['Layers'][layer]['Sensors'][lgad]['nPady']
        padsizex = (xsize - 2.0*xborder)/nPadx
        padsizey = (ysize - 2.0*yborder)/nPady
        realx = xdet + xlayer + xlgad + xborder - xsize / 2.0 + padsizex/2.0 + xpad * padsizex 
        realy = ydet + ylayer + ylgad + yborder - ysize / 2.0 + padsizey/2.0 + ypad * padsizey 
        realz = zdet + zlayer + zlgad

        return realx, realy, realz 


