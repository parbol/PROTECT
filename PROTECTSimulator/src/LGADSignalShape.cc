#include "LGADSignalShape.hh"
#include <array>



//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
LGADSignalShape::LGADSignalShape(G4double thres) {

    threshold = thres;
       
    for(G4int i = 1; i < sizeof(signalShape)/sizeof(G4double); i++) {
        if(signalShape[i] == 0 && signalShape[i-1] != 0) {
            maxN = i;
            break;
        }
    }

};
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
    mypair = std::make_pair(iArrival, iEnd-iArrival);
    return mypair;
}


