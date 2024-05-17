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
        G4double zOffsetCRY_ = atof(root["theWorld"]["zOffsetCRY"].asString().c_str());
        G4double sizeBoxCRY_ = atof(root["theWorld"]["sizeBoxCRY"].asString().c_str());

        if(xSize <= 0 || ySize <= 0|| zSize <= 0) {
            G4cerr << "\033[1;31m" << "The size of the Universe has been greater than 0" << "\033[0m" << G4endl;
            goodGeometry = false;
            return;
        }

        if(zOffsetCRY_ < 0) {
            G4cerr << "\033[1;31m" << "Cry should be producing muons above the surface" << "\033[0m" << G4endl;
            goodGeometry = false;
            return;
        }

        if(sizeBoxCRY_ <= 0) {
            G4cerr << "\033[1;31m" << "Cry should have a positive size of production" << "\033[0m" << G4endl;
            goodGeometry = false;
            return;
        }

        uniSizeX = xSize * CLHEP::cm;
        uniSizeY = ySize * CLHEP::cm;
        uniSizeZ = zSize * CLHEP::cm;
        zOffsetCRY = zOffsetCRY_ * CLHEP::cm;
        sizeBoxCRY = sizeBoxCRY_ * CLHEP::cm;

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
		        Layer *layer = new Layer(xPosLayer, yPosLayer, zPosLayer, xDirLayer, yDirLayer, zDirLayer, xSizeLayer_, ySizeLayer_, zSizeLayer_, idet, icoll);
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
                    G4double interPadx = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["interPadx"].asString().c_str()) * CLHEP::cm;
                    G4double interPady = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["interPady"].asString().c_str()) * CLHEP::cm;
                    G4double xborder = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["xborder"].asString().c_str()) * CLHEP::cm;
                    G4double yborder = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["yborder"].asString().c_str()) * CLHEP::cm;
                    G4int nPadx = atoi(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["nPadx"].asString().c_str());
                    G4int nPady = atoi(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["nPady"].asString().c_str());
                    G4double chargeThreshold = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["chargeThreshold"].asString().c_str()) * CLHEP::cm;
                    G4double noise = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["noise"].asString().c_str()) * CLHEP::cm;
                    G4double tdcSigma = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["tdcSigma"].asString().c_str()) * CLHEP::cm;
                    G4double gain = atof(root["Detectors"][idet]["Layers"][icoll]["Sensors"][isens]["gain"].asString().c_str()) * CLHEP::cm;
                    LGAD *sensor = new LGAD(xSensPos, ySensPos, zSensPos, 
                                            xSensDir, ySensDir, zSensDir,
                                            xSensSize, ySensSize, zSensSize,
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
G4double ConfigurationGeometry::getZOffsetCRY() {
    return zOffsetCRY;
}
//----------------------------------------------------------------------//
//----------------------------------------------------------------------//


//----------------------------------------------------------------------//
// Accesor to class information                                         //
//----------------------------------------------------------------------//
G4double ConfigurationGeometry::getSizeBoxCRY() {
    return sizeBoxCRY;
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

    for(int i = 0; i < detectors.size(); i++) {
        detectors[i]->createG4Objects(G4String(std::to_string(detectors[i]->detId())),
                                      mother, materials, SDman);
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




