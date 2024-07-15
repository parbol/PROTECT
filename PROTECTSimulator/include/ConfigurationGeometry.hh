//------------------------------------------------------------//
// |__   __/ __ \|  \/  | |  | | |    / ____|   /\   |  __ \  //
//    | | | |  | | \  / | |  | | |   | |  __   /  \  | |  | | //
//    | | | |  | | |\/| | |  | | |   | | |_ | / /\ \ | |  | | //
//    | | | |__| | |  | | |__| | |___| |__| |/ ____ \| |__| | //
//    |_|  \____/|_|  |_|\____/|______\_____/_/    \_\_____/  //
//------------------------------------------------------------//
// ConfigurationGeometry class:                               //                                                           
//                                                            //
// Parses json files with the configuration of the detectors. //
//                                                            //
//------------------------------------------------------------//

#ifndef ConfigurationGeometry_h
#define ConfigurationGeometry_h 1

#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include "assert.h"

#include "globals.hh"
#include "Detector.hh"
#include "Layer.hh"
#include "LGAD.hh"
#include "Gantry.hh"

class ConfigurationGeometry {

public:

    ConfigurationGeometry(G4String);
    
    bool isGood();

    // Information about the GEANT4 universe 
    G4double getSizeX();
    G4double getSizeY();
    G4double getSizeZ();
   
    // Informatio about the BEAM
    G4double GetXBeamPosition();
    G4double GetXBeamSigma();
    G4double GetYBeamPosition();
    G4double GetYBeamSigma();
    G4double GetZBeamPosition();
    G4double GetMomentum();
    G4int GetNStep();
    G4double GetMomentumSigma();
    G4double GetTBeamSigma();
    G4int GetMomentumDistribution();
    G4int GetNParticles();
    G4int GetParticleDistribution();
    G4double GetMaxOpenAngle();


    // Detector information
    Detector *getDetector(G4int);
    G4int getNDetectors();

    // Gantry information
    Gantry *getGantry();
    
    //Creating the geometry
    void createG4objects(G4LogicalVolume *, 
                         std::map<G4String, G4Material*> &,
                         G4SDManager *);
    // Detector collections
    void registerCollection(G4String);
    std::vector <G4String> collections;
    
    void Print();

private:

    G4double xBeamPosition, xBeamSigma;
    G4double yBeamPosition, yBeamSigma;
    G4double zBeamPosition;
    G4double p, pSigma;
    G4double tBeamSigma;
    G4double maxOpenAngle;
    G4int nParticles, nStep;
    G4int momentumDistribution, particleDistribution;

    G4double uniSizeX, uniSizeY, uniSizeZ;
    Gantry *gantry;
    std::vector <Detector *> detectors;
    bool goodGeometry;
    LGADSignalShape *signalShape;
};



#endif

