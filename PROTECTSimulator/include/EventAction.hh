#ifndef EventAction_h
#define EventAction_h 1


#include "G4UserEventAction.hh"
#include "globals.hh"
#include <vector>
#include "Randomize.hh"
#include "LGADSensorHit.hh"
#include "ConfigurationGeometry.hh"
#include "LGADDigi.hh"

#ifdef G4ANALYSIS_USE
#include "AIDA/AIDA.h"
using namespace AIDA;
#endif


class EventActionMessenger;


class EventAction : public G4UserEventAction {
public:
    EventAction(ConfigurationGeometry *);
    virtual ~EventAction();

public:
    virtual void BeginOfEventAction(const G4Event*);
    virtual void EndOfEventAction(const G4Event*);

private:
    std::vector<G4int> DHCID;

    EventActionMessenger *messenger;
    ConfigurationGeometry *geom;
    G4int verboseLevel;

public:
    inline void SetVerbose(G4int val) {
        verboseLevel = val;
    }
    inline G4int GetVerbose() const {
        return verboseLevel;
    }
    typedef std::vector<LGADSensorHitsCollection* > LGADSensorHitsCollections;
    CLHEP::HepRandomEngine* MyRndEngine;
    CLHEP::RandGauss* myGauss;
};


#endif
