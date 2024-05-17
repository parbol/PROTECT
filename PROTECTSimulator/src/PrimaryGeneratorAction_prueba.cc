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

    myGeom = myGeom_;
    randomSeed = randomSeed_;
    pt = pt_;

    G4String particleName;
    particleGun = new G4ParticleGun();
    timeSimulated=0.0;

    // Create the table containing all particle names
    particleTable = G4ParticleTable::GetParticleTable();
    fProton = particleTable->FindParticle(particleName="proton");
    particleGun->SetParticlePosition(G4ThreeVector(0.,0.,0));
    particleGun->SetParticleDefinition(fProton);

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

    G4String particleName;
    G4int maxParticles = 5;

    G4cout << "Hey youuuuuu" << G4endl;

    G4double xmin = -1.0;
    G4double xmax = 1.0;
    G4double step = (xmax-xmin)/maxParticles;
    for ( unsigned j=0; j< maxParticles; j++) {
        
	
        particleGun->SetParticleDefinition(fProton);
	G4double mass = particleGun->GetParticleDefinition()->GetPDGMass();
        G4double pt = 2000;
	G4cout << "Momentum: " << pt << "; mass " << mass << G4endl;
	particleGun->SetParticleEnergy(std::sqrt(pt*pt + mass*mass)*CLHEP::MeV);
	G4double x = (xmin + step * j)*CLHEP::cm;
	G4double y = 0.0*CLHEP::cm;
	G4double z = 120.0*CLHEP::cm;


        std::list<float> Xaxis;
        for (float i = -15; i = 15; ++i){
            Xaxis.push_back(i);
        }
        std::list<float> Yaxis;
        for (float i = -15; i = 15; ++i){
            Yaxis.push_back(i);
        }

        for (auto itery = Yaxis.begin(); iter != Yaxis.end(); ++itery){
            for (auto iterx = Xaxis.begin(); iter != Xaxis.end(); ++iterx){
            
	        G4double vx = *iterx/135;
	        G4double vy = *itery/135;
	        G4double vz = -1.0;
                G4double t = 0;
                particleGun->SetParticlePosition(G4ThreeVector(x, y, z));
                particleGun->SetParticleMomentumDirection(G4ThreeVector(vx, vy, vz));
                particleGun->SetParticleTime(t);
                particleGun->GeneratePrimaryVertex(anEvent);
    }
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

