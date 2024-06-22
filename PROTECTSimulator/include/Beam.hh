#ifndef LGAD_h
#define LGAD_h 1

#include "Randomize.hh"
#include "ConfigurationGeometry.hh"


class Beam {

public:

    Beam(ConfigurationGeometry *, CLHEP::HepRandomEngine*);
    std::vector<G4double> fireParticle();
    void updateBeam();

private:
 
    ConfigurationGeometry *myGeom;
    CLHEP::HepRandomEngine* MyRndEngine;
    CLHEP::RandGauss* myGauss;
    CLHEP::RandPoisson* myPoiss;

    G4double vx, vy, vz;
    G4double step;
};



#endif

