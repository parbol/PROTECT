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
    
    G4String particleName;
    particleGun = new G4ParticleGun();

    //Information of the beam    
    timeSimulated = 0.0;
    vx = -myGeom->GetMaxOpenAngle();
    vy = -myGeom->GetMaxOpenAngle();
    vz = -1.0;
    step = 2.0 * myGeom->GetMaxOpenAngle() / (G4double) myGeom->GetNStep();
    
    MyRndEngine = CLHEP::HepRandom::getTheEngine();
    MyRndEngine->setSeed(randomSeed_,1);
    myGauss = new CLHEP::RandGauss(MyRndEngine);
    myPoiss = new CLHEP::RandPoisson(MyRndEngine);

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
    
    G4int maxParticles;
    //Poisson
    if(myGeom->GetParticleDistribution() == 1) {
        maxParticles = myPoiss->fire(myGeom->GetNParticles());
    } else{
        maxParticles = myGeom->GetNParticles();
    }
    
    for ( unsigned j=0; j< maxParticles; j++) {
        
	particleGun->SetParticleDefinition(fProton);
	G4double mass = particleGun->GetParticleDefinition()->GetPDGMass() * CLHEP::MeV;
        G4double p; 
        //Gauss
        if(myGeom->GetMomentumDistribution() == 2) {
            p = myGauss->fire(myGeom->GetMomentum(), myGeom->GetMomentumSigma()) * CLHEP::MeV;
        } else{
            p = myGeom->GetMomentum() * CLHEP::MeV;
        }
        G4double e = std::sqrt(p * p + mass * mass);
    	particleGun->SetParticleEnergy(e);
	
        G4double x = myGauss->fire(myGeom->GetXBeamPosition(), myGeom->GetXBeamSigma()) * CLHEP::cm;
        G4double y = myGauss->fire(myGeom->GetYBeamPosition(), myGeom->GetYBeamSigma()) * CLHEP::cm;
        G4double z = myGeom->GetZBeamPosition() * CLHEP::cm;     
        G4double t = myGauss->fire(0.0, myGeom->GetTBeamSigma()) * CLHEP::ns; //cuidado con las unidades

        particleGun->SetParticlePosition(G4ThreeVector(x, y, z));
        particleGun->SetParticleMomentumDirection(G4ThreeVector(vx, vy, vz));
        particleGun->SetParticleTime(t);
        particleGun->GeneratePrimaryVertex(anEvent);
    }

    if(vx < myGeom->GetMaxOpenAngle()) {
        vx = vx + step;
    } else {
        vx = -myGeom->GetMaxOpenAngle();
        if(vy < myGeom->GetMaxOpenAngle()) {
            vy = vy + step;
        } else {
            vy = -myGeom->GetMaxOpenAngle();
        }
    }
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

