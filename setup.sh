#!/bin/bash

echo "Setting up environment in Galois"
export G4INSTALLDIR=/home/pablo/geant4-v11.1.2-install/
export G4WORKDIR=/home/pablo/Documentos/PROTECT/PROTECTSimulator/
export JSONCPPDIR=/home/pablo/jsoncpp/
source $G4INSTALLDIR/bin/geant4.sh
export PYTHONPATH=$G4WORKDIR/dataAnalysis/


