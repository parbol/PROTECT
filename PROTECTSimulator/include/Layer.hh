#ifndef Layer_h
#define Layer_h 1

#include "GeomObject.hh"
#include "LGAD.hh"


class Layer : GeomObject {

public:

    Layer(G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4int, G4int);
    
    void AddSensor(LGAD *);
    
    LGAD *GetSensor(G4int);
    
    G4int detId();

    G4int layerId();

    G4int GetNSensors();

    void createG4Objects(G4String, G4LogicalVolume *, std::map<G4String, G4Material*> &, G4SDManager*);
    
    void Print();

private:
    std::vector<LGAD *> sensors;
    G4int ndetId, nlayerId;
};



#endif

