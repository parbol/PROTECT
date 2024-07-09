#ifndef LGADDigi_h
#define LGADDigi_h 1
#include "Randomize.hh"
#include "LGADSensorHit.hh"
#include "LGADSignalShape.hh"
#include "ConfigurationGeometry.hh"
#define MIPperMEV 66.667


class LGADDigi {

public:

    LGADDigi(LGADSensorHit *, LGADSignalShape *);

    G4int GetDet();

    G4int GetLayer();

    G4int GetLGAD();

    G4int GetPadx();

    G4int GetPady();

    G4bool Digitize(CLHEP::RandGauss *, ConfigurationGeometry *);

    void Print();

    G4int debug;
    G4int eventNumber;
    G4int hitID;
    G4double TOA;
    G4double TOT;
    G4double genTOA;
    G4double genTOT;
    G4double charge;
    G4double genX, genY, genZ;
    G4double genEnergy;
    G4int genID;
    LGADSignalShape *signalShape;
    LGADSensorHit *aHit;

};



#endif

