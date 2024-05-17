#ifndef GeomObject_h
#define GeomObject_h 1

#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"
#include "G4VSolid.hh"
#include "G4LogicalVolume.hh"
#include "G4VPhysicalVolume.hh"
#include "G4ErrorMatrix.hh"
#include "G4Box.hh"
#include "G4PVPlacement.hh"
#include "G4Material.hh"
#include "G4SDManager.hh"


class GeomObject {

public:

    GeomObject(G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double);
    G4RotationMatrix *getRot();
    G4ThreeVector     getPos();
    G4ThreeVector     getSizes();
    G4ThreeVector     toGlobal(G4ThreeVector);
    G4ThreeVector     toLocal(G4ThreeVector);
    G4ErrorMatrix     toGlobalStateVector(G4ErrorMatrix);
    G4ErrorMatrix     toGlobalStateCov(G4ErrorMatrix);
    G4VSolid          *getSolidVolume();
    G4LogicalVolume   *getLogicalVolume();
    G4VPhysicalVolume *getPhysicalVolume();
    void              setPhysicalVolume(G4VPhysicalVolume *);
    void              Print();

    G4RotationMatrix rot, invrot;
    G4ThreeVector pos;
    G4ThreeVector sizes;
    G4ThreeVector rots;
    G4ErrorMatrix *superMatrix;
    G4ErrorMatrix *superVector;
    G4VSolid* solidVolume;
    G4LogicalVolume *logicalVolume;
    G4VPhysicalVolume *physicalVolume;


private:

};



#endif

