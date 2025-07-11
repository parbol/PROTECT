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

#include "ConfigurationGeometry.hh"
#include <json/json.h>
#include <json/value.h>
#include "G4VisAttributes.hh"



//----------------------------------------------------------------------//
// Constructor                                                          //
//----------------------------------------------------------------------//
ConfigurationGeometry::ConfigurationGeometry(G4String file) {

    Json::Value root;
    Json::Reader reader;

    //We open the JSON file, read it and put it on a string
    std::stringstream  filecontent;
    std::ifstream infile(file.c_str());

    if(!(infile.good())) {
        G4cerr << "\033[1;31m" << "Error opening geometry file: " + file << "\033[0m" << G4endl;
        goodGeometry = false;
        return;
    }

    std::string currline;
    while(getline(infile,currline)) {
        filecontent<<currline;
    }

    infile.close();

    std::string FileContent=filecontent.str();

    //Parsing of the JSON file
    bool parsingSuccessful = reader.parse( FileContent, root );
    if ( !parsingSuccessful ) {
        G4cerr << "\033[1;31m" << "Error parsing file: " + file << "\033[0m" << G4endl;
        goodGeometry = false;
        return;
    }

    if( root.size() > 0 ) {
        //Definition of the Universe ----------------------------------------------
        G4double xSize = atof(root["theWorld"]["xSizeWorld"].asString().c_str());
        G4double ySize = atof(root["theWorld"]["ySizeWorld"].asString().c_str());
        G4double zSize = atof(root["theWorld"]["zSizeWorld"].asString().c_str());

        if(xSize <= 0 || ySize <= 0|| zSize <= 0) {
            G4cerr << "\033[1;31m" << "The size of the Universe has been greater than 0" << "\033[0m" << G4endl;
            goodGeometry = false;
            return;
        }

        uniSizeX = xSize * CLHEP::cm;
        uniSizeY = ySize * CLHEP::cm;
        uniSizeZ = zSize * CLHEP::cm;

        //Definition of the beam---------------------------------------
        xBeamPosition = atof(root["theBeam"]["xBeamPosition"].asString().c_str());
        xBeamSigma = atof(root["theBeam"]["xBeamSigma"].asString().c_str());
        yBeamPosition = atof(root["theBeam"]["yBeamPosition"].asString().c_str());
        yBeamSigma = atof(root["theBeam"]["yBeamSigma"].asString().c_str());    
        zBeamPosition = atof(root["theBeam"]["zBeamPosition"].asString().c_str());
        xBeamDir = atof(root["theBeam"]["xDir"].asString().c_str()) * CLHEP::degree;
        yBeamDir = atof(root["theBeam"]["yDir"].asString().c_str()) * CLHEP::degree;
        zBeamDir = atof(root["theBeam"]["zDir"].asString().c_str()) * CLHEP::degree;
        p = atof(root["theBeam"]["momentum"].asString().c_str());
        pSigma = atof(root["theBeam"]["momentumSigma"].asString().c_str());
        tBeamSigma = atof(root["theBeam"]["tBeamSigma"].asString().c_str());
        maxOpenAngle = atof(root["theBeam"]["maxOpenAngle"].asString().c_str());
        nParticles = atoi(root["theBeam"]["nParticles"].asString().c_str());
        nStep = atoi(root["theBeam"]["nStep"].asString().c_str());
        if(root["theBeam"]["particleDistribution"].asString().find("Poisson") != -1) {
            particleDistribution = 1;
        } else {
            particleDistribution = 0;
        }
        if(root["theBeam"]["nParticles"].asString().find("Gauss") != -1) {
            momentumDistribution = 2;
        } else {
            momentumDistribution = 0;
        }


        //Definition of the Phantoms ----------------------------------------------
        const Json::Value Phantoms = root["Phantoms"];
        for(G4int iphan = 0; iphan < Phantoms.size(); ++iphan) {
		G4String name = root["Phantoms"][iphan]["name"].asString().c_str();
		G4String material = root["Phantoms"][iphan]["material"].asString().c_str();
		G4double radius = atof(root["Phantoms"][iphan]["radius"].asString().c_str()) * CLHEP::cm;
		G4double zsize = atof(root["Phantoms"][iphan]["zsize"].asString().c_str()) * CLHEP::cm;
		G4double xPos = atof(root["Phantoms"][iphan]["xPos"].asString().c_str()) * CLHEP::cm;
		G4double yPos = atof(root["Phantoms"][iphan]["yPos"].asString().c_str()) * CLHEP::cm;
		G4double zPos = atof(root["Phantoms"][iphan]["zPos"].asString().c_str()) * CLHEP::cm;
		G4double xDir = atof(root["Phantoms"][iphan]["xDir"].asString().c_str()) * CLHEP::degree;
		G4double yDir = atof(root["Phantoms"][iphan]["yDir"].asString().c_str()) * CLHEP::degree;
		G4double zDir = atof(root["Phantoms"][iphan]["zDir"].asString().c_str()) * CLHEP::degree;
                Phantom *phantom = new Phantom(xPos, yPos, zPos, xDir, yDir, zDir, radius, zsize, name, material);
		phantoms.push_back(phantom);
	}


        //Definition of the Detectors ----------------------------------------------
        const Json::Value Detectors = root["Detectors"];

	    for(G4int idet = 0; idet < Detectors.size(); ++idet) {

	    G4double xPos = atof(root["Detectors"][idet]["xPosDetector"].asString().c_str()) * CLHEP::cm;
            G4double yPos = atof(root["Detectors"][idet]["yPosDetector"].asString().c_str()) * CLHEP::cm;
            G4double zPos = atof(root["Detectors"][idet]["zPosDetector"].asString().c_str()) * CLHEP::cm;
            G4double xDir = atof(root["Detectors"][idet]["xDirDetector"].asString().c_str()) * CLHEP::degree;
            G4double yDir = atof(root["Detectors"][idet]["yDirDetector"].asString().c_str()) * CLHEP::degree;
            G4double zDir = atof(root["Detectors"][idet]["zDirDetector"].asString().c_str()) * CLHEP::degree;
            G4double xSize = atof(root["Detectors"][idet]["xSizeDetector"].asString().c_str()) * CLHEP::cm;
            G4double ySize = atof(root["Detectors"][idet]["ySizeDetector"].asString().c_str()) * CLHEP::cm;
            G4double zSize = atof(root["Detectors"][idet]["zSizeDetector"].asString().c_str()) * CLHEP::cm;
            

            if(xPos - xSize/2.0 < - uniSizeX/2.0 || yPos - ySize/2.0 < -uniSizeY/2.0 || zPos - zSize/2.0 < -uniSizeZ/2.0) {
                G4cerr << "\033[1;31m" << "Chamber " << idet << " is not contained in the world" << "\033[0m" << G4endl;
                goodGeometry = false;
                return;
            }
            Detector *detector = new Detector(xPos, yPos, zPos, xDir, yDir, zDir, xSize, ySize, zSize, idet);
            
            //Layers inside a detector ----------------------------------------------
	        const Json::Value jLayer = root["Detectors"][idet]["Layers"];
            
            for(G4int icoll = 0; icoll < jLayer.size(); ++icoll) {
                G4double xPosLayer = atof(root["Detectors"][idet]["Layers"][icoll]["xPosLayer"].asString().c_str()) * CLHEP::cm;
                G4double yPosLayer = atof(root["Detectors"][idet]["Layers"][icoll]["yPosLayer"].asString().c_str()) * CLHEP::cm;
                G4double zPosLayer = atof(root["Detectors"][idet]["Layers"][icoll]["zPosLayer"].asString().c_str()) * CLHEP::cm;
                G4double xDirLayer = atof(root["Detectors"][idet]["Layers"][icoll]["xDirLayer"].asString().c_str()) * CLHEP::degree;
                G4double yDirLayer = atof(root["Detectors"][idet]["Layers"][icoll]["yDirLayer"].asString().c_str()) * CLHEP::degree;
                G4double zDirLayer = atof(root["Detectors"][idet]["Layers"][icoll]["zDirLayer"].asString().c_str()) * CLHEP::degree;
                G4double xSizeLayer_ = atof(root["Detectors"][idet]["Layers"][icoll]["xSizeLayer"].asString().c_str()) * CLHEP::cm;
                G4double ySizeLayer_ = atof(root["Detectors"][idet]["Layers"][icoll]["ySizeLayer"].asString().c_str()) * CLHEP::cm;
                G4double zSizeLayer_ = atof(root["Detectors"][idet]["Layers"][icoll]["zSizeLayer"].asString().c_str()) * CLHEP::cm;
	        G4double xPosPlate = atof(root["Detectors"][idet]["Layers"][icoll]["xPosPlate"].asString().c_str()) * CLHEP::cm;
                G4double yPosPlate = atof(root["Detectors"][idet]["Layers"][icoll]["yPosPlate"].asString().c_str()) * CLHEP::cm;
                G4double zPosPlate = atof(root["Detectors"][idet]["Layers"][icoll]["zPosPlate"].asString().c_str()) * CLHEP::cm;
                G4double xDirPlate = atof(root["Detectors"][idet]["Layers"][icoll]["xDirPlate"].asString().c_str()) * CLHEP::degree;
                G4double yDirPlate = atof(root["Detectors"][idet]["Layers"][icoll]["yDirPlate"].asString().c_str()) * CLHEP::degree;
                G4double zDirPlate = atof(root["Detectors"][idet]["Layers"][icoll]["zDirPlate"].asString().c_str()) * CLHEP::degree;
                G4double xSizePlate_ = atof(root["Detectors"][idet]["Layers"][icoll]["xSizePlate"].asString().c_str()) * CLHEP::cm;
                G4double ySizePlate_ = atof(root["Detectors"][idet]["Layers"][icoll]["ySizePlate"].asString().c_str()) * CLHEP::cm;
                G4double zSizePlate_ = atof(root["Detectors"][idet]["Layers"][icoll]["zSizePlate"].asString().c_str()) * CLHEP::cm;
	        Layer *layer = new Layer(xPosLayer, yPosLayer, zPosLayer, xDirLayer, yDirLayer, zDirLayer, xSizeLayer_, ySizeLayer_, zSizeLayer_, 
				         xPosPlate, yPosPlate, zPosPlate, xDirPlate, yDirPlate, zDirPlate, xSizePlate_, ySizePlate_, zSizePlate_, idet, icoll);
                //Sensors inside a layer ----------------------------------------------
	            const Json::Value Sensors = root["Detectors"][idet]["Layers"][icoll]["Sensors"];
                for(G4int isens = 0; isens < Sensors.size(); ++isens) {
                    G4double xSensPos = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["xPosSensor"].asString().c_str()) * CLHEP::cm;
                    G4double ySensPos = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["yPosSensor"].asString().c_str()) * CLHEP::cm;
                    G4double zSensPos = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["zPosSensor"].asString().c_str()) * CLHEP::cm;
                    G4double xSensDir = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["xDirSensor"].asString().c_str()) * CLHEP::degree;
                    G4double ySensDir = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["yDirSensor"].asString().c_str()) * CLHEP::degree;
                    G4double zSensDir = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["zDirSensor"].asString().c_str()) * CLHEP::degree;
                    G4double xSensSize = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["xSizeSensor"].asString().c_str()) * CLHEP::cm;
                    G4double ySensSize = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["ySizeSensor"].asString().c_str()) * CLHEP::cm;
                    G4double zSensSize = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["zSizeSensor"].asString().c_str()) * CLHEP::cm;
                    G4double xETROCPos = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["xPosETROC"].asString().c_str()) * CLHEP::cm;
                    G4double yETROCPos = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["yPosETROC"].asString().c_str()) * CLHEP::cm;
                    G4double zETROCPos = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["zPosETROC"].asString().c_str()) * CLHEP::cm;
                    G4double xETROCDir = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["xDirETROC"].asString().c_str()) * CLHEP::degree;
                    G4double yETROCDir = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["yDirETROC"].asString().c_str()) * CLHEP::degree;
                    G4double zETROCDir = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["zDirETROC"].asString().c_str()) * CLHEP::degree;
                    G4double xETROCSize = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["xSizeETROC"].asString().c_str()) * CLHEP::cm;
                    G4double yETROCSize = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["ySizeETROC"].asString().c_str()) * CLHEP::cm;
                    G4double zETROCSize = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["zSizeETROC"].asString().c_str()) * CLHEP::cm;
		    G4double interPadx = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["interPadx"].asString().c_str()) * CLHEP::cm;
                    G4double interPady = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["interPady"].asString().c_str()) * CLHEP::cm;
                    G4double xborder = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["xborder"].asString().c_str()) * CLHEP::cm;
                    G4double yborder = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["yborder"].asString().c_str()) * CLHEP::cm;
                    G4int nPadx = atoi(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["nPadx"].asString().c_str());
                    G4int nPady = atoi(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["nPady"].asString().c_str());
                    G4double chargeThreshold = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["chargeThreshold"].asString().c_str());
                    G4double noise = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["noise"].asString().c_str());
                    G4double tdcSigma = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["tdcSigma"].asString().c_str());
                    G4double gain = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["gain"].asString().c_str());
                    LGAD *sensor = new LGAD(xSensPos, ySensPos, zSensPos, 
                                            xSensDir, ySensDir, zSensDir,
                                            xSensSize, ySensSize, zSensSize,
					    xETROCPos, yETROCPos, zETROCPos,
                                            xETROCDir, yETROCDir, zETROCDir,
                                            xETROCSize, yETROCSize, zETROCSize,
                                            nPadx, nPady, interPadx, interPady,
                                            xborder, yborder, chargeThreshold,
                                            noise, tdcSigma, gain, idet, icoll, isens);
                    layer->AddSensor(sensor);
                    G4String label = G4String(std::to_string(idet)) + G4String("_") + 
                                     G4String(std::to_string(icoll)) + G4String("_") + 
                                     G4String(std::to_string(isens)); 
                    G4String Coll = G4String("HitsCollection_") + label;
                    registerCollection(Coll);
		        }   
                detector->AddLayer(layer);
	        }
            detectors.push_back(detector);	    
        }
    }    
    goodGeometry = true;
    Print();
    return;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
