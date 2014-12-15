from OpenGL.GL import *

class Light(object):
    """docstring for Light"""
    def __init__(self):
        self._xInterval = [-20,20]
        self._yInterval = [4,30]
        self._zInterval = [-20,20]
        xInit = (self._xInterval[1])
        yInit = (self._yInterval[1])
        zInit = (self._zInterval[1])
        self.setPosition([xInit, yInit, zInit])
        self._intensity = [1,1,1]

    def resetLight(self):
        """ """
        self.__init__()

    def getPosition(self):
        return self._position

    def getIntensity(self):
        """ """
        return self._intensity

    def setPosition(self, position):
        "light with a custom position"
        
        self._position = list(position)

    def setIntensity(self, intensity):
        """ """
        self._intensity = intensity


    def setLightsRatio(self,positionPercent):
        "light with a custom position"
        x = self._xInterval[0] + (float(positionPercent[0])/100 * ( abs(self._xInterval[0]) + abs(self._xInterval[1])))
        y = self._yInterval[0] + (float(positionPercent[1])/100 * ( abs(self._yInterval[0]) + abs(self._yInterval[1])))
        z = self._zInterval[0] + (float(positionPercent[2])/100 * ( abs(self._zInterval[0]) + abs(self._zInterval[1])))
        #print("{0}, {1}, {2}".format(x,y,z))
        self.setPosition([x,y,z])
