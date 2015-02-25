#!/usr/bin/python2
# -*- coding: utf-8 -*-


class SceneObject:
	def __init__(self, vertices, indices, normals, position, color=None, texture=None, outline = None, visible = True):
        self._vertices = [[vertex[i]+position[i] for i in range(len(vertex))] for vertex in vertices]
		try:
			self._indices = reduce(add, indices, [])
		except:
			self._indices = indices
		self._normals = normals
		self._color = color
		self._texture = texture
		self._outline = outline
		self._visible = visible

	def getVertices(self):
		return self._vertices

	def getIndices(self):
		return self._indices

	def getNormals(self):
		return self._normals

	def getColor(self):
		return self._color

	def getTexture(self):
		return self._texture

	def hasOutline(self):
		return self._outline

	def isVisible(self):
		return self._visible