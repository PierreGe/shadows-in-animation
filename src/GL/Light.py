from OpenGL.GL import *

import math

## ---- ###
LIGHT_POSSIBILITY = ["Point", "Directionnel", "Spot", "Ligne", "Rond"]
LIGHT_WITH_DIRECTION = ["Directionnel","Ligne","Spot"]
COLOR_POSSIBILITY = ["Blanc", "Rouge", "Jaune", "Bleu"]



class Light(object):
    """docstring for Light"""
    
    def __init__(self):
        # interval pour eviter d'envoyer la lampe au perou
        self._xInterval = [-20,20]
        self._yInterval = [2,30]
        self._zInterval = [-20,20]

        xInit = (self._xInterval[1])
        yInit = (self._yInterval[1])
        zInit = (self._zInterval[1])

        self.setPosition([xInit, yInit, zInit])
        self._color = [1,1,1]
        self._type = "Point"

        self._verticalAngle = 45  # 0 vers le bas, 180 vers le plafond
        self._horizontalAngle = 0 # tourne sur lui meme

    def resetLight(self):
        """ """
        self.__init__()

    def getPosition(self):
        return self._position

    def getIntensity(self):
        """ """
        return self._color

    def setPosition(self, position):
        "light with a custom position"
        self._position = list(position)

    def setIntensity(self, intensity):
        """ """
        self._color = intensity

    def getColor(self):
        """ """
        return self._color

    def setColor(self, color):
        """ """
        self._color = color

    def getType(self):
        """ """
        return self._type

    def setVerticalAngle(self,angle):
        """ """
        self._verticalAngle = angle

    def getVerticalAngle(self):
        """ """
        return self._verticalAngle 

    def setHorizontalAngle(self,angle):
        """ """
        self._horizontalAngle = angle

    def getHorizontalAngle(self):
        """ """
        return self._horizontalAngle 

    def getDirectionAsVec3f(self):
        """ """
        return (math.cos(self._horizontalAngle), math.sin(self._verticalAngle ), 1)

    def setLightsRatio(self,positionPercent):
        "light with a custom position"
        x = self._xInterval[0] + (float(positionPercent[0])/100 * ( abs(self._xInterval[0]) + abs(self._xInterval[1])))
        y = self._yInterval[0] + (float(positionPercent[1])/100 * ( abs(self._yInterval[0]) + abs(self._yInterval[1])))
        z = self._zInterval[0] + (float(positionPercent[2])/100 * ( abs(self._zInterval[0]) + abs(self._zInterval[1])))
        #print("{0}, {1}, {2}".format(x,y,z))
        self.setPosition([x,y,z])
