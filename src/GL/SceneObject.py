#!/usr/bin/python2
# -*- coding: utf-8 -*-

from operator import add
from vispy import gloo
from vispy.geometry import *
import numpy

class SceneObject:
    def __init__(self, vertices, indices, normals, position, color=None, texture=None, outline = None, visible = True):
        self._vertices = numpy.array(vertices)
        try:
            self._indices = reduce(add, indices, [])
        except:
            self._indices = indices
        self._indices = numpy.array(self._indices)
        self._normals = numpy.array(normals)
        self._position = position
        self._color = color
        self._texture = texture
        self._outline = outline
        self._visible = visible

    def getVertices(self):
        return self._vertices

    def getVertexBuffer(self):
        return gloo.VertexBuffer(self.getVertices())

    def getIndices(self):
        return self._indices

    def getIndexBuffer(self):
        return gloo.IndexBuffer(self.getIndices())

    def getNormals(self):
        return self._normals

    def getNormalBuffer(self):
        return gloo.VertexBuffer(self.getNormals())

    def getPosition(self):
        return self._position

    def getPositionHomogeneous(self):
        return self._position + [0]

    def getColor(self):
        return self._color

    def getColorAlpha(self):
        return self._color + [1]

    def getTexture(self):
        return self._texture

    def hasOutline(self):
        return self._outline

    def isVisible(self):
        return self._visible

if __name__ == '__main__':
    V, F, O = create_cube()
    vertices = [x[0] for x in V]
    indices = F.tolist()
    normals = [x[2].tolist() for x in V]
    position = [1,1,1]
    color = [0.7,0.7,0.7]
    obj = SceneObject(vertices, indices, normals, position, color)
    print obj.getVertices()
    print obj.getIndices()
    print obj.getNormals()