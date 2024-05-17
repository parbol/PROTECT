

#include "LGAD.hh"
#include "LGADSensor.hh"

//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
LGAD::LGAD(G4double xPos, G4double yPos, G4double zPos,
           G4double xRot, G4double yRot, G4double zRot,
           G4double xSize, G4double ySize, G4double zSize,
           G4int nxpad, G4int nypad, G4double interpadx, G4double interpady,
           G4double borderpadx, G4double borderpady, G4double chargeThres,
           G4double noise, G4double tdcSigma_, G4double gain_,
           G4int ndet, G4int nlayer, G4int nsensor) :
           GeomObject(xPos, yPos, zPos, xRot, yRot, zRot, xSize, ySize, zSize) {
            ndetId = ndet;
            nlayerId = nlayer;
            nsensorId = nsensor;
            nPadx = nxpad;
            nPady = nypad;
            interPadx = interpadx;
            interPady = interpady;
            borderPadx = borderpadx;
            borderPady = borderpady;
            chargeThreshold = chargeThres;
            noiseLevel = noise;
            tdcSigma = tdcSigma_;
            Gain = gain_;
            signalShape_ = new LGADSignalShape(chargeThreshold);
           };
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return signalShape pointer                                           //
//----------------------------------------------------------------------//
LGADSignalShape * LGAD::signalShape() {
    return signalShape_;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return nPadx                                                         //
//----------------------------------------------------------------------//
G4int LGAD::npadx() {
	return nPadx;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return nPady                                                         //
//----------------------------------------------------------------------//
G4int LGAD::npady() {
	return nPady;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return interPadx                                                     //
//----------------------------------------------------------------------//
G4double LGAD::interpadx() {
	return interPadx;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return interPady                                                     //
//----------------------------------------------------------------------//
G4double LGAD::interpady() {
	return interPady;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return borderPadx                                                    //
//----------------------------------------------------------------------//
G4double LGAD::borderpadx() {
	return borderPadx;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return borderPady                                                    //
//----------------------------------------------------------------------//
G4double LGAD::borderpady() {
	return borderPady;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return chargeTreshold                                                //
//----------------------------------------------------------------------//
G4double LGAD::chargethreshold() {
	return chargeThreshold;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return noiseLevel                                                    //
//----------------------------------------------------------------------//
G4double LGAD::noiselevel() {
	return noiseLevel;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return tdcSigma                                                      //
//----------------------------------------------------------------------//
G4double LGAD::tdcsigma() {
	return tdcSigma;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return gain                                                          //
//----------------------------------------------------------------------//
G4double LGAD::gain() {
	return Gain;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return detId                                                         //
//----------------------------------------------------------------------//
G4int LGAD::detId() {
	return ndetId;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return layerId                                                       //
//----------------------------------------------------------------------//
G4int LGAD::layerId() {
	return nlayerId;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Return sensorId                                                         //
//----------------------------------------------------------------------//
G4int LGAD::sensorId() {
	return nsensorId;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// createG4Objects                                              //
//----------------------------------------------------------------------//
void LGAD::createG4Objects(G4String name, G4LogicalVolume *mother,
                               std::map<G4String, G4Material*> &materials,
                               G4SDManager *SDman) {

    G4String LGADName = G4String("LGAD_") + name;  
    solidVolume = new G4Box(LGADName, sizes[0]/2.0, sizes[1]/2.0, sizes[2]/2.0);
    logicalVolume = new G4LogicalVolume(solidVolume, materials["air"], LGADName);
    G4String LGADPhysicalName = G4String("LGADPhys_") + name;
    physicalVolume = new G4PVPlacement(getRot(), getPos(), 
                                       logicalVolume, LGADPhysicalName,
                                       mother, false, 0, true);

    //We need to make this object sensitive
    G4String SDname = LGADName;
    G4String Collection = G4String("HitsCollection_") + name;
    LGADSensor *lgadSensor = new LGADSensor(SDname = SDname, Collection);
    lgadSensor->setLGAD(this);
    SDman->AddNewDetector(lgadSensor);
    logicalVolume->SetSensitiveDetector(lgadSensor);

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Print                                                                //
//----------------------------------------------------------------------//
void LGAD::Print() {

    G4cout << "\033[1;34m" << "LGAD" << "\033[0m" << G4endl;
    G4cout << "\033[1;34m" << "Location x: " << pos.x()/CLHEP::cm << ", y: " << pos.y()/CLHEP::cm << ", z: " << pos.z()/CLHEP::cm << G4endl;
    G4cout << "\033[1;34m" << "Rotation x: " << rots.x() << ", y: " << rots.y() << ", z: " << rots.z() << G4endl;
    G4cout << "\033[1;34m" << "Sizes x: " << sizes.x()/CLHEP::cm << ", y: " << sizes.y()/CLHEP::cm << ", z: " << sizes.z()/CLHEP::cm << G4endl;
    G4cout << "\033[1;34m" << "N pads x: " << nPadx << " N pads y: " << nPady << G4endl; 
    G4cout << "\033[1;34m" << "Interpad x: " << interPadx << " Interpad y: " << interPady << G4endl; 
    G4cout << "\033[1;34m" << "Border x: " << borderPadx << " Border y: " << borderPady << G4endl; 
    G4cout << "\033[1;34m" << "chargeThreshold: " << chargeThreshold << " noise: " << noiseLevel << " tdcSigma: " << tdcSigma << G4endl; 
    G4cout << "\033[0m" << G4endl;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// GetPads                                                              //
//----------------------------------------------------------------------//
std::tuple<G4int, G4int, G4double> LGAD::getPads(G4ThreeVector p) {

    G4double px = p.x();
    G4double py = p.y();
    G4double sizex = sizes.x();
    G4double sizey = sizes.y();
    G4double padSizex = (sizex - 2.0*borderPadx)/nPadx;
    G4double padSizey = (sizey - 2.0*borderPady)/nPady;
    G4double G = Gain; 
    G4double xref = (px + sizex/2.0 - borderPadx)/padSizex;
    G4double yref = (py + sizey/2.0 - borderPady)/padSizey;
    //Let's start with the x
    G4int i = G4int(floor(xref));
    if(xref <= 0) {
        i = 0;
        G = 1.0;
    } else if (xref >= nPadx) {
        i = nPadx-1;
        G = 1.0;
    } else {
        G4double poslocalpad = xref - floor(xref);
        if(poslocalpad <= interPadx/2.0 || poslocalpad >= 1.0 - interPadx/2.0) {
            G = 1.0;
        }
    }
    //Let's start with the x
    G4int j = G4int(floor(yref));
    if(yref <= 0) {
        j = 0;
        G = 1.0;
    } else if (yref >= nPady) {
        j = nPady-1;
        G = 1.0;
    } else {
        G4double poslocalpad = yref - floor(yref);
        if(poslocalpad <= interPady/2.0 || poslocalpad >= 1.0 - interPady/2.0) {
            G = 1.0;
        }
    }
    //G4cout << "Size x " << sizex << " " << sizey << G4endl;
    //if(G > 1.0) G4cout << "Real position " << px/CLHEP::cm << " " << py/CLHEP::cm << G4endl;
    //G4cout << "Ref position " << xref << " " << yref << G4endl; 
    //G4cout << "Pad: " << i << " " << j << " " << G << G4endl;
    return {i, j, G};
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//
