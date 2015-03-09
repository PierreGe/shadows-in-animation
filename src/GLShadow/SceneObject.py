#!/usr/bin/python2
# -*- coding: utf-8 -*-

from operator import add
from vispy import gloo
from vispy.geometry import *
import numpy

class SceneObject:
    def __init__(self, vertices, indices, normals, position, color=None, texture=None, texcoord = None, outline = None, visible = True):
        self._vertices = numpy.array(vertices).astype(numpy.float32)
        if texcoord != None:
            self._texcoord = [[x[1], x[0]] for x in texcoord]
            self._texcoord = numpy.array(self._texcoord).astype(numpy.float32)
        else:
            self._texcoord = None
        try:
            self._indices = [item for sublist in indices for item in sublist]
        except:
            self._indices = indices
        self._indices = numpy.array(self._indices).astype(numpy.uint16)
        self._normals = numpy.array(normals).astype(numpy.float32)
        self._position = position
        self._color = color
        self._texture = texture
        self._outline = outline
        self._visible = visible
        self._vertexBuffer = None
        self._indexBuffer = None
        self._normalBuffer = None
        self._texcoordBuffer = None

    def getVertices(self):
        return self._vertices

    def getVertexBuffer(self):
        if not self._vertexBuffer:
            self._vertexBuffer = gloo.VertexBuffer(self.getVertices())
        return self._vertexBuffer

    def getIndices(self):
        return self._indices

    def getIndexBuffer(self):
        if not self._indexBuffer:
            self._indexBuffer = gloo.IndexBuffer(self.getIndices())
        return self._indexBuffer

    def getNormals(self):
        return self._normals

    def getNormalBuffer(self):
        if not self._normalBuffer:
            self._normalBuffer = gloo.VertexBuffer(self.getNormals())
        return self._normalBuffer

    def getTexCoords(self):
        return self._texcoord

    def getTexBuffer(self):
        if not self._texcoordBuffer:
            self._texcoordBuffer = gloo.VertexBuffer(self.getTexCoords())
        return self._texcoordBuffer

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