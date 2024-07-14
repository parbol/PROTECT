#include <iomanip>
#include "PrimaryGeneratorAction.hh"
#include <sstream>
#include <sys/time.h>
#include <iostream>
#include <list>

#include "G4Event.hh"

using namespace std;



//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
PrimaryGeneratorAction::PrimaryGeneratorAction(ConfigurationGeometry *myGeom_, G4long randomSeed_, G4double pt_) {

    //Configuration information
    myGeom = myGeom_;
    randomSeed = randomSeed_;  
    
    //Particle gun
    G4String particleName;
    particleGun = new G4ParticleGun();
    MyRndEngine = CLHEP::HepRandom::getTheEngine();
    MyRndEngine->setSeed(randomSeed, 1);
    // Create the table containing all particle names
    particleTable = G4ParticleTable::GetParticleTable();
    fProton = particleTable->FindParticle(particleName="proton");
    particleGun->SetParticlePosition(G4ThreeVector(0.,0.,0));
    particleGun->SetParticleDefinition(fProton);

    //Beam
    beam = new Beam(myGeom, MyRndEngine);

    // Create the messenger file
    gunMessenger = new PrimaryGeneratorMessenger(this);

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Destructuor                                                          //
//----------------------------------------------------------------------//
PrimaryGeneratorAction::~PrimaryGeneratorAction() {
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Real generation of the primaries                                     //
//----------------------------------------------------------------------//
void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent) {

    G4int maxParticles = beam->GetNParticles();
       
    for ( unsigned j=0; j< maxParticles; j++) {
        
	    particleGun->SetParticleDefinition(fProton);
	    std::vector<G4double> vect = beam->fireParticle();
        //Momentum
        particleGun->SetParticleMomentum(vect[0]);
        particleGun->SetParticlePosition(G4ThreeVector(vect[1], vect[2], vect[3]));
        particleGun->SetParticleTime(vect[4]);
        particleGun->SetParticleMomentumDirection(G4ThreeVector(vect[5], vect[6], vect[7]));
        particleGun->GeneratePrimaryVertex(anEvent);

        
    }

    beam->updateBeam();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

