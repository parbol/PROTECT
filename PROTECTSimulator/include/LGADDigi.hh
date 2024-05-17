#ifndef LGADDigi_h
#define LGADDigi_h 1

#include "LGADSensorHit.hh"
#include "LGADSignalShape.hh"

#define MIPperMEV 66.667


class LGADDigi {

public:

    LGADDigi(LGADSensorHit *, LGADSignalShape *);

    G4int GetDet();

    G4int GetLayer();

    G4int GetLGAD();

    G4int GetPadx();

    G4int GetPady();

    G4bool Digitize();

    G4int eventNumber;
    G4int hitID;
    G4double TOA;
    G4double TOT;
    G4double genTOA;
    G4double genTOT;
    G4double charge;
    G4double genX, genY, genZ;

    LGADSignalShape *signalShape;

};



#endif