bool ConfigurationGeometry::isGood() {
    return goodGeometry;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::getSizeX() {
    return uniSizeX;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::getSizeY() {
    return uniSizeY;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::getSizeZ() {
    return uniSizeZ;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
Phantom * ConfigurationGeometry::getPhantom(G4int a) {
    return phantoms.at(a);
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
Detector * ConfigurationGeometry::getDetector(G4int a) {
    return detectors.at(a);
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetXBeamPosition() {
    return xBeamPosition;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetXBeamSigma() {
    return xBeamSigma;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetYBeamPosition() {
    return yBeamPosition;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetYBeamSigma() {
    return yBeamSigma;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetZBeamPosition() {
    return zBeamPosition;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetXDirBeam() {
    return xBeamDir;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetYDirBeam() {
    return yBeamDir;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetZDirBeam() {
    return zBeamDir;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetMomentum() {
    return p;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetMomentumSigma() {
    return pSigma;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetTBeamSigma() {
    return tBeamSigma;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::GetMaxOpenAngle() {
    return maxOpenAngle;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4int ConfigurationGeometry::GetNParticles() {
    return nParticles;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4int ConfigurationGeometry::GetNStep() {
    return nStep;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4int ConfigurationGeometry::GetMomentumDistribution() {
    return momentumDistribution;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4int ConfigurationGeometry::GetParticleDistribution() {
    return particleDistribution;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4int ConfigurationGeometry::getNPhantoms() {
    return phantoms.size();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4int ConfigurationGeometry::getNDetectors() {
    return detectors.size();
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//

//----------------------------------------------------------------------//
// createG4Objects                                                      //
//----------------------------------------------------------------------//
void ConfigurationGeometry::createG4objects(G4LogicalVolume *mother, 
                                            std::map<G4String, G4Material *> &materials, 
                                            G4SDManager *SDman) {


    G4ThreeVector pos;
    pos.setX(0);
    pos.setY(0);
    pos.setZ(GetZBeamPosition());
    G4RotationMatrix rot;
    rot.rotateY(yBeamDir);
    rot.rotateX(xBeamDir);
    G4ThreeVector newpos = rot * pos;

    G4cout << "Mierda " << newpos << G4endl; 
    coneVolume = new G4Cons("gantry", 0.5*CLHEP::cm, 1.0*CLHEP::cm, 3.0*CLHEP::cm, 3.5*CLHEP::cm, 5.0*CLHEP::cm, 0.0, 2.0*3.14159287);
    conelogicalVolume = new G4LogicalVolume(coneVolume, materials["steel"], "gantrylogical");
    conePhysical = new G4PVPlacement(&rot, newpos, conelogicalVolume, "gantryphysical", mother, false, 0, true);

    G4Colour silicon(238.0/256.0, 162.0/256.0, 11.0/256.0);
    G4VisAttributes *attlog = new G4VisAttributes(silicon);
    conelogicalVolume->SetVisAttributes(attlog);

    for(int i = 0; i < detectors.size(); i++) {
        detectors[i]->createG4Objects(G4String(std::to_string(detectors[i]->detId())),
                                      mother, materials, SDman);
    }


    for(int i = 0; i < phantoms.size(); i++) { 
	phantoms[i]->createG4Objects(mother, materials, SDman);
    }

}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
void ConfigurationGeometry::registerCollection(G4String a) {
    collections.push_back(a);
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Print the class information                                          //
//----------------------------------------------------------------------//
void ConfigurationGeometry::Print() {

    G4cout << "\033[1;34m" << "---------------------------------------Geometry information-----------------------------------" << "\033[0m" << G4endl;
    G4cout << "\033[1;34m" << "The loaded geometry is as follows: " << G4endl;
    G4cout << "\033[1;34m" << "The world is contained in [" << -uniSizeX/2.0/CLHEP::cm << ", " << uniSizeX/2.0/CLHEP::cm << "]x[" << -uniSizeY/2.0/CLHEP::cm << ", " << uniSizeY/2.0/CLHEP::cm << "]x[" << -uniSizeZ/2.0/CLHEP::cm << ", " << uniSizeZ/2.0/CLHEP::cm << "]" << G4endl;
    for(G4int i = 0; i < getNDetectors(); i++) {
        detectors.at(i)->Print();
    }
    G4cout << "\033[0m" << G4endl;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//




