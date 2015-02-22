#!/usr/bin/python2
# -*- coding: utf-8 -*-

import Light

class LightCollection(list):
    """docstring for LightCollection"""
    def __init__(self, *args):
        list.__init__(self, *args)
        self.append(Light.Light())

    def addLight(self, light):
        """ """
        self.append(light)
        print(self)
    
    def getLightList(self):
        """ """
        return self

    def deleteLight(self, lightIndex):
        """ """
        del self[lightIndex]