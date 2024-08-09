#include "ModularPhysicsList.hh"
#include "globals.hh"

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

#include "G4EmStandardPhysics.hh"
#include "G4EmExtraPhysics.hh"
#include "G4DecayPhysics.hh"
#include "G4HadronElasticPhysicsPHP.hh"
//#include "G4HadronPhysicsQGSP_BIC.hh"
#include "G4HadronPhysicsFTFP_BERT_HP.hh"
#include "G4StoppingPhysics.hh"
#include "G4IonPhysics.hh"
#include "G4NeutronTrackingCut.hh"
#include "G4RadioactiveDecayPhysics.hh"
#include "G4IonBinaryCascadePhysics.hh"


//https://ceiden.com/wp-content/uploads/2022/06/011-EMendoza_Protontherapy_WPE_v01.pdf
//----------------------------------------------------------------------//
// The constructor                                                      //
//----------------------------------------------------------------------//
MyPhysicsList::MyPhysicsList() : G4VModularPhysicsList() {

	RegisterPhysics( new G4EmStandardPhysics );
	RegisterPhysics( new G4EmExtraPhysics );
	RegisterPhysics( new G4DecayPhysics );
	RegisterPhysics( new G4HadronElasticPhysicsPHP );
	RegisterPhysics( new G4HadronPhysicsFTFP_BERT_HP );
	RegisterPhysics( new G4StoppingPhysics );
	RegisterPhysics( new G4IonPhysics );
	RegisterPhysics( new G4NeutronTrackingCut );     
	RegisterPhysics( new G4RadioactiveDecayPhysics);  


}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// The destructor                                                       //
//----------------------------------------------------------------------//
MyPhysicsList::~MyPhysicsList() {}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//



