class Camera(object):
    """docstring for Camera"""
    def __init__(self):
        """ Constructeur de la classe Camera"""
        self._x = 20
        self._xInterval = [20,60]
        self._y = 352
        self._z = 6

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getZ(self):
        return self._z

    def setX(self,x):
        """ """
        x = self.normalizeAngle(x)
        if x < self._xInterval[0]:
            x = self._xInterval[0]
        elif x > self._xInterval[1]:
            x = self._xInterval[1]
        if x != self._x:
            self._x = x
            return True
        return False

    def setY(self,y):
        """ """
        y = self.normalizeAngle(y)
        if y != self._y:
            self._y = y
            return True
        return False

    def setZ(self,z):
        """ """
        z = self.normalizeAngle(z)
        if z != self._z:
            self._z = z
            return True
        return False

    def normalizeAngle(self, angle):
        """ Keep angle between 0 and 360"""
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle