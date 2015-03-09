#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
from OpenGL.GL import *
import os

class MtlParser (dict):
    def __init__(self, filename):
        dict.__init__(self)
        self._filePath = "/".join(filename.split("/")[:-1])
        if len(self._filePath) >0 and self._filePath[-1] != "/":
            self._filePath += "/"
        self._filename = filename.split("/")[-1]
        self._parseMtlFile()
        self._texid = 0


    def _parseMtlFile(self):
        if (os.path.exists(self._filePath + self._filename)):
            for line in open(self._filePath + self._filename, "r"):
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue
                if values[0] == 'newmtl':
                    self[values[1]] = {}
                elif self is {}:
                    raise ValueError, "mtl file doesn't start with newmtl stmt"
                elif values[0] == 'map_Kd':
                    # load the texture referred to by this declaration
                    self[values[0]] = values[1]
                else:
                    self[values[0]] = map(float, values[1:])
        else:
            self['Kd'] = (0.5, 0.5, 0.5)

    # return a 3-tuple containing a basic color for the material
    def getColor(self):
        return self['Kd']

    # return 0 if no image texture else texture id (>0)
    def getTexID(self):
        return self._texid

    def getTexture(self):
        return self._filePath + self['map_Kd']

    def build(self, index):
        # if has a texture and texture exists
        if ('map_Kd' in self) and os.path.exists(self._filePath + self['map_Kd']):
            # glEnable(GL_TEXTURE_2D)
            # generate an image texture
            self._texid = self['texture_Kd'] = glGenTextures(index)
            glBindTexture(GL_TEXTURE_2D, self._texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR)
            # load image
            surf = pygame.image.load(self._filePath + self['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            # apply image as a texture
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,GL_UNSIGNED_BYTE, image)
            # glDisable(GL_TEXTURE_2D)
            