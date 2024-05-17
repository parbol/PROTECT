#ifndef Detector_h
#define Detector_h 1

#include "GeomObject.hh"
#include "Layer.hh"


class Detector : GeomObject {

public:

    Detector(G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4int);   
    
    void AddLayer(Layer *);
    
    Layer * GetLayer(G4int);
    
    G4int detId();

    G4int GetNLayers();
    
    void createG4Objects(G4String, G4LogicalVolume *, 
                        std::map<G4String, G4Material*> &, G4SDManager*);

    void Print();

private:
    std::vector<Layer *> layers;
    G4int ndetId;

};



#endif

