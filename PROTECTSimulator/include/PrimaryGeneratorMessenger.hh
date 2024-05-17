#ifndef PrimaryGeneratorMessenger_h
#define PrimaryGeneratorMessenger_h 1

#include "G4UImessenger.hh"
#include "globals.hh"

class PrimaryGeneratorAction;
class G4UIdirectory;
class G4UIcmdWithAString;
class G4UIcmdWithoutParameter;


class PrimaryGeneratorMessenger: public G4UImessenger {
public:
    PrimaryGeneratorMessenger(PrimaryGeneratorAction *);
    ~PrimaryGeneratorMessenger();

    void SetNewValue(G4UIcommand*, G4String);

private:
    PrimaryGeneratorAction*      Action;
    G4UIdirectory*               CRYDir;
    G4UIcmdWithAString*          FileCmd;
    G4UIcmdWithAString*          InputCmd;
    G4UIcmdWithoutParameter*     UpdateCmd;
    std::string* MessInput;
};


#endif

