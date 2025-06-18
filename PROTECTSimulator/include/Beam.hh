#ifndef Beam_h
#define Beam_h 1

#include "Randomize.hh"
#include "ConfigurationGeometry.hh"
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"


class Beam {

public:

    Beam(ConfigurationGeometry *, CLHEP::HepRandomEngine*);
    std::vector<G4double> fireParticle();
    void updateBeam();
    G4int GetNParticles();

private:
 
    ConfigurationGeometry *myGeom;
    CLHEP::HepRandomEngine* MyRndEngine;
    CLHEP::RandGauss* myGauss;
    CLHEP::RandPoisson* myPoiss;

    G4RotationMatrix rot;
    G4double vx, vy, vz;
    G4double step;
    G4int debug;
};



#endif

