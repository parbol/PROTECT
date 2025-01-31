#ifndef Phantom_h
#define Phantom_h 1

#include "GeomObject.hh"
#include "G4Tubs.hh"


class Phantom : GeomObject {

public:

    Phantom(G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4String, G4String);   
    
    G4String getName();

    G4String getMaterial();
    
    void createG4Objects(G4LogicalVolume *, 
                        std::map<G4String, G4Material*> &, G4SDManager*);

    void Print();

private:
   
    G4double radius;
    G4double zsize; 
    G4String name;
    G4String material;

};



#endif

