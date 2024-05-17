#ifndef LGADSensorHit_h
#define LGADSensorHit_h 1

#include "G4VHit.hh"
#include "G4THitsCollection.hh"
#include "G4Allocator.hh"
#include "G4ThreeVector.hh"
#include "G4LogicalVolume.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"

class G4AttDef;
class G4AttValue;

class LGADSensorHit : public G4VHit
{
public:

    LGADSensorHit();
    virtual ~LGADSensorHit();
    LGADSensorHit(const LGADSensorHit &right);
    const LGADSensorHit& operator=(const LGADSensorHit &right);
    int operator==(const LGADSensorHit &right) const;

    inline void *operator new(size_t);
    inline void operator delete(void *aHit);

    inline float x();
    inline float y();

    virtual const std::map<G4String,G4AttDef>* GetAttDefs() const;
    virtual std::vector<G4AttValue>* CreateAttValues() const;
    virtual void Print();

private:
    G4int eventNumber;
    G4int detectorID;
    G4int layerID;
    G4int lgadID;
    G4double gentoa;
    G4double gentot;
    G4double toa;
    G4double tot;
    G4double energy;
    G4int padx;
    G4int pady;
    G4ThreeVector localPos;
    G4ThreeVector globalPos;
    

public:
    inline void SetEventNumber(G4int z) {
        eventNumber = z;
    }
    inline G4int GetEventNumber() const {
        return eventNumber;
    }
    inline void SetDetectorID(G4int z) {
        detectorID = z;
    }
    inline G4int GetDetectorID() const {
        return detectorID;
    }
    inline void SetLayerID(G4int z) {
        layerID = z;
    }
    inline G4int GetLayerID() const {
        return layerID;
    }
     inline void SetLGADID(G4int z) {
        lgadID = z;
    }
    inline G4int GetLGADID() const {
        return lgadID;
    }
    inline void SetGenTOA(G4double t) {
        gentoa = t;
    }
    inline G4double GetGenTOA() const {
        return gentoa;
    }
    inline void SetGenTOT(G4double t) {
        gentot = t;
    }
    inline G4double GetGenTOT() const {
        return gentot;
    }
    inline void SetTOA(G4double t) {
        toa = t;
    }
    inline G4double GetTOA() const {
        return toa;
    }
    inline void SetTOT(G4double t) {
        tot = t;
    }
    inline G4double GetTOT() const {
        return tot;
    }
    inline void SetPadx(G4int t) {
        padx = t;
    }
    inline G4int GetPadx() const {
        return padx;
    }
    inline void SetPady(G4int t) {
        pady = t;
    }
    inline G4int GetPady() const {
        return pady;
    }
    inline void SetEnergy(G4double t) {
        energy = t;
    }
    inline G4double GetEnergy() const {
        return energy;
    }
    inline void SetLocalPos(G4ThreeVector xyz) {
        localPos = xyz;
    }
    inline G4ThreeVector GetLocalPos() const {
        return localPos;
    }
    inline void SetGlobalPos(G4ThreeVector xyz) {
        globalPos = xyz;
    }
    inline G4ThreeVector GetGlobalPos() const {
        return globalPos;
    }
    

};


//----------------------------------------------------------------------//
// Collections of this                                                  //
//----------------------------------------------------------------------//
typedef G4THitsCollection<LGADSensorHit> LGADSensorHitsCollection;

extern G4Allocator<LGADSensorHit> LGADSensorHitAllocator;
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Redefinition of new operator                                         //
//----------------------------------------------------------------------//
inline void* LGADSensorHit::operator new(size_t) {
    void* aHit;
    aHit = (void*)LGADSensorHitAllocator.MallocSingle();
    return aHit;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Redefinition of delete operator                                      //
//----------------------------------------------------------------------//
inline void LGADSensorHit::operator delete(void* aHit) {
    LGADSensorHitAllocator.FreeSingle((LGADSensorHit*) aHit);
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

#endif


