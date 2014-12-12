import pygame
from OpenGL.GL import *

class MtlParser (dict):
    def __init__(self, filename):
        dict.__init__(self)
        self._filePath = "/".join(filename.split("/")[:-1])
        if len(self._filePath) >0 and self._filePath[-1] != "/":
            self._filePath += "/"
        self._filename = filename.split("/")[-1]
        self._parseMtlFile()
        self.texid = 0


    def _parseMtlFile(self):
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

    def getColor(self):
        return self['Kd']

    def build(self, index):
        surf = pygame.image.load(self._filePath + self['map_Kd'])
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size
        self.texid = self['texture_Kd'] = glGenTextures(index)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,GL_UNSIGNED_BYTE, image)
        glDisable(GL_TEXTURE_2D)
            