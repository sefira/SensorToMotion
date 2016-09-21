import pandas as pd

sensor_name = ['accelerometerX','accelerometerY','accelerometerZ','gyroscopeX',
'gyroscopeY','gyroscopeZ']

def ReadData(filename):
    sensorData = pd.read_csv(filename)
    
    normalizedSensorData = sensorData.copy()
    normalizedSensorData.drop('deviceID',axis=1, inplace=True)
    sensorData.drop('deviceID',axis=1, inplace=True)
    
    #normalize the accelerometer and gyroscope data
    from sklearn import preprocessing
    normalizedSensorData = pd.DataFrame(preprocessing.scale(normalizedSensorData),
                                        normalizedSensorData.index,normalizedSensorData.columns)
#    normalizedSensorData = normalizedSensorData - normalizedSensorData.mean()
#    normalizedSensorData = normalizedSensorData / normalizedSensorData.std()
#    normalizedSensorData = normalizedSensorData / 2048
    
    return (sensorData, normalizedSensorData)
