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
import AutoRotateLight
import AutoRotateCamera


class OpenGLWidget(QtOpenGL.QGLWidget):
    """ The main openGL widget """
    def __init__(self, objectNames, algoName, controller,  parent=None):
        """ docstring """
        QtOpenGL.QGLWidget.__init__(self, parent)
        self._controller = controller
        self._algorithms = {
            "Shadow Mapping": ShadowMapAlgorithm(),
            "Aucune Ombre": NoShadowAlgorithm(),
<<<<<<< HEAD
            "Auto-Ombre": SelfShadowAlgorithm()
=======
            "Ray Tracing": RayTracingAlgorithm()
>>>>>>> 11a20619119bcf110ecebf33c30b1fab00e5e834
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

    def keyPressEvent(self, e):
        """ """
        print("Key pressed")
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


    # ---------- Partie : Opengl ------------
 
    # Called at startup
    def initializeGL(self):
        """ docstring """
        print "GLSL Version : " + GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
        self._mutex.acquire()
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

        self._makePlane((0,0,0), 20, 20)
        # examples : should be removed or used for empty scenes
        # self._makeCube((0,1.1,0))
        # self._makeSphere((0,3,0))
        self._loadObjects()

        self._chosenAlgo.init(self.positions, self.indices, self.normals, self._camera, self._light)
        self._lightRotation = AutoRotateLight.AutoRotateLight(self._light,1)
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

        self._addPositions(vertices, position)
        self._addIndices(I)
        self.normals.extend(normals)
# 
    def _makeCube(self, position):
        """ docstring """
        V, F, O = create_cube()
        positions = [x[0] for x in V]
        normals = [x[2] for x in V]
        self._addPositions(positions, position)
        self._addIndices(F.tolist())
        self.normals.extend(normals)

    def _makeSphere(self, position):
        sphere = create_sphere(36,36)
        self._addPositions(sphere.vertices().tolist(), position)
        self._addIndices(sphere.faces().tolist())
        self.normals.extend(sphere.vertex_normals().tolist())

    def _loadObjects(self):
        for obj in self._objectNames:
            parser = ObjParser(obj[0])
            #program['u_texture'] = gloo.Texture2D(imread(parser.getMtl().getTexture()))
            self._addPositions(parser.getVertices().tolist(), obj[1])
            self._addIndices(parser.getFaces().astype(numpy.uint16).tolist())
            self.normals.extend(parser.getNormals().astype(numpy.float32).tolist())

    def _addPositions(self, vertices, position):
        self.positions.extend([[vertex[i]+position[i] for i in range(3)] for vertex in vertices])

    # add index so mesh reference only their vertices
    def _addIndices(self, indices):
        if (len(self.indices) > 0):
            max_index = max(self.indices)+1
        else:
            max_index = 0
        try:
            self.indices.extend([item+max_index for sublist in indices for item in sublist])
        except:
            self.indices.extend([item+max_index for item in indices])

    def switchLightAnimation(self):
        """ """
        if self._lightRotation:
            if self._lightRotation.getAlive():
                self._lightRotation.stop()
            else:
                self._lightRotation.start()

    def switchCameraAnimation(self):
        """ """
        if self._cameraRotation:
            if self._cameraRotation.getAlive():
                self._cameraRotation.stop()
            else:
                self._cameraRotation.start()

    def killThreads(self):
        """ """
        if self._lightRotation:
            self._lightRotation.stop()
        if self._cameraRotation:
            self._cameraRotation.stop()


