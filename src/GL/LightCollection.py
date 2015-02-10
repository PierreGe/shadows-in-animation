

class LightCollection(object):
    """docstring for LightCollection"""
    def __init__(self):
        self.lightList = []

    def addLight(self, light):
        """ """
        self.lightList.append(light)
    
    def getLightList(self):
        """ """
        return self.lightList