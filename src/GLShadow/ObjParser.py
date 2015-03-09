#!/usr/bin/python2
# -*- coding: utf-8 -*-


import os

from vispy.io import imread, read_mesh, load_data_file

 
class ObjParser:
    def __init__(self, filename):
        """Loads a Wavefront OBJ file. """

        self._filePath = "/".join(filename.split("/")[:-1])
        filename = filename.split("/")[-1]
        if len(self._filePath) >0 and self._filePath[-1] != "/":
            self._filePath += "/"
        self._cachePath = self._filePath.replace("assets/", "cache/", 1)

        self._vertices = []
        self._normals = []
        self._textureCoords = []
        self._faces = []
        self._mtl = None
        try:
            if os.path.isfile(self._filePath + filename):
                self._parseObjFile(filename)
            else:
                raise IOError("File does not exist")
        except Exception, e:
            print("[ERROR] Unable to load object")
            raise

    def getVertices(self):
        return self._vertices

    def getNormals(self):
        return self._normals

    def getTextureCoords(self):
        return self._textureCoords

    def getFaces(self):
        return self._faces

    def getMtl(self):
        return self._mtl

    def _parseObjFile(self, filename):
        """ """
        self._vertices, self._faces, self._normals, self._textureCoords = read_mesh(self._filePath + filename)
        


