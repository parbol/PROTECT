#ifndef PrimaryGeneratorAction_h
#define PrimaryGeneratorAction_h 1

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4ThreeVector.hh"
#include "G4DataVector.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleGun.hh"
#include "Randomize.hh"
#include "globals.hh"
#include "ConfigurationGeometry.hh"
#include "vector"
#include "RNGWrapper.hh"
#include "PrimaryGeneratorMessenger.hh"
#include "Beam.hh"

class G4Event;

class PrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction
{
public:
    PrimaryGeneratorAction(ConfigurationGeometry *, G4long, G4double);
    ~PrimaryGeneratorAction();

public:
    void GeneratePrimaries(G4Event* anEvent);
    G4double timeSimulated;

private:
    G4ParticleTable* particleTable;
    G4ParticleGun* particleGun;
    G4ParticleDefinition* fProton;
    G4int InputState;
    PrimaryGeneratorMessenger* gunMessenger;
    ConfigurationGeometry *myGeom;
    G4long randomSeed;
    CLHEP::HepRandomEngine* MyRndEngine;
    CLHEP::RandGauss* myGauss;
    CLHEP::RandPoisson* myPoiss;
    G4double step;
    G4double vx, vy, vz;
    Beam *beam;
};

#endif
