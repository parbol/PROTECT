#include "Gantry.hh"



//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
Gantry::Gantry(G4double xPos, G4double yPos, G4double zPos, G4double xRot, 
                   G4double yRot, G4double zRot, G4double pRmin1_, G4double pRmax1_,
                   G4double pRmin2_, G4double pRmax2_, G4double sizez_) : GeomObject(xPos, yPos, zPos, xRot, yRot,
                   zRot, pRmax2_, pRmax2_, sizez_) {
    pRmin1 = pRmin1_;
    pRmax1 = pRmax1_;
    pRmin2 = pRmin2_;
    pRmax2 = pRmax2_;
    sizez = sizez_;
    
};
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// createG4Objects                                              //
//----------------------------------------------------------------------//
void Gantry::createG4Objects(G4String name, G4LogicalVolume *mother,
                               std::map<G4String, G4Material*> & materials,
                               G4SDManager *SDman) {

    G4String gantryName = G4String("gantry_") + name;  
    solidVolume = new G4Cons(gantryName, pRmin1, pRmax1, pRmin2, pRmax2,
                             sizez/2.0, 0.0, 2.0*CLHEP::pi);
    logicalVolume = new G4LogicalVolume(solidVolume, materials["steel"], gantryName);
    G4String gantryPhysicalName = G4String("gantryPhys_") + name;
    physicalVolume = new G4PVPlacement(getRot(), getPos(), logicalVolume, gantryPhysicalName,
                                       mother, false, 0, true);
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// Print                                                                //
//----------------------------------------------------------------------//
void Gantry::Print() {

    G4cout << "\033[1;34m" << "Gantry" << "\033[0m" << G4endl;
    G4cout << "\033[1;34m" << "Location x: " << pos.x()/CLHEP::cm << ", y: " << pos.y()/CLHEP::cm << ", z: " << pos.z()/CLHEP::cm << G4endl;
    G4cout << "\033[1;34m" << "Rotation x: " << rots.x() << ", y: " << rots.y() << ", z: " << rots.z() << G4endl;
    G4cout << "\033[1;34m" << "pRmin1: " << pRmin1/CLHEP::cm << ", pRmax1: " << pRmax1/CLHEP::cm << G4endl;
    G4cout << "\033[1;34m" << "pRmin2: " << pRmin2/CLHEP::cm << ", pRmax2: " << pRmax2/CLHEP::cm << G4endl;
    G4cout << "\033[1;34m" << "Size Z: " << sizez/CLHEP::cm << G4endl;
    G4cout << "\033[0m" << G4endl;

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//
