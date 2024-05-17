#ifndef LGAD_h
#define LGAD_h 1

#include "GeomObject.hh"
#include <tuple>
#include "LGADSignalShape.hh"


class LGAD : GeomObject {

public:

    LGAD(G4double, G4double, G4double, 
         G4double, G4double, G4double, 
         G4double, G4double, G4double,
         G4int, G4int, G4double, G4double,
         G4double, G4double, G4double, G4double,
         G4double, G4double, G4int, G4int, G4int);

    G4int detId();

    G4int layerId();

    G4int sensorId();

    LGADSignalShape * signalShape();


    void createG4Objects(G4String, G4LogicalVolume *, 
                         std::map<G4String, G4Material*> &,
                         G4SDManager *);
    
    void Print();

    G4int npadx();
    
    G4int npady();

    G4double interpadx();
    
    G4double interpady();
    
    G4double borderpadx();
    
    G4double borderpady();
    
    G4double chargethreshold();
    
    G4double noiselevel();
    
    G4double tdcsigma();
    
    G4double gain();

    std::tuple<G4int, G4int, G4double> getPads(G4ThreeVector);

private:
    G4int ndetId, nlayerId, nsensorId;
    G4int nPadx, nPady;
    G4double interPadx, interPady, borderPadx, borderPady;
    G4double chargeThreshold, noiseLevel, tdcSigma, Gain;

    LGADSignalShape *signalShape_;    

};



#endif

