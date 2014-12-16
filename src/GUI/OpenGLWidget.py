#!/usr/bin/python2
# -*- coding: utf8 -*-

from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
import vispy.gloo as gloo
from vispy.util.transforms import *
from vispy.geometry import *
import numpy

from ObjParser import ObjParser
from Camera import Camera
from Light import Light   
from SceneObject import SceneObject 
from Utils import * 
from Algorithms import *  


class OpenGLWidget(QtOpenGL.QGLWidget):
    """ docstring """
    def __init__(self, objectNames, algo, controller,  parent=None):
        """ docstring """
        QtOpenGL.QGLWidget.__init__(self, parent)
        self._controller = controller
        self._algorithms = {
            "Shadow Mapping": ShadowMapAlgorithm(),
            "Aucune Ombre": NoShadowAlgorithm()
        }
        self.setObjects(objectNames)
        self.setAlgo(algo)

    def getObjectNames(self):
        """ Reload openGLWidget """
        return self._objectNames

    def getChosenAlgo(self):
        """ """
        return self._chosenAlgo

    def setObjects(self, objectNames):
        """ docstring """
        self._objectNames = objectNames

    def setAlgo(self, algo):
        if (algo in self._algorithms):
            self._chosenAlgo = self._algorithms[algo]
        else:
            QtGui.QMessageBox.warning(self, "Erreur", "Cet algo n'existe pas pour cette scene")
            self._controller.showHelp()
            raise ValueError("Misconfoguration of scene")
    # ---------- Partie : Qt ------------
 
    def minimumSizeHint(self):
        """ docstring """
        return QtCore.QSize(50, 50)
 
    def sizeHint(self):
        """ docstring """
        return QtCore.QSize(400, 400)

        # Events
    def mousePressEvent(self, event):
        """ This method is called when there is a click """
        self.lastPos = QtCore.QPoint(event.pos())
 
    def mouseMoveEvent(self, event):
        """ This method is called when there is a mouse (drag) event"""
        smoothFactor = 10
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        dx = int(dx/smoothFactor)
        dy = int(dy/smoothFactor)
        res = False
        if event.buttons() & QtCore.Qt.LeftButton:
            res |= self._camera.setX(self._camera.getX() + 8 * dy)
            res |= self._camera.setY(self._camera.getY() + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            res |= self._camera.setX(self._camera.getX() + 8 * dy)
            res |= self._camera.setZ(self._camera.getZ() + 8 * dx)
        self.lastPos = QtCore.QPoint(event.pos())
        if res:
            self.updateGL()
 
    def wheelEvent(self, event):
        """ docstring """
        if (event.delta() > 0):
            self._camera.zoomIn()
        else:
            self._camera.zoomOut()
        self.updateGL()

    def updateLights(self,position):
        """ """
        self._light.setLightsRatio(position)
        self.updateGL()


    # ---------- Partie : Opengl ------------
 
    # Called at startup
    def initializeGL(self):
        """ docstring """
        # save mouse cursor position for smooth rotation
        self.lastPos = QtCore.QPoint()

        gloo.set_state(clear_color=(0.30, 0.30, 0.35, 1.00), depth_test=True,
                       polygon_offset=(1, 1),
                       blend_func=('src_alpha', 'one_minus_src_alpha'),
                       line_width=0.75)
        # create camera and light
        self._camera = Camera()
        self._light = Light()

        self.positions = []
        self.indices = []
        self.normals = []

        self.makeFloor()
        # examples : should be removed or used for empty scenes
        # self.makeCube((0,1.1,0),(0,1,0,1))
        # self.makeSphere((0,3,0),(1,1,1,1))
        self.loadObjects()

        self._chosenAlgo.init(self.positions, self.indices, self.normals, self._camera, self._light)

    # Objects construction methods
    def makeFloor(self):
        """ docstring """
        vertices = [[ 10, 0, 10], [10, 0, -10], [-10, 0, -10], [-10,0, 10],
                    [ 10, -0.1, 10], [10, -0.1, -10], [-10, -0.1, -10], [-10, -0.1, 10]]
        normals = []
        for index in range(len(vertices)):
            prev = vertices[index-1]
            curr = vertices[index]
            next = vertices[(index+1)%len(vertices)]
            diff1 = numpy.subtract(prev, curr)
            diff2 = numpy.subtract(next, curr)
            normals.append(numpy.cross(diff2, diff1))
        I = [0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
             1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5]
        # O = [0,1, 1,2, 2,3, 3,0,
        #      4,7, 7,6, 6,5, 5,4,
        #      0,5, 1,6, 2,7, 3,4 ]

        self.positions.extend(vertices)
        self.indices.extend(I)
        self.normals.extend(normals)
# 
    def makeCube(self, position, color):
        """ docstring """
        V, F, O = create_cube()
        vertices = gloo.VertexBuffer(V)
        indices = gloo.IndexBuffer(F)
        outlines = gloo.IndexBuffer(O)

        program = gloo.Program(self.vertexshader, self.fragmentshader)
        program.bind(vertices)
        self.objects.append(SceneObject(program,
                                        position,
                                        color,
                                        indices,
                                        outlines))

    def makeSphere(self, position, color):
        sphere = create_sphere(36,36)
        V = sphere.vertices()
        N = sphere.vertex_normals()
        F = sphere.faces()
        vertices = gloo.VertexBuffer(V)
        normals = gloo.VertexBuffer(N)
        indices = gloo.IndexBuffer(F)

        program = gloo.Program(self.vertexshader, self.fragmentshader)
        program['position'] = vertices
        program['normal'] = normals
        self.objects.append(SceneObject(program,
                                        position,
                                        color,
                                        indices))

    def loadObjects(self):
        for obj in self._objectNames:
            parser = ObjParser(obj[0])
            position = obj[1]
            #program['u_texture'] = gloo.Texture2D(imread(parser.getMtl().getTexture()))
            self.positions.extend(parser.getVertices().tolist())
            # should add maximum of previous list to item
            max_index = max(self.indices)+1
            self.indices.extend([item+max_index for sublist in parser.getFaces().astype(numpy.uint16).tolist() for item in sublist])
            self.normals.extend(parser.getNormals().astype(numpy.float32).tolist())

    # Called on each update/frame
    def paintGL(self):
        """ docstring """
        gloo.clear(color=True, depth=True)
        self._chosenAlgo.update()

    # Called when window is resized
    def resizeGL(self, width, height):
        """ docstring """
        # set openGL in the center of the widget
        GL.glViewport(0, 0, width, height)
 
 