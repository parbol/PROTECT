#ifndef Gantry_h
#define Gantry_h 1

#include "GeomObject.hh"


class Gantry : GeomObject {

public:

    Gantry(G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double);   
    
    void createG4Objects(G4String, G4LogicalVolume *, 
                        std::map<G4String, G4Material*> &, G4SDManager*);

    void Print();

private:
    
    G4double pRmin1;
    G4double pRmax1;
    G4double pRmin2;
    G4double pRmax2;
    G4double sizez;    

};



#endif

