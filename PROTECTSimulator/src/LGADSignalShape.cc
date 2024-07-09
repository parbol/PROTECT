#include "LGADSignalShape.hh"
#include <array>

#define qNSecPerBin 0.01


//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
LGADSignalShape::LGADSignalShape(G4double thres) {

    threshold = thres;

    //Estimate the time and value of the maximum
    for(G4int i = 1; i < sizeof(signalShape)/sizeof(G4double); i++) {      
        if(signalShape[i] < signalShape[i-1]) {
            maxN = i-1;
            break;
        }
    }
    maxValue = signalShape[maxN];
    timeMax = maxN * qNSecPerBin;

    //Estimate the falling time
    for(G4int i = 1; i < sizeof(signalShape)/sizeof(G4double); i++) { 
        if(signalShape[i] == 0 && signalShape[i-1] != 0) {
            maxN = i;
            break;
        }
    }
    fallValue = maxN * qNSecPerBin;

};
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// getMaximum value                                                     //
//----------------------------------------------------------------------//
G4double LGADSignalShape::maximum() {return maxValue;}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// get Time of maximum                                                  //
//----------------------------------------------------------------------//
G4double LGADSignalShape::timeOfMax() {return timeMax;}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// get falling time                                                     //
//----------------------------------------------------------------------//
G4double LGADSignalShape::fallTime() {return fallValue;}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// getTimes                                                             //
//----------------------------------------------------------------------//
std::pair<G4double, G4double> LGADSignalShape::getTimes(G4double charge) {
    std::pair<G4double, G4double> mypair;
    G4int iArrival, iEnd;
    for(G4int i = 0; i < maxN; i++) {
        if(signalShape[i]*charge > threshold) {
            iArrival = i;
            break;
        }
    }
    if(iArrival == maxN) {
        mypair = std::make_pair(0.0, 0.0);
        return mypair;
    }
    for(G4int i = maxN; i >= 0; i--) {
        if(signalShape[i]*charge > threshold) {
            iEnd = i;
            break;
        }
    }
    mypair = std::make_pair(iArrival*qNSecPerBin, (iEnd-iArrival)*qNSecPerBin);
    return mypair;
}


