#include "PrimaryGeneratorMessenger.hh"

#include "PrimaryGeneratorAction.hh"
#include "G4UIdirectory.hh"
#include "G4UIcmdWithAString.hh"
#include "G4UIcmdWithoutParameter.hh"


//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
PrimaryGeneratorMessenger::PrimaryGeneratorMessenger(PrimaryGeneratorAction* Gun):Action(Gun) {


    MessInput = new std::string;

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Destructor                                                           //
//----------------------------------------------------------------------//
PrimaryGeneratorMessenger::~PrimaryGeneratorMessenger() {
    delete InputCmd;
    delete UpdateCmd;
    delete FileCmd;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// ?????????                                                            //
//----------------------------------------------------------------------//
void PrimaryGeneratorMessenger::SetNewValue(G4UIcommand* command, G4String newValue) {

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

