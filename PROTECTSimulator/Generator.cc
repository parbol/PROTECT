#include "G4RunManager.hh"
#include "G4UImanager.hh"

#include "RunAction.hh"
#include "EventAction.hh"
#include "DetectorConstruction.hh"
#include "ModularPhysicsList.hh"
#include "PrimaryGeneratorAction.hh"
#include "ConfigurationGeometry.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"



#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>

#include <iostream>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <linux/kd.h>


//----------------------------------------------------------------------//
// Methods defined in this file                                         //
//----------------------------------------------------------------------//

//Get options from the command line
bool getOptions(int , char **, G4String &, G4String &, G4String &, G4int &, G4long &, G4double &);

//Simply shows a cool propaganda banner
void showBanner();

//----------------------------------------------------------------------//
//----------------------------------------------------------------------//




//----------------------------------------------------------------------//
// Start of the program                                                 //
//----------------------------------------------------------------------//

int main(int argc,char** argv) {

    showBanner();

    G4String nameOfInputFile;
    G4String nameOfOutputFile;
    G4String nameOfGeantFile;
    G4int    numberOfEvents;
    G4long   randomSeed = 0;
	G4double pt = 0;
    //Options all right?
    if(!getOptions(argc, argv, nameOfInputFile, nameOfOutputFile, nameOfGeantFile, numberOfEvents, randomSeed, pt)) {
        G4cerr << "\033[1;31m" << "Usage: ./Generator --input NameOfGeometry.json --geant file.g4 --output outputfile --number numberOfEvents --seed seed --pt pt"  << "\033[0m" << G4endl;
        return -1;
    }

    //Number of events all right?
    if(numberOfEvents < 1) {
        G4cerr << "\033[1;31m" << "The number of events must be a positive integer greater than 0" << "\033[0m" << G4endl;
        return -1;
    }
 
    G4UIExecutive *ui = NULL;
    if(nameOfGeantFile != "") ui = new G4UIExecutive(argc, argv);


    //Initializing runManager
    G4RunManager* runManager = new G4RunManager;


    ConfigurationGeometry *geomConf = new ConfigurationGeometry(nameOfInputFile);
    if(!geomConf->isGood()) {
        G4cerr << "\033[1;31m" << "Problems in the configuration geometry file" << "\033[0m" << G4endl;
        return -1;
    }
    
    runManager->SetVerboseLevel(2);

    DetectorConstruction *myDetector = new DetectorConstruction(geomConf);
    if(myDetector == NULL) {
        G4cerr << "\033[1;31m" << "Problems in the construction of the detector" << "\033[0m" << G4endl;
        return -1;
    }

    
    runManager->SetUserInitialization(myDetector);
    
    MyPhysicsList *myPhysicsList = new MyPhysicsList();
    if(myPhysicsList == NULL) {
        G4cerr << "\033[1;31m" << "Problems in the physics list" << "\033[0m" << G4endl;
        return -1;
    }

    runManager->SetUserInitialization(myPhysicsList);

    PrimaryGeneratorAction *myPrimaryGeneratorAction = new PrimaryGeneratorAction(geomConf, randomSeed, pt);
    if(myPrimaryGeneratorAction == NULL) {
        G4cerr << "\033[1;31m" << "Problems in PrimaryGeneratorAction" << "\033[0m" << G4endl;
        return -1;
    }

    runManager->Initialize();

    runManager->SetUserAction(myPrimaryGeneratorAction);

    RunAction *myRunAction = new RunAction(nameOfOutputFile);
    if(myRunAction == NULL) {
        G4cerr << "\033[1;31m" << "Problems in RunAction" << "\033[0m" << G4endl;
        return -1;
    }

    runManager->SetUserAction(myRunAction);

    EventAction *myEventAction = new EventAction(geomConf);
    if(myEventAction == NULL) {
        G4cerr << "\033[1;31m" << "Problems in EventAction" << "\033[0m" << G4endl;
        return -1;
    }

    runManager->SetUserAction(myEventAction);


    G4VisManager* visManager = new G4VisExecutive;
    
    visManager->Initialize();
    G4UImanager* UImanager = G4UImanager::GetUIpointer();

    // Run or start UI session
    if ( ! ui ) {
        runManager->BeamOn(numberOfEvents);
    } else { 
        UImanager->ApplyCommand("/control/execute init_vis.mac");
        ui->SessionStart();
        delete ui;
    }

    delete geomConf;
    delete visManager;
    delete runManager;
    
    G4cout << "The program finished successfully" << G4endl;
    
    
    return 0;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//



//----------------------------------------------------------------------//
// This method will put the command line input in the variables.        //
//----------------------------------------------------------------------//
bool getOptions(int argc, char **argv, G4String &nameOfInputFile, G4String &nameOfOutputFile, G4String &nameOfGeantFile, G4int &numberOfEvents, G4long &randomSeed, G4double &pt) {

    int option_iterator;
    int option_counter = 0;
    bool moreoptions = true;

    while (moreoptions) {
        static struct option long_options[] = {
            /* These options set a flag. */
            {"input",     required_argument, 0, 'i'},
            {"output",    required_argument, 0, 'o'},
            {"seed",    required_argument, 0, 's'},
            {"number",    required_argument, 0, 'n'},
            {"geant",    required_argument, 0, 'g'},            
            {"pt",    required_argument, 0, 'p'},
            {0, 0, 0, 0}
        };
        int option_index = 0;
        option_iterator = getopt_long(argc, argv, "d:", long_options, &option_index);
        if (option_iterator == -1) {
            moreoptions = false;
        } else {
            option_counter++;
            switch (option_iterator) {
            case 0:
                if (long_options[option_index].flag != 0)
                    break;
                if (optarg)
                    break;
            case 'i':
                nameOfInputFile = (G4String) optarg;
                break;
            case 'o':
                nameOfOutputFile = (G4String) optarg;
                break;
            case 'n':
                numberOfEvents = (G4int) atoi(optarg);
                break;
            case 'g':
                nameOfGeantFile = (G4String) optarg;
                break;
            case 's':
                randomSeed = (G4long) atoi(optarg);
                break;
            case 'p':
                pt = (G4double) atof(optarg);
                break;
            case '?':
                return false;
                break;
            default:
                return false;
            }
        }
    }

    if (option_counter == 0) {
        return false;
    }
    return true;

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//




//----------------------------------------------------------------------//
// Just showing the banner.                                             //
//----------------------------------------------------------------------//

void showBanner() {

    G4cout << "\033[1;34m"
	   << "_______  _______  _______ _________ _______  _______ _________     " << G4endl
           << "(  ____ )(  ____ )(  ___  )\\__   __/(  ____ \\(  ____ \\\\__   __/    " << G4endl
           << "| (    )|| (    )|| (   ) |   ) (   | (    \\/| (    \\/   ) (       " << G4endl
           << "| (____)|| (____)|| |   | |   | |   | (__    | |         | |       " << G4endl
           << "|  _____)|     __)| |   | |   | |   |  __)   | |         | |       " << G4endl
           << "| (      | (\\ (   | |   | |   | |   | (      | |         | |       " << G4endl
           << "| )      | ) \\ \\__| (___) |   | |   | (____/\\| (____/\\   | |       " << G4endl
           << "|/       |/   \\__/(_______)   )_(   (_______/(_______/   )_(       " << G4endl
           << "                                                                   " << G4endl                                                            
           << "LGAD based proton tomography simulator (IFCA)                      " << G4endl
	   << "\033[0m"                                                  << G4endl;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

