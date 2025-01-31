import ROOT as r
import math



    

class POCAEstimator:

    def __init__(self, tree, binInfo, threshold1, threshold2, style, path):

        self.style = style
        self.tree = tree
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.binInfo = binInfo
        self.path = path
        #Preparing all histograms 
        self.thetax = r.TH1F('thetax', '', 100, -0.2, 0.2)
        self.thetax.SetStats(0)
        self.thetax.GetXaxis().SetTitle('#Delta#theta_{x}')
        self.thetay = r.TH1F('thetay', '', 100, -0.2, 0.2)
        self.thetay.SetStats(0)
        self.thetay.GetXaxis().SetTitle('#Delta#theta_{y}')
        self.hxyproj = r.TH2F('hxyproj', '', int(binInfo['hxy'][0]), binInfo['hxy'][1], binInfo['hxy'][2], int(binInfo['hxy'][3]), binInfo['hxy'][4], binInfo['hxy'][5])
        self.hxyproj.SetStats(0)
        self.hxyproj.GetXaxis().SetTitle('X [cm]')
        self.hxyproj.GetYaxis().SetTitle('Y [cm]')
        self.hxyproj.GetZaxis().SetTitle('N. Events')
        self.hxy = r.TH2F('hxy', '', int(binInfo['hxy'][0]), binInfo['hxy'][1], binInfo['hxy'][2], int(binInfo['hxy'][3]), binInfo['hxy'][4], binInfo['hxy'][5])
        self.hxy.SetStats(0)
        self.hxy.GetXaxis().SetTitle('X [cm]')
        self.hxy.GetYaxis().SetTitle('Y [cm]')
        self.hxy.GetZaxis().SetTitle('N. Events')
        self.hxz = r.TH2F('hxz', '', int(binInfo['hxz'][0]), binInfo['hxz'][1], binInfo['hxz'][2], int(binInfo['hxz'][3]), binInfo['hxz'][4], binInfo['hxz'][5])
        self.hxz.SetStats(0)
        self.hxz.GetXaxis().SetTitle('X [cm]')
        self.hxz.GetYaxis().SetTitle('Z [cm]')
        self.hxz.GetZaxis().SetTitle('N. Events')
        self.hyz = r.TH2F('hyz', '', int(binInfo['hyz'][0]), binInfo['hyz'][1], binInfo['hyz'][2], int(binInfo['hyz'][3]), binInfo['hyz'][4], binInfo['hyz'][5])
        self.hyz.SetStats(0)
        self.hyz.GetXaxis().SetTitle('Y [cm]')
        self.hyz.GetYaxis().SetTitle('Z [cm]')
        self.hyz.GetZaxis().SetTitle('N. Events')
        self.aux_hxy = self.hxy.Clone('aux_hxy')
        self.aux_hyz = self.hyz.Clone('aux_hyz')
        self.aux_hxz = self.hxz.Clone('aux_hxz')
        self.hxy_sat = self.hxy.Clone('hxy_sat')
        self.hyz_sat = self.hyz.Clone('hyz_sat')
        self.hxz_sat = self.hxz.Clone('hxz_sat')
        self.hxy_sat.SetMaximum(40.0)
        self.hxz_sat.SetMaximum(40.0)
        self.hyz_sat.SetMaximum(40.0)
        self.hxy_theta = r.TH2F('hxy_theta', '', int(binInfo['hxy'][0]), binInfo['hxy'][1], binInfo['hxy'][2], int(binInfo['hxy'][3]), binInfo['hxy'][4], binInfo['hxy'][5])
        self.hxz_theta = r.TH2F('hxz_theta', '', int(binInfo['hxz'][0]), binInfo['hxz'][1], binInfo['hxz'][2], int(binInfo['hxz'][3]), binInfo['hxz'][4], binInfo['hxz'][5])
        self.hyz_theta = r.TH2F('hyz_theta', '', int(binInfo['hyz'][0]), binInfo['hyz'][1], binInfo['hyz'][2], int(binInfo['hyz'][3]), binInfo['hyz'][4], binInfo['hyz'][5])
        self.hxy_theta2 = r.TH2F('hxy_theta2', '', int(binInfo['hxy'][0]), binInfo['hxy'][1], binInfo['hxy'][2], int(binInfo['hxy'][3]), binInfo['hxy'][4], binInfo['hxy'][5])
        self.hxz_theta2 = r.TH2F('hxz_theta2', '', int(binInfo['hxz'][0]), binInfo['hxz'][1], binInfo['hxz'][2], int(binInfo['hxz'][3]), binInfo['hxz'][4], binInfo['hxz'][5])
        self.hyz_theta2 = r.TH2F('hyz_theta2', '', int(binInfo['hyz'][0]), binInfo['hyz'][1], binInfo['hyz'][2], int(binInfo['hyz'][3]), binInfo['hyz'][4], binInfo['hyz'][5])
        self.var_xy = r.TH2F('var_xy', '', int(binInfo['hxy'][0]), binInfo['hxy'][1], binInfo['hxy'][2], int(binInfo['hxy'][3]), binInfo['hxy'][4], binInfo['hxy'][5])
        self.var_xy.SetStats(0)
        self.var_xy.GetXaxis().SetTitle('X [cm]')
        self.var_xy.GetYaxis().SetTitle('Y [cm]')
        self.var_xy.GetZaxis().SetTitle('#sigma(#theta)p#beta [rad MeV]')
        self.var_xz = r.TH2F('var_xz', '', int(binInfo['hxz'][0]), binInfo['hxz'][1], binInfo['hxz'][2], int(binInfo['hxz'][3]), binInfo['hxz'][4], binInfo['hxz'][5])
        self.var_xz.SetStats(0)
        self.var_xz.GetXaxis().SetTitle('X [cm]')
        self.var_xz.GetYaxis().SetTitle('Z [cm]')
        self.var_xz.GetZaxis().SetTitle('#sigma(#theta) [rad]')
        self.var_yz = r.TH2F('var_yz', '', int(binInfo['hyz'][0]), binInfo['hyz'][1], binInfo['hyz'][2], int(binInfo['hyz'][3]), binInfo['hyz'][4], binInfo['hyz'][5])
        self.var_yz.SetStats(0)
        self.var_yz.GetXaxis().SetTitle('Y [cm]')
        self.var_yz.GetYaxis().SetTitle('Z [cm]')
        self.var_yz.GetZaxis().SetTitle('#sigma(#theta)p#beta [rad MeV]')
        
        #Preparing variables for roofit
        self.xvar = r.RooRealVar("X","X (cm)", -12.0, 12.0)
        self.yvar = r.RooRealVar("Y","Y (cm)", -12.0, 12.0);
        self.d = r.RooDataSet("d","d", r.RooArgSet(self.xvar,self.yvar))


    def loop(self):
        
        for ev in self.tree:
            
            x1 = [ev.x1, ev.y1, ev.z1]
            x2 = [ev.x2, ev.y2, ev.z2]
            vx1 = [ev.vx1, ev.vy1, ev.vz1]
            vx2 = [ev.vx2, ev.vy2, ev.vz2]
            valid = False
            v = [0, 0, 0]
            if self.style == 1:
                if abs(ev.dthetax) > self.threshold1 or abs(ev.dthetay) > self.threshold1:
                    valid, v = self.getPoint(x1, x2, vx1, vx2, ev.p, ev.p, ev.dthetax, ev.dthetay)
            else:
                if ev.p < 0.0 or ev.p > 1500.0:
                    if abs(ev.dthetax) > self.threshold1 or abs(ev.dthetay) > self.threshold1:
                        valid, v = self.getPoint(x1, x2, vx1, vx2, ev.p, ev.p, ev.dthetax, ev.dthetay)
                else:
                    if abs(ev.dthetax*ev.p) > self.threshold2 or abs(ev.dthetay*ev.p) > self.threshold2:
                        valid, v = self.getPoint(x1, x2, vx1, vx2, ev.p, ev.p, ev.dthetax, ev.dthetay)
            if valid:
                #Angular
                self.thetax.Fill(ev.dthetax)
                self.thetay.Fill(ev.dthetay)
                #RooFit
                self.xvar.setVal(v[0])
                self.yvar.setVal(v[1])
                self.d.add(r.RooArgSet(self.xvar,self.yvar))
                #Histograms xy
                self.aux_hxy.Fill(v[0], v[1])
                binxy = self.aux_hxy.FindBin(v[0], v[1])
                valxy = self.hxy_theta.GetBinContent(binxy)
                self.hxy_theta.SetBinContent(binxy, valxy + (ev.dthetax + ev.dthetay))
                valxy2 = self.hxy_theta2.GetBinContent(binxy)
                self.hxy_theta2.SetBinContent(binxy, valxy2 + (ev.dthetax)**2 + (ev.dthetay)**2)
                #Histograms xz
                self.aux_hxz.Fill(v[0], v[2])
                binxz = self.aux_hxz.FindBin(v[0], v[2])
                valxz = self.hxz_theta.GetBinContent(binxz)
                self.hxz_theta.SetBinContent(binxz, valxz + ev.dthetax + ev.dthetay)
                valxz2 = self.hxz_theta2.GetBinContent(binxz)
                self.hxz_theta2.SetBinContent(binxz, valxz2 + ev.dthetax**2 + ev.dthetay**2)
                #Histograms yz
                self.aux_hyz.Fill(v[1], v[2])
                binyz = self.aux_hyz.FindBin(v[1], v[2])
                valyz = self.hyz_theta.GetBinContent(binyz)
                self.hyz_theta.SetBinContent(binyz, valyz + ev.dthetax + ev.dthetay)
                valyz2 = self.hyz_theta2.GetBinContent(binyz)
                self.hyz_theta2.SetBinContent(binyz, valyz2 + ev.dthetax**2 + ev.dthetay**2)
        self.makeVar()

    def cross(self, v1, v2):

        a = [0.0, 0.0, 0.0]
        a[0] = v1[1] * v2[2] - v1[2] * v2[1]
        a[1] = v1[2] * v2[0] - v1[0] * v2[2]
        a[2] = v1[0] * v2[1] - v1[1] * v2[0]
        return a

    def dot(self, v1, v2):

        return v1[0]*v2[0] + v1[1]*v2[1] + v1[2] * v2[2]

    def norm(self, v):

        return math.sqrt(v[0]**2+v[1]**2+v[2]**2)

    def normalize(self, v):
        n = self.norm(v)
        a = v
        a[0] = v[0]/n
        a[1] = v[1]/n
        a[2] = v[2]/n
        return a

    def minus(self, v1, v2):

        return [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]]
    
    def plus(self, v1, v2):

        return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]

    def divide(self, v1, k):

        return [v1[0]/k, v1[1]/k, v1[2]/k]
    
    def multiply(self, v1, k):

        return [v1[0]*k, v1[1]*k, v1[2]*k]

    def getPoint(self, x1, x2, p1, p2, k1, k2, thetax, thetay):

        b1 = k1 / math.sqrt(k1**2 + 105.66**2)
        b2 = k2 / math.sqrt(k2**2 + 105.66**2)
        momentum = (k1+k2)/2.0
        beta = (b1+b2)/2.0
        betap = momentum * beta

        cross_st = self.cross(p1, p2)
        cross_stnorm = self.norm(cross_st)
        vts = self.dot(p1, p2)
        if cross_stnorm < 1.0e-6 or vts < 1.0e-6:
            return False, [0, 0, 0]
        
        cross_sst = self.cross(p1, cross_st)
        DeltaR = self.minus(x1, x2)
        
        xproj = x2[0] + (20.0-x2[2])/p2[2] * p2[0]
        yproj = x2[1] + (20.0-x2[2])/p2[2] * p2[1]
        self.hxyproj.Fill(xproj, yproj)
        xpoca2 = self.minus(x2, self.multiply(p2, self.dot(DeltaR, cross_sst)/cross_stnorm**2))
        xpoca1 = self.plus(x1, self.multiply(p1, self.dot(self.minus(xpoca2, x1), p1)/vts))
        v = self.multiply(self.plus(xpoca1, xpoca2), 0.5)
        return True, v


    def makeVar(self):
      
        N = 6
        N2 = 14
        #Histogram xy
        for ix in range(0, self.hxy.GetNbinsX()):
            for iy in range(0, self.hxy.GetNbinsY()):
                if ix < 1 or ix >= self.hxy.GetNbinsX() or iy < 1 or iy >= self.hxy.GetNbinsY():
                    continue
                n = 2.0 * self.aux_hxy.GetBinContent(ix, iy)
                theta = self.hxy_theta.GetBinContent(ix, iy)
                theta2 = self.hxy_theta2.GetBinContent(ix, iy)
                if n >= N:
                    self.var_xy.SetBinContent(ix, iy, math.sqrt(theta2/n - (theta/n)**2))
                    self.hxy.SetBinContent(ix, iy, self.aux_hxy.GetBinContent(ix, iy))
                    if n >= N2:
                        self.hxy_sat.SetBinContent(ix, iy, 1.0)

        #Histogram xz
        for ix in range(0, self.hxz.GetNbinsX()):
            for iy in range(0, self.hxz.GetNbinsY()):
                if ix < 1 or ix >= self.hxz.GetNbinsX() or iy < 1 or iy >= self.hxz.GetNbinsY():
                    continue
                n = 2.0 * self.aux_hxz.GetBinContent(ix, iy)
                theta = self.hxz_theta.GetBinContent(ix, iy)
                theta2 = self.hxz_theta2.GetBinContent(ix, iy)
                if n >= N:
                    self.var_xz.SetBinContent(ix, iy, math.sqrt(theta2/n - (theta/n)**2))
                    self.hxz.SetBinContent(ix, iy, self.aux_hxz.GetBinContent(ix, iy))
                    if n >= N2:
                        self.hxz_sat.SetBinContent(ix, iy, 1.0)
        
        #Histogram yz
        for ix in range(1, self.hyz.GetNbinsX()):
            for iy in range(1, self.hyz.GetNbinsY()):
                if ix < 1 or ix >= self.hxz.GetNbinsX() or iy < 1 or iy >= self.hxz.GetNbinsY():
                    continue
                n = 2.0 * self.aux_hyz.GetBinContent(ix, iy)
                theta = self.hyz_theta.GetBinContent(ix, iy)
                theta2 = self.hyz_theta2.GetBinContent(ix, iy)
                if n >= N:
                    self.var_yz.SetBinContent(ix, iy, math.sqrt(theta2/n - (theta/n)**2))
                    self.hyz.SetBinContent(ix, iy, self.aux_hyz.GetBinContent(ix, iy))
                    self.hyz_sat.SetBinContent(ix, iy, 20.0)
                    if n >= N2:
                        self.hyz_sat.SetBinContent(ix, iy, 1.0)


    def histogramWithFrame(self, h, option):

        name = h.GetName() 
        filename = name + '.png'
        nameCanvas = name + '_canvas'
        c = r.TCanvas(nameCanvas, nameCanvas)
        h.Draw(option)
        c.SaveAs(self.path + '/' + filename)

    def histogramWithoutFrame(self, h, option):

        name = h.GetName() + '_noframe'
        newh = h.Clone(name)
        filename = name + '.png'
        nameCanvas = name + '_canvas'
        c = r.TCanvas(nameCanvas, nameCanvas)
        c.SetFrameLineColor(0)
        c.SetRightMargin(0)
        c.SetLeftMargin(0)
        c.SetTopMargin(0)
        c.SetBottomMargin(0)
        newh.Draw(option)
        c.SaveAs(self.path + '/' + filename)

 
    def MakePlot(self):

        #Angular distributions
        self.histogramWithFrame(self.thetax, 'HIST')
        self.histogramWithFrame(self.thetay, 'HIST')
        #cxy Normal
        self.histogramWithFrame(self.hxy, 'COLZ')
        self.histogramWithoutFrame(self.hxy, 'COLA')
        #cxz Normal
        self.histogramWithFrame(self.hxz, 'COLZ')
        self.histogramWithoutFrame(self.hxz, 'COLA')
        #cyz Normal
        self.histogramWithFrame(self.hyz, 'COLZ')
        self.histogramWithoutFrame(self.hyz, 'COLA')
        #cxy Sat
        self.histogramWithFrame(self.hxy_sat, 'COLZ')
        self.histogramWithoutFrame(self.hxy_sat, 'COLA')
        #cxz Sat
        self.histogramWithFrame(self.hxz_sat, 'COLZ')
        self.histogramWithoutFrame(self.hxz_sat, 'COLA')
        #cyz Sat
        self.histogramWithFrame(self.hyz_sat, 'COLZ')
        self.histogramWithoutFrame(self.hyz_sat, 'COLA')
        #varcxy Normal
        self.histogramWithFrame(self.var_xy, 'COLZ')
        self.histogramWithoutFrame(self.var_xy, 'COLA')
        #varcxz Normal
        self.histogramWithFrame(self.var_xz, 'COLZ')
        self.histogramWithoutFrame(self.var_xz, 'COLA')
        #varcyz Normal
        self.histogramWithFrame(self.var_yz, 'COLZ')
        self.histogramWithoutFrame(self.var_yz, 'COLA')
        #pdfktest 
        kest4 = r.RooNDKeysPdf("kest4","kest4", r.RooArgSet(self.xvar, self.yvar), self.d)
        bin1 = r.RooFit.Binning(int(self.binInfo['hxy'][0]), self.binInfo['hxy'][1], self.binInfo['hxy'][2])
        bin2 = r.RooFit.Binning(int(self.binInfo['hxy'][3]), self.binInfo['hxy'][4], self.binInfo['hxy'][5])
        hh_data = self.d.createHistogram("hh_data", self.xvar, bin1, r.RooFit.YVar(self.yvar, bin2))
        hh_pdf = kest4.createHistogram("hh_kernel", self.xvar, bin1, r.RooFit.YVar(self.yvar, bin2))
        hh_pdf.SetStats(0)
        hh_pdf.SetTitle('')
        #kTest
        for ix in range(0, hh_pdf.GetNbinsX()):
            for iy in range(0, hh_pdf.GetNbinsY()):
                val = hh_pdf.GetBinContent(ix, iy)
                #if val < 0.0003: for configuration 5
                if val < 0.0001: #for configuration 6, 7, 8
                    val = hh_pdf.SetBinContent(ix, iy, 0.0)
        self.histogramWithFrame(hh_pdf, 'COLZ')
        self.histogramWithoutFrame(hh_pdf, 'COLA')

 
