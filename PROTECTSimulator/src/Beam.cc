#include "Beam.hh"

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
    myPoiss = new CLHEP::RandPoisson(MyRndEngine);

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

    vect.push_back(p);
    vect.push_back(x);
    vect.push_back(y);
    vect.push_back(z);
    vect.push_back(t);
    vect.push_back(vx);
    vect.push_back(vy);
    vect.push_back(vz);      

    if(debug) {
        G4cout << "Gen Particle x: " << x/CLHEP::cm << " cm, y: " << y/CLHEP::cm << " cm, z: " << z/CLHEP::cm << " cm, vx: " << vx << ", vy: " << vy << ", vz: " << vz << ", p: " << p/CLHEP::MeV << G4endl;
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

