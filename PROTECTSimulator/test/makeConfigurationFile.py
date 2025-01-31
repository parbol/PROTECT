import json, sys, optparse

#######################################################################
# This is a helper class to produce configuration files for the setup #
# Notice that here we are assuming that each detector/layer/sensor is #
# similar. If this is not the case you need to do some manual editing #
#######################################################################

if __name__=='__main__':

    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-n', '--name', action='store', type='string', dest='name', default='', help='Name of output file')
    
    (opts, args) = parser.parse_args()
    if opts.name == '':
        print('Please specify a name for the output configuration file')
        sys.exit()
    
    nPhantoms = 4
    nDetectors = 2
    nLayers = 4
    nSensors = 64
 
    #We take the structure from this basic json file and adapt the dictionary
    with open('../data/confExample.json', 'r') as f:
        data_ = json.load(f)
    
    theWorld = data_['theWorld']
    theBeam = data_['theBeam']
    phantom = data_['Phantoms'][0]
    detector = data_['Detectors'][0]
    layer = detector['Layers'][0]
    sensor = layer['Sensors'][0]

    theWorld["zSizeWorld"] = 250
    
    sensors = []
    for isensor in range(0, nSensors):
        copysens = sensor.copy()
        sensors.append(copysens)
    layer['Sensors'] = sensors

    layers = []
    for ilayer in range(0, nLayers):
        copylayer = layer.copy()
        layers.append(copylayer)
    detector['Layers'] = layers

    detectors = []
    for idetector in range(0, nDetectors):
        copydetector = detector.copy()
        detectors.append(copydetector)

    phantoms = []
    for iphantom in range(0, nPhantoms):
        copyphantom = phantom.copy()
        phantoms.append(copyphantom)

    phantoms[0]['name'] = 'lung'
    phantoms[0]['material'] = 'lung'
    phantoms[0]['xPos'] = 3.0
    phantoms[0]['yPos'] = 3.0
    phantoms[0]['zPos'] = 0.0
    phantoms[0]['radius'] = 2.0
    phantoms[0]['zsize'] = 0.5

    phantoms[1]['name'] = 'brain'
    phantoms[1]['material'] = 'brain'
    phantoms[1]['xPos'] = 3.0
    phantoms[1]['yPos'] = -3.0
    phantoms[1]['zPos'] = 0.0
    phantoms[1]['radius'] = 2.0
    phantoms[1]['zsize'] = 0.5

    phantoms[2]['name'] = 'fat'
    phantoms[2]['material'] = 'fat'
    phantoms[2]['xPos'] = -3.0
    phantoms[2]['yPos'] = 3.0
    phantoms[2]['zPos'] = 0.0
    phantoms[2]['radius'] = 2.0
    phantoms[2]['zsize'] = 0.5

    phantoms[3]['name'] = 'bone'
    phantoms[3]['material'] = 'bone'
    phantoms[3]['xPos'] = -3.0
    phantoms[3]['yPos'] = -3.0
    phantoms[3]['zPos'] = 0.0
    phantoms[3]['radius'] = 2.0
    phantoms[3]['zsize'] = 0.5

    #phantoms = []

    data = {} 
    data['theWorld'] = theWorld
    data['theBeam'] = theBeam
    data['Phantoms'] = phantoms
    data['Detectors'] = detectors

    
    #This must be configured for every setup 
    detectorXPosition = [0, 0]
    detectorYPosition = [0, 0]
    detectorZPosition = [70, -70]
    detectorXSize = [25, 25]
    detectorYSize = [25, 25]
    detectorZSize = [110, 110]
    layerXPosition = [0, 0, 0, 0]
    layerYPosition = [0, 0, 0, 0]
    layerZPosition = [50, 25, -25, -50]
    layerXSize = [24, 24, 24, 24]
    layerYSize = [24, 24, 24, 24]
    layerZSize = [1, 1, 1, 1]
    sensorSize = 2.2
    centralCorridor = 0.2
    interpad = 0.05
    L = (8.0*sensorSize+6.0*centralCorridor)
    posX = -L/2.0 + sensorSize / 2.0
    posY = -L/2.0 + sensorSize / 2.0
    sensorXPosition = []
    sensorYPosition = []
    sensorZPosition = []
    sensorXSize = []
    sensorYSize = []
    sensorZSize = []
    for ix in range(0, 4):
        for iy in range(0, 4):
            Xc = centralCorridor/2.0 + sensorSize/2.0 + ix * (sensorSize + centralCorridor)
            Yc = centralCorridor/2.0 + sensorSize/2.0 + iy * (sensorSize + centralCorridor)
            sensorXPosition.append(Xc)
            sensorYPosition.append(Yc)
            sensorZPosition.append(0)
            sensorXSize.append(sensorSize)
            sensorYSize.append(sensorSize)
            sensorZSize.append(0.05)
            sensorXPosition.append(-Xc)
            sensorYPosition.append(Yc)
            sensorZPosition.append(0)
            sensorXSize.append(sensorSize)
            sensorYSize.append(sensorSize)
            sensorZSize.append(0.05 )
            sensorXPosition.append(Xc)
            sensorYPosition.append(-Yc)
            sensorZPosition.append(0)
            sensorXSize.append(sensorSize)
            sensorYSize.append(sensorSize)
            sensorZSize.append(0.05)
            sensorXPosition.append(-Xc)
            sensorYPosition.append(-Yc)
            sensorZPosition.append(0)
            sensorXSize.append(sensorSize)
            sensorYSize.append(sensorSize)
            sensorZSize.append(0.05)
            print(Xc, Yc)

    for i, det_ in enumerate(data['Detectors']):
        det_['xPosDetector'] = detectorXPosition[i]  
        det_['yPosDetector'] = detectorYPosition[i]        
        det_['zPosDetector'] = detectorZPosition[i]
        det_['xSizeDetector'] = detectorXSize[i]
        det_['ySizeDetector'] = detectorYSize[i]
        det_['zSizeDetector'] = detectorZSize[i]
        for j, layer_ in enumerate(det_['Layers']):
            layer_['xPosLayer'] = layerXPosition[j]
            layer_['yPosLayer'] = layerYPosition[j]
            layer_['zPosLayer'] = layerZPosition[j]
            layer_['xSizeLayer'] = layerXSize[j]
            layer_['ySizeLayer'] = layerYSize[j]
            layer_['zSizeLayer'] = layerZSize[j]
            for k, sensor_ in enumerate(layer_['Sensors']):
                sensor_['xPosSensor'] = sensorXPosition[k]
                sensor_['yPosSensor'] = sensorYPosition[k]
                sensor_['zPosSensor'] = sensorZPosition[k]
                sensor_['xSizeSensor'] = sensorXSize[k]
                sensor_['ySizeSensor'] = sensorYSize[k]
                sensor_['zSizeSensor'] = sensorZSize[k]
                sensor_['interPadx'] = interpad
                sensor_['interPady'] = interpad
                sensor_['gain'] = 10


    # Serializing json
    json_object = json.dumps(data, indent=4)
    # Writing to sample.json
    with open(opts.name, "w") as outfile:
        outfile.write(json_object)


