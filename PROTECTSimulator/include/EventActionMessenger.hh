#ifndef EventActionMessenger_h
#define EventActionMessenger_h 1

class EventAction;
class G4UIcmdWithAnInteger;

#include "G4UImessenger.hh"
#include "globals.hh"

class EventActionMessenger: public G4UImessenger
{
public:
    EventActionMessenger(EventAction* mpga);
    ~EventActionMessenger();

public:
    void SetNewValue(G4UIcommand * command,G4String newValues);
    G4String GetCurrentValue(G4UIcommand * command);

private:
    EventAction* target;

private: //commands
    G4UIcmdWithAnInteger*  verboseCmd;

};

#endif


