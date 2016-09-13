import pandas as pd

sensor_name = ['accelerometerX','accelerometerY','accelerometerZ','gyroscopeX',
'gyroscopeY','gyroscopeZ']

def ReadData(filename):
    sensorData = pd.read_csv(filename)
    sizeofData = sensorData.shape
    
    normalizedSensorData = sensorData.copy()
    normalizedSensorData.drop('deviceID',axis=1, inplace=True)
    sensorData.drop('deviceID',axis=1, inplace=True)
    mean = range(sizeofData[1])
    std = range(sizeofData[1])
    
    #normalize the accelerometer and gyroscope data, except the last deviceID
    for i in range(sizeofData[1] - 1):
        mean[i] = sensorData.ix[:,i].mean()
        std[i] = sensorData.ix[:,i].std()
        normalizedSensorData.ix[:,i] -= mean[i]
        normalizedSensorData.ix[:,i] /= std[i]
    
    return (sensorData, normalizedSensorData)
