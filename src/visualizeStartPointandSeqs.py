from splitData import *
from matplotlib import * 

try:
    type(startPoints)
except BaseException:
    print("startPoints is not defined")
    startPoints = GetAllSeqStartPoints()
    normalizedSeqs = GetAllNormalizedSeqs()
    unNormalizedSeqs = GetAllUnnormalizedSeqs()
else:
    print("startPoints is already defined")

from pylab import *

name = ['accelerometerX','accelerometerY','accelerometerZ','gyroscopeX',
'gyroscopeY','gyroscopeZ']
label = 4
start = 20
end = 25

for sensor in name:
    figure()
    plot(normalizedSeqs[label][sensor].
        loc[startPoints[label][start]-100:startPoints[label][end]+100],'b-')
    
    X = startPoints[label][start:end+1]
    print(X)
    Y = [0] * len(X)
    scatter(X,Y,marker = '^',color = 'r')
    show()
