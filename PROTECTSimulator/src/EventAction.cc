#include "EventAction.hh"
#include "EventActionMessenger.hh"

#include "G4AnalysisManager.hh"

#include "Analysis.hh"
#include "G4Run.hh"
#include "G4Event.hh"
#include "G4EventManager.hh"
#include "G4HCofThisEvent.hh"
#include "G4VHitsCollection.hh"
#include "G4TrajectoryContainer.hh"
#include "G4Trajectory.hh"
#include "G4VVisManager.hh"
#include "G4SDManager.hh"
#include "G4UImanager.hh"
#include "G4ios.hh"

#include "LGADSensorHit.hh"

#include "ConfigurationGeometry.hh"

#include <math.h>

#include <iostream>
#include <map>

#define PI 3.141592653589793238462643383279502884



//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
EventAction::EventAction(ConfigurationGeometry *geom_) {

    geom = geom_;
    G4String colName;
    G4SDManager* SDman = G4SDManager::GetSDMpointer();
    G4int numberOfDetectors = SDman->GetCollectionCapacity();
    SDman->ListTree();
    MyRndEngine = CLHEP::HepRandom::getTheEngine();
    myGauss = new CLHEP::RandGauss(MyRndEngine);

    for(auto i : geom->collections) {
        DHCID.push_back(SDman->GetCollectionID(i));
    }
    messenger = new EventActionMessenger(this);

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Destructor                                                           //
//----------------------------------------------------------------------//
EventAction::~EventAction() {
    delete messenger;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//



//----------------------------------------------------------------------//
// Begin of the event                                                   //
//----------------------------------------------------------------------//
void EventAction::BeginOfEventAction(const G4Event*) {}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// End of the event -> the action goes here                             //
//----------------------------------------------------------------------//
void EventAction::EndOfEventAction(const G4Event* evt) {

    std::map<G4int, LGADDigi*> digis;

    auto man = G4AnalysisManager::Instance();
    G4HCofThisEvent * HCE = evt->GetHCofThisEvent();
    
    std::vector<LGADSensorHitsCollections> DHCs;
    //G4SDManager* SDman = G4SDManager::GetSDMpointer();
    if(HCE) {
        for (auto i : DHCID) {
            LGADSensorHitsCollection *a = 0;
            a = (LGADSensorHitsCollection*)(HCE->GetHC(i));
            LGADSensorHitsCollections DHCcoll;
            DHCcoll.push_back(a);
            DHCs.push_back(DHCcoll);
        }
        for (auto i : DHCs) {
            if(i.at(0)) {
                G4int n_hit = i.at(0)->entries();
                for(G4int hit = 0; hit < n_hit; hit++) {
                    LGADSensorHit* aHit = (*(i.at(0)))[hit];
                    if(aHit->GetEnergy() == 0) continue;
                    auto detID = aHit->GetDetectorID();
                    auto layerID = aHit->GetLayerID();
                    auto lgadID = aHit->GetLGADID();
                    auto a = geom->getDetector(detID)->GetLayer(layerID)->GetSensor(lgadID);
                    auto sh = geom->getDetector(aHit->GetDetectorID())->GetLayer(aHit->GetLayerID())->GetSensor(aHit->GetLGADID())->signalShape();
                    LGADDigi *digi = new LGADDigi(aHit, 
                    geom->getDetector(aHit->GetDetectorID())->GetLayer(aHit->GetLayerID())->GetSensor(aHit->GetLGADID())->signalShape());
                    auto it = digis.find(digi->hitID);
                    if(it == digis.end()) {
                        digis.insert(std::make_pair(digi->hitID, digi));
                    } else {
                        it->second->charge += digi->charge;
                        it->second->TOA = (it->second->TOA < digi->TOA) ? it->second->TOA : digi->TOA;
                    }
                }
                    
            }
        }
    }
    
    for(auto i = digis.begin(); i != digis.end(); ++i) {
        if(i->second->Digitize(myGauss, geom)) {     
            man->FillNtupleIColumn(0, i->second->eventNumber);
            man->FillNtupleIColumn(1, i->second->GetDet());
            man->FillNtupleIColumn(2, i->second->GetLayer());
            man->FillNtupleIColumn(3, i->second->GetLGAD());
            man->FillNtupleIColumn(4, i->second->GetPadx());
            man->FillNtupleIColumn(5, i->second->GetPady());
            man->FillNtupleDColumn(6, i->second->TOA/CLHEP::ns);
            man->FillNtupleDColumn(7, i->second->TOT/CLHEP::ns);
            man->FillNtupleDColumn(8, i->second->charge);
            man->FillNtupleDColumn(9, i->second->genTOA/CLHEP::ns);
            man->FillNtupleDColumn(10, i->second->genTOT/CLHEP::ns);
            man->FillNtupleDColumn(11, i->second->genX/CLHEP::cm);
            man->FillNtupleDColumn(12, i->second->genY/CLHEP::cm);
            man->FillNtupleDColumn(13, i->second->genZ/CLHEP::cm);
            man->FillNtupleDColumn(14, i->second->genEnergy/CLHEP::MeV);
            man->FillNtupleIColumn(15, i->second->genID);
            man->AddNtupleRow(); 
        }
    }
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//
