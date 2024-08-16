#include "LGADDigi.hh"

//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
LGADDigi::LGADDigi(LGADSensorHit *h, LGADSignalShape *shape) {

    debug = 1;
    aHit = h;

    G4int det = h->GetDetectorID();
    G4int layer = h->GetLayerID();
    G4int lgad = h->GetLGADID();
   
    G4int padx = h->GetPadx();
    G4int pady = h->GetPady();
        
    G4int detS = det << 19;
    G4int layerS = layer << 14;
    G4int lgadS = lgad << 8;
    G4int padxS = padx << 4;
    G4int padyS = pady;
    
    hitID = detS | layerS | lgadS | padxS | padyS;
    

    genTOA = h->GetGenTOA();
    charge = (h->GetEnergy()/CLHEP::MeV)*MIPperMEV;
 
    genX = h->GetLocalPos().x();
    genY = h->GetLocalPos().y();
    genZ = h->GetLocalPos().z();
    genEnergy = h->GetGenEnergy();
    genID = h->GetGenID();
    eventNumber = h->GetEventNumber();
    signalShape = shape;

};
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Get Det                                                              //
//----------------------------------------------------------------------//
G4int LGADDigi::GetDet() {

    G4int maskDet = 0b00000000111110000000000000000000;
    return (hitID & maskDet) >> 19;

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Get Layer                                                            //
//----------------------------------------------------------------------//
G4int LGADDigi::GetLayer() {
 
    G4int maskLay = 0b00000000000001111100000000000000;
    return (hitID & maskLay) >> 14;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Get LGAD                                                             //
//----------------------------------------------------------------------//
G4int LGADDigi::GetLGAD() {
 
    G4int maskLGA = 0b00000000000000000011111100000000;
    return (hitID & maskLGA) >> 8;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Get Padx                                                             //
//----------------------------------------------------------------------//
G4int LGADDigi::GetPadx() {
  
    G4int maskpax = 0b00000000000000000000000011110000;
    return (hitID & maskpax) >> 4;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Get Pady                                                             //
//----------------------------------------------------------------------//
G4int LGADDigi::GetPady() {
  
    G4int maskpay = 0b00000000000000000000000000001111;
    return (hitID & maskpay);
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Digitize                                                             //
//----------------------------------------------------------------------//
G4bool LGADDigi::Digitize(CLHEP::RandGauss *myGauss, ConfigurationGeometry *geom) {
    
    G4double chThres = geom->getDetector(aHit->GetDetectorID())->GetLayer(aHit->GetLayerID())->GetSensor(aHit->GetLGADID())->chargethreshold();
    
    if(charge * signalShape->maximum() < chThres) return false;
    G4double noise = geom->getDetector(aHit->GetDetectorID())->GetLayer(aHit->GetLayerID())->GetSensor(aHit->GetLGADID())->noiselevel();
    G4double tdcsigma = geom->getDetector(aHit->GetDetectorID())->GetLayer(aHit->GetLayerID())->GetSensor(aHit->GetLGADID())->tdcsigma();

    std::pair<G4double, G4double> a = signalShape->getTimes(charge);
    if (a.first == 0 && a.second == 0) return false;
    
    G4double SignalToNoise = signalShape->maximum() * charge / noise;
    G4double sigmaJitter1 = signalShape->timeOfMax() / SignalToNoise;
    G4double sigmaJitter2 = (signalShape->fallTime() - signalShape->timeOfMax()) / SignalToNoise;
    
    G4double sigmaDistorsion = 0.0;
    
    //Calculate the Landau Noise
    //chOverMPV[0] = (it->second).hit_info[0][i] / (it->second).hit_info[2][i];
    //double sigmaLN = formulaLandauNoise_.evaluate(chOverMPV, emptyV);
    G4double sigmaLN = 0.025;
    
    G4double sigmaToA = sqrt(sigmaJitter1 * sigmaJitter1 + sigmaDistorsion * sigmaDistorsion + tdcsigma * tdcsigma +
                           sigmaLN * sigmaLN);
    G4double sigmaToC = sqrt(sigmaJitter2 * sigmaJitter2 + sigmaDistorsion * sigmaDistorsion + tdcsigma * tdcsigma +
                            sigmaLN * sigmaLN);
    
    G4double smearing1 = myGauss->fire(0., sigmaToA);
    G4double smearing2 = myGauss->fire(0., sigmaToC);   
    TOA = genTOA + (a.first + smearing1) * CLHEP::ns; 
    TOT = (a.second + smearing2 - smearing1) * CLHEP::ns;
    if (TOT < 0) return false; 
   
    //Start here with the smearing
    if(debug) {
        Print();
    }

    return true;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//
  

//----------------------------------------------------------------------//
// Print Digi                                                           //
//----------------------------------------------------------------------//
void LGADDigi::Print() { 
    
    G4cout << "Printing DIGI information in event: " << eventNumber << G4endl;
    G4cout << "Det: " << GetDet() << " Layer: " << GetLayer() << " LGAD: " << GetLGAD() << " Padx: " << GetPadx() << " Pady: " << GetPady() << G4endl;
    G4cout << "Gen Local Pos x: " << genX/CLHEP::cm << " y: " << genY/CLHEP::cm << " z: " << genZ/CLHEP::cm << G4endl;
    G4cout << "Gen Energy: " << genEnergy/CLHEP::MeV << " Gen TOA: " << genTOA/CLHEP::ns << " genID: " << genID << G4endl;
    G4cout << "TOA: " << TOA/CLHEP::ns << " TOT: " << TOT/CLHEP::ns << G4endl;

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//