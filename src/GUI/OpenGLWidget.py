#!/usr/bin/python2
# -*- coding: utf8 -*-

from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
from vispy.geometry import *
import numpy

from ObjParser import ObjParser
from Camera import Camera
from Light import Light
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

        self.makePlane((0,0,0), 20, 20)
        # examples : should be removed or used for empty scenes
        # self.makeCube((0,1.1,0))
        # self.makeSphere((0,3,0))
        self.loadObjects()

        self._chosenAlgo.init(self.positions, self.indices, self.normals, self._camera, self._light)

    # Objects construction methods
    def makePlane(self, position, width, height):
        """ docstring """
        vertices = [[ (width/2), 0, (height/2)], [(width/2), 0, -(height/2)], [-(width/2), 0, -(height/2)], [-(width/2),0, (height/2)],
                    [ (width/2), -0.1, (height/2)], [(width/2), -0.1, -(height/2)], [-(width/2), -0.1, -(height/2)], [-(width/2), -0.1, (height/2)]]
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

        self.addPositions(vertices, position)
        self.addIndices(I)
        self.normals.extend(normals)
# 
    def makeCube(self, position):
        """ docstring """
        V, F, O = create_cube()
        positions = [x[0] for x in V]
        normals = [x[2] for x in V]
        self.addPositions(positions, position)
        self.addIndices(F.tolist())
        self.normals.extend(normals)

    def makeSphere(self, position):
        sphere = create_sphere(36,36)
        self.addPositions(sphere.vertices().tolist(), position)
        self.addIndices(sphere.faces().tolist())
        self.normals.extend(sphere.vertex_normals().tolist())

    def loadObjects(self):
        for obj in self._objectNames:
            parser = ObjParser(obj[0])
            #program['u_texture'] = gloo.Texture2D(imread(parser.getMtl().getTexture()))
            self.addPositions(parser.getVertices().tolist(), obj[1])
            self.addIndices(parser.getFaces().astype(numpy.uint16).tolist())
            self.normals.extend(parser.getNormals().astype(numpy.float32).tolist())

    def addPositions(self, vertices, position):
        self.positions.extend([[vertex[i]+position[i] for i in range(3)] for vertex in vertices])

    # add index so mesh reference only their vertices
    def addIndices(self, indices):
        if (len(self.indices) > 0):
            max_index = max(self.indices)+1
        else:
            max_index = 0
        try:
            self.indices.extend([item+max_index for sublist in indices for item in sublist])
        except:
            self.indices.extend([item+max_index for item in indices])

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
 
 