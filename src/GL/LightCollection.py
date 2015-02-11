

import Light

class LightCollection(object):
    """docstring for LightCollection"""
    def __init__(self):
        self.lightList = []
        self.lightList.append(Light.Light())

    def addLight(self, light):
        """ """
        self.lightList.append(light)
        print(self.lightList)
    
    def getLightList(self):
        """ """
        return self.lightList

    def deleteLight(self, light):
        """ """
        self.lightList.remove(light)

    def  __getitem__(self,index):
        """ """
        return self.lightList[index]

    def __len__(self):
        """ """
        return len(self.lightList)