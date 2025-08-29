#include "Beam.hh"
#include "G4ThreeVector.hh"

//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
Beam::Beam(ConfigurationGeometry *g, CLHEP::HepRandomEngine* MyRndEngine_) {

    myGeom = g;
    debug = 1;
    //Information of the beam    
    vx = -myGeom->GetMaxOpenAngle();
    vy = -myGeom->GetMaxOpenAngle();
    vz = -1.0;
    step = 2.0 * myGeom->GetMaxOpenAngle() / (G4double) myGeom->GetNStep();
    MyRndEngine = MyRndEngine_;
    myGauss = new CLHEP::RandGauss(MyRndEngine);
    G4RotationMatrix auxrot;
    auxrot.rotateX(g->GetXDirBeam());
    auxrot.rotateY(g->GetYDirBeam());
    rot = auxrot.inverse();

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Number of particles in beam                                          //
//----------------------------------------------------------------------//
G4int Beam::GetNParticles() {

    //Poisson
    G4int maxParticles;
    if(myGeom->GetParticleDistribution() == 1) {
        maxParticles = myPoiss->fire(myGeom->GetNParticles());
    } else{
        maxParticles = myGeom->GetNParticles();
    }
    return maxParticles;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Create a new particle                                                //
//----------------------------------------------------------------------//
std::vector<G4double> Beam::fireParticle() {

    std::vector<G4double> vect;
    G4double p; 
    //Gauss
    if(myGeom->GetMomentumDistribution() == 2) {
        p = myGauss->fire(myGeom->GetMomentum(), myGeom->GetMomentumSigma()) * CLHEP::MeV;
    } else{
        p = myGeom->GetMomentum() * CLHEP::MeV;
    }
    G4double x = myGauss->fire(myGeom->GetXBeamPosition(), myGeom->GetXBeamSigma()) * CLHEP::cm;
    G4double y = myGauss->fire(myGeom->GetYBeamPosition(), myGeom->GetYBeamSigma()) * CLHEP::cm;
    G4double z = myGeom->GetZBeamPosition() * CLHEP::cm;     
    G4double t = myGauss->fire(0.0, myGeom->GetTBeamSigma()) * CLHEP::ns; //cuidado con las unidades

    G4ThreeVector pos, dir;
    pos.setX(x); 
    pos.setY(y); 
    pos.setZ(z);
    dir.setX(vx); 
    dir.setY(vy); 
    dir.setZ(vz);
    
    G4ThreeVector newpos = rot * pos;
    G4ThreeVector newdir = rot * dir;

    vect.push_back(p);
    vect.push_back(newpos.getX());
    vect.push_back(newpos.getY());
    vect.push_back(newpos.getZ());
    vect.push_back(t);
    vect.push_back(newdir.getX());
    vect.push_back(newdir.getY());
    vect.push_back(newdir.getZ());      

    if(debug) {
        G4cout << "Gen Particle x: " << x/CLHEP::cm << " cm, y: " << y/CLHEP::cm << " cm, z: " << z/CLHEP::cm << " cm, vx: " << vx << ", vy: " << vy << ", vz: " << vz << ", p: " << p/CLHEP::MeV << G4endl;
        G4cout << "Real Gen Particle x: " << newpos.getX()/CLHEP::cm << " cm, y: " << newpos.getY()/CLHEP::cm << " cm, z: " << newpos.getZ()/CLHEP::cm << " cm, vx: " << newdir.getX() << ", vy: " << newdir.getY() << ", vz: " << newdir.getZ() << ", p: " << p/CLHEP::MeV << G4endl;
    } 
    
    return vect;

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Update beam                                                          //
//----------------------------------------------------------------------//
void Beam::updateBeam() {

    if(vx < myGeom->GetMaxOpenAngle()) {
        vx = vx + step;
    } else {
        vx = -myGeom->GetMaxOpenAngle();
        if(vy < myGeom->GetMaxOpenAngle()) {
            vy = vy + step;
        } else {
            vy = -myGeom->GetMaxOpenAngle();
        }
    }
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//



