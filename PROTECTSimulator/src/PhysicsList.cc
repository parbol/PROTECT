#include "globals.hh"
#include "PhysicsList.hh"

#include "G4ParticleDefinition.hh"
#include "G4ParticleWithCuts.hh"
#include "G4ProcessManager.hh"
#include "G4ProcessVector.hh"
#include "G4ParticleTypes.hh"
#include "G4ParticleTable.hh"
#include "G4Material.hh"
#include "G4MaterialTable.hh"
#include "G4ios.hh"
#include <iomanip>


//----------------------------------------------------------------------//
// The constructor                                                      //
//----------------------------------------------------------------------//
PhysicsList::PhysicsList():  G4VUserPhysicsList() {
    defaultCutValue = 1.*CLHEP::mm;
    SetVerboseLevel(3);
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// The destructor                                                       //
//----------------------------------------------------------------------//
PhysicsList::~PhysicsList() {}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Construct all the particles                                          //
//----------------------------------------------------------------------//
void PhysicsList::ConstructParticle() {
    // In this method, static member functions should be called
    // for all particles which you want to use.
    // This ensures that objects of these particle types will be
    // created in the program.

    ConstructBosons();
    ConstructLeptons();
    ConstructMesons();
    ConstructBaryons();
    ConstructIons();

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// The Bosons                                                           //
//----------------------------------------------------------------------//
void PhysicsList::ConstructBosons() {
    // pseudo-particles
    G4Geantino::GeantinoDefinition();
    G4ChargedGeantino::ChargedGeantinoDefinition();

    // gamma
    G4Gamma::GammaDefinition();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// The leptons                                                          //
//----------------------------------------------------------------------//
void PhysicsList::ConstructLeptons() {
    // leptons
    G4Electron::ElectronDefinition();
    G4Positron::PositronDefinition();
    G4MuonPlus::MuonPlusDefinition();
    G4MuonMinus::MuonMinusDefinition();

    G4NeutrinoE::NeutrinoEDefinition();
    G4AntiNeutrinoE::AntiNeutrinoEDefinition();
    G4NeutrinoMu::NeutrinoMuDefinition();
    G4AntiNeutrinoMu::AntiNeutrinoMuDefinition();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Mesons                                                               //
//----------------------------------------------------------------------//
void PhysicsList::ConstructMesons() {
//  mesons
    G4PionPlus::PionPlusDefinition();
    G4PionMinus::PionMinusDefinition();
    G4PionZero::PionZeroDefinition();
    G4Eta::EtaDefinition();
    G4EtaPrime::EtaPrimeDefinition();
    G4KaonPlus::KaonPlusDefinition();
    G4KaonMinus::KaonMinusDefinition();
    G4KaonZero::KaonZeroDefinition();
    G4AntiKaonZero::AntiKaonZeroDefinition();
    G4KaonZeroLong::KaonZeroLongDefinition();
    G4KaonZeroShort::KaonZeroShortDefinition();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Barions.cc                                                           //
//----------------------------------------------------------------------//
void PhysicsList::ConstructBaryons() {
//  baryons
    G4Proton::ProtonDefinition();
    G4AntiProton::AntiProtonDefinition();
    G4Neutron::NeutronDefinition();
    G4AntiNeutron::AntiNeutronDefinition();

    G4Lambda::LambdaDefinition();
    G4AntiLambda::AntiLambdaDefinition();
    G4SigmaPlus::SigmaPlusDefinition();
    G4SigmaMinus::SigmaMinusDefinition();
    G4SigmaZero::SigmaZeroDefinition();
    G4AntiSigmaZero::AntiSigmaZeroDefinition();
    G4XiZero::XiZeroDefinition();
    G4AntiXiZero::AntiXiZeroDefinition();
    G4XiMinus::XiMinusDefinition();
    G4AntiXiMinus::AntiXiMinusDefinition();
    G4OmegaMinus::OmegaMinusDefinition();
    G4AntiOmegaMinus::AntiOmegaMinusDefinition();

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Ions                                                                 //
//----------------------------------------------------------------------//
void PhysicsList::ConstructIons() {
    //  nuclei
    G4Alpha::AlphaDefinition();
    G4Deuteron::DeuteronDefinition();
    G4Triton::TritonDefinition();
    G4He3::He3Definition();
    //  generic ion
    G4GenericIon::GenericIonDefinition();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Processes                                                            //
//----------------------------------------------------------------------//
void PhysicsList::ConstructProcess() {
    AddTransportation();
    ConstructGeneral();
    ConstructInteractions();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


#include "G4Decay.hh"

void PhysicsList::ConstructGeneral() {

    G4Decay* theDecayProcess = new G4Decay();
    auto theParticleIterator=GetParticleIterator();
    theParticleIterator->reset();
    while( (*theParticleIterator)() ) {
        G4ParticleDefinition* particle = theParticleIterator->value();
        G4ProcessManager* pmanager = particle->GetProcessManager();
        if (theDecayProcess->IsApplicable(*particle)) {
            pmanager->AddDiscreteProcess(theDecayProcess);
        }
    }
}



// gamma
#include "G4PhotoElectricEffect.hh"
#include "G4ComptonScattering.hh"
#include "G4PolarizedCompton.hh"
#include "G4GammaConversion.hh"
// e-
// e+
#include "G4eMultipleScattering.hh"
#include "G4eIonisation.hh"
#include "G4eBremsstrahlung.hh"
#include "G4eplusAnnihilation.hh"
// muon
#include "G4MuMultipleScattering.hh"
#include "G4MuIonisation.hh"
#include "G4MuBremsstrahlung.hh"
#include "G4MuPairProduction.hh"
#include "G4hMultipleScattering.hh"
#include "G4hIonisation.hh"


//----------------------------------------------------------------------//
// Define interactions                                                  //
//----------------------------------------------------------------------//
void PhysicsList::ConstructInteractions() {

    auto theParticleIterator=GetParticleIterator();
    theParticleIterator->reset();
    while( (*theParticleIterator)() ) {
        G4ParticleDefinition* particle = theParticleIterator->value();
        G4ProcessManager* pmanager = particle->GetProcessManager();
        G4String particleName = particle->GetParticleName();

        if (particleName == "gamma") {
            // Standard classes
            pmanager->AddDiscreteProcess(new G4PhotoElectricEffect());
            pmanager->AddDiscreteProcess(new G4ComptonScattering());
            pmanager->AddDiscreteProcess(new G4PolarizedCompton());
            pmanager->AddDiscreteProcess(new G4GammaConversion());
        } else if (particleName == "e-") {
            // Standard classes:
            pmanager->AddProcess(new G4eMultipleScattering(),-1, 1,1);
            pmanager->AddProcess(new G4eIonisation(),       -1, 2,2);
            pmanager->AddProcess(new G4eBremsstrahlung(),   -1,-1,3);

        } else if (particleName == "e+") {
            // Standard classes:
            pmanager->AddProcess(new G4eMultipleScattering(),-1, 1,1);
            pmanager->AddProcess(new G4eIonisation(),       -1, 2,2);
            pmanager->AddProcess(new G4eBremsstrahlung(),   -1,-1,3);
            pmanager->AddProcess(new G4eplusAnnihilation(),  0,-1,4);

        } else if( particleName == "mu+" ||
                   particleName == "mu-"    ) {
            //muon
            // Construct processes for muon+
            pmanager->AddProcess(new G4MuMultipleScattering(),-1,1,1);
            pmanager->AddProcess(new G4MuIonisation(),-1,2,2);
            pmanager->AddProcess(new G4MuBremsstrahlung(),-1,-1,3);
            pmanager->AddProcess(new G4MuPairProduction(),-1,-1,4);

        } else if( particleName == "GenericIon" ) {
            pmanager->AddProcess(new G4hMultipleScattering(),-1,1,1);
            pmanager->AddProcess(new G4hIonisation(),-1,2,2);
        } else {
            if ((particle->GetPDGCharge() != 0.0) &&
                    (particle->GetParticleName() != "chargedgeantino")&&
                    (!particle->IsShortLived()) ) {
                // all others charged particles except geantino
                pmanager->AddProcess(new G4hMultipleScattering(),-1,1,1);
                pmanager->AddProcess(new G4hIonisation(),-1,2,2);
            }
        }
    }
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Set cuts for the simulation of particles                             //
//----------------------------------------------------------------------//
void PhysicsList::SetCuts() {
    SetCutsWithDefault();
    if (verboseLevel > 0) DumpCutValuesTable();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

