#!/usr/bin/python2
# -*- coding: utf8 -*-

from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
from vispy.geometry import *
import numpy
from threading import Thread, Lock

from ObjParser import ObjParser
from Camera import Camera
from Light import Light
from Algorithms import *  
from SceneObject import SceneObject

import AutoRotateCamera


class OpenGLWidget(QtOpenGL.QGLWidget):
    """ The main openGL widget """
    def __init__(self, objectNames, algoName, controller,  parent=None):
        """ docstring """
        QtOpenGL.QGLWidget.__init__(self, parent)
        self._controller = controller
        self._algorithms = {
            "Shadow Mapping": ShadowMapAlgorithm(),
            "Shadow Volume" : ShadowVolumeAlgorithm(),
            "Aucune Ombre": NoShadowAlgorithm(),
            "Auto-Ombre": SelfShadowAlgorithm()
        }
        self.setObjects(objectNames)
        self.setAlgo(algoName)
        self._mutex = Lock()

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.timerUpdate)
        fps = 24
        self.timer.start(int(1000/fps))
        self._lightRotation = None
        self._cameraRotation = None
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def timerUpdate(self):
        """ """
        self.updateGL()

    def getObjectNames(self):
        """ Reload openGLWidget """
        return self._objectNames

    def getChosenAlgo(self):
        """ """
        return self._chosenAlgo

    def getChosenAlgoName(self):
        """ """
        return self._chosenAlgoName

    def setObjects(self, objectNames):
        """ docstring """
        self._objectNames = objectNames

    def setAlgo(self, algoName):
        if (algoName in self._algorithms):
            self._chosenAlgo = self._algorithms[algoName]
            self._chosenAlgoName = algoName
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
        smoothFactor = 100
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        dx = int(dx/smoothFactor)
        dy = int(dy/smoothFactor)
        res = False
        if event.buttons() & QtCore.Qt.LeftButton:
            res |= self._camera.setVerticalAngle(self._camera.getVerticalAngle() + 8 * dy)
            res |= self._camera.setHorizontalAngle(self._camera.getHorizontalAngle() + 8 * dx)
        self.lastPos = QtCore.QPoint(event.pos())
        if res:
            self.updateGL()
 
    def wheelEvent(self, event):
        """ docstring """
        if (event.delta() > 0):
            self._camera.forward()
        else:
            self._camera.backward()
        self.updateGL()

    def keyPressEvent(self, event):
        """ """
        if event.key() == QtCore.Qt.Key_Left or event.key() == QtCore.Qt.Key_Q:
            self._camera.left()
        elif event.key() == QtCore.Qt.Key_Right or event.key() == QtCore.Qt.Key_D:
            self._camera.right()
        elif event.key() == QtCore.Qt.Key_Up:
             self._camera.up()
        elif event.key() == QtCore.Qt.Key_Down:
            self._camera.down()
        elif event.key() == QtCore.Qt.Key_Z:
            self._camera.forward()
        elif event.key() == QtCore.Qt.Key_S:
            self._camera.backward()
        elif event.key() == QtCore.Qt.Key_E:
            self._camera.rotateHorizontal(-2.0)
        elif event.key() == QtCore.Qt.Key_A:
            self._camera.rotateHorizontal(2.0)
        elif event.key() == QtCore.Qt.Key_O:
            self._camera.rotateVertical(2.0)
        elif event.key() == QtCore.Qt.Key_L:
            self._camera.rotateVertical(-2.0)
        elif event.key() == QtCore.Qt.Key_Space:
            self._camera.setVerticalAngle(0)
        self.updateGL()


    # ---------- Partie : Opengl ------------
 
    # Called at startup
    def initializeGL(self):
        """ docstring """
        self._mutex.acquire()
        # save mouse cursor position for smooth rotation
        self.lastPos = QtCore.QPoint()

        gloo.set_state(clear_color=(0.2734375, 0.5078125, 0.703125, 1.00), depth_test=True,
                       polygon_offset=(1, 1),
                       blend_func=('src_alpha', 'one_minus_src_alpha'),
                       line_width=0.75)
        # create camera and light
        self._camera = Camera()
        self._lights = self._controller.getLightCollection()

        self._objects = []

        # self._makePlane([0,0,0], 200, 200)
        # examples : should be removed or used for empty scenes
        # self._makeCube((0,1.1,0))
        # self._makeSphere((0,3,0))
        self._loadObjects()

        self._chosenAlgo.init(self._objects, self._camera, self._controller.getLightCollection())
        self._cameraRotation = AutoRotateCamera.AutoRotateCamera(self._camera,1)

        self._mutex.release()

    # Called on each update/frame
    def paintGL(self):
        """ docstring """
        self._mutex.acquire()
        gloo.clear(color=True, depth=True)
        self._chosenAlgo.update()
        self._mutex.release()

    # Called when window is resized
    def resizeGL(self, width, height):
        """ docstring """
        # set openGL in the center of the widget
        self._mutex.acquire()
        GL.glViewport(0, 0, width, height)
        self._mutex.release()

    # Objects construction methods
    def _makePlane(self, position, width, height):
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
        obj = SceneObject(vertices, I, normals, position)
        self._objects.append(obj)
 
    def _makeCube(self, position):
        """ docstring """
        V, F, O = create_cube()
        positions = [x[0] for x in V]
        normals = [x[2] for x in V]
        obj = SceneObject(positions, F, normals, position)
        self._objects.append(obj)

    def _makeSphere(self, position):
        sphere = create_sphere(36,36)
        obj = SceneObject(sphere.vertices(), sphere.faces(), sphere.vertex_normals(), position)
        self._objects.append(obj)

    def _loadObjects(self):
        for obj in self._objectNames:
            parser = ObjParser(obj[0])
            position = obj[1]
            texture = None
            color = None
            if len(obj) == 3:
                if isinstance(obj[2], unicode):
                    texture = obj[2]
                    color = None
                elif isinstance(obj[2], list):
                    texture = None
                    color = obj[2]
            sceneObj = SceneObject(parser.getVertices(), parser.getFaces(), parser.getNormals(), position, color, texture, parser.getTextureCoords())
            self._objects.append(sceneObj)


    def switchCameraAnimation(self):
        """ """
        if self._cameraRotation:
            if self._cameraRotation.getAlive():
                self._cameraRotation.stop()
            else:
                self._cameraRotation.start()

    def killThreads(self):
        """ """
        if self._cameraRotation:
            self._cameraRotation.stop()
