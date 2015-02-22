#!/usr/bin/python2
# -*- coding: utf-8 -*-


class SceneObject:
	def __init__(self, program, position, color, indices=None, outline = None, visible = True):
		self.program = program
		self.position = position
		self.color = color
		self.indices = indices
		self.outline = outline
		self.visible = visible