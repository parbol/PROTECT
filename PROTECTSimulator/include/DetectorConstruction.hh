#ifndef DetectorConstruction_h
#define DetectorConstruction_h 1

#include "globals.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4RotationMatrix.hh"
#include "G4FieldManager.hh"
#include "ConfigurationGeometry.hh"

#include "G4LogicalVolume.hh"
#include "G4VPhysicalVolume.hh"
#include "G4Box.hh"


class G4VPhysicalVolume;
class G4Material;
class G4VSensitiveDetector;
class G4VisAttributes;
class DetectorConstMessenger;

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    DetectorConstruction(ConfigurationGeometry *);
    virtual ~DetectorConstruction();

public:
    virtual G4VPhysicalVolume* Construct();

private:
    void ConstructMaterials();
    void DestroyMaterials();
    void DumpGeometricalTree(G4VPhysicalVolume*, G4int);

private:
    DetectorConstMessenger* messenger;

    ConfigurationGeometry *myConf;

    std::map<G4String, G4Material*> materials;

};

#endif

