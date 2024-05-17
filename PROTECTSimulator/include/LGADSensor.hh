#ifndef LGADSensor_h
#define LGADSensor_h 1

#include "G4VSensitiveDetector.hh"
#include "LGADSensorHit.hh"
#include "LGAD.hh"

class G4Step;
class G4HCofThisEvent;
class G4TouchableHistory;

class LGADSensor : public G4VSensitiveDetector
{

public:
    LGADSensor(G4String name, G4String collection);
    
    void setLGAD(LGAD *);
    virtual ~LGADSensor();
    LGAD *getLGAD();
    virtual void Initialize(G4HCofThisEvent*HCE);
    virtual G4bool ProcessHits(G4Step*aStep,G4TouchableHistory*ROhist);
    virtual void EndOfEvent(G4HCofThisEvent*HCE);

private:
    LGADSensorHitsCollection * hitsCollection;
    G4ThreeVector theLocalPosError;
    LGAD *lgad;
    G4int HCID;
};




#endif

