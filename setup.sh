#!/bin/bash

if [ $HOSTNAME == "galois" ]; then
	echo "Setting up environment in Galois"
	export G4INSTALLDIR=/home/pablo/geant4-v11.1.2-install/
	export G4WORKDIR=/home/pablo/Documentos/PROTECTRaul/PROTECT/PROTECTSimulator/
	export JSONCPPDIR=/home/pablo/jsoncpp/
	source $G4INSTALLDIR/bin/geant4.sh
	export PYTHONPATH=$G4WORKDIR/dataAnalysis/
	source /home/pablo/root_v6.28.04-install/bin/thisroot.sh
fi

if [ $HOSTNAME == "deep-gan" ]; then
        echo "Setting up environment in deep gan"
        export G4INSTALLDIR=/home/leire/geant4-v11.1.2-install/
        export G4WORKDIR=/home/leire/PROTECT/PROTECTSimulator/
        export JSONCPPDIR=/home/leire/jsoncpp/
        source $G4INSTALLDIR/bin/geant4.sh
        export PYTHONPATH=$G4WORKDIR/dataAnalysis/
        source /home/leire/root_v6.28.04-install/bin/thisroot.sh
fi

if [ $HOSTNAME == "euler" ]; then
        echo "Setting up environment in euler"
        export G4INSTALLDIR=/home/pablo/geant4-v11.1.2-install/
        export G4WORKDIR=/home/pablo/Documentos/PROTECT/PROTECTSimulator/
        export JSONCPPDIR=/home/pablo/jsoncpp/
        source $G4INSTALLDIR/bin/geant4.sh
        export PYTHONPATH=$G4WORKDIR/dataAnalysis/
        source /home/pablo/root_v6.28.04-install/bin/thisroot.sh
fi

if [ $HOSTNAME == "gauss" ]; then
        echo "Setting up environment in gauss"
        export G4INSTALLDIR=/home/pablo/geant4-v11.1.2-install/
        export G4WORKDIR=/home/pablo/Documentos/PROTECT/PROTECTSimulator/
        export JSONCPPDIR=/home/pablo/jsoncpp/
        source $G4INSTALLDIR/bin/geant4.sh
        export PYTHONPATH=$G4WORKDIR/dataAnalysis/
        source /home/pablo/root_v6.28.04-install/bin/thisroot.sh
fi


