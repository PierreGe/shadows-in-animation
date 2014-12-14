#!/usr/bin/python2
# -*- coding: utf8 -*-


import math, random
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
from OpenGL.GL import shaders
from ObjParser import ObjParser
from vispy.gloo import *
from vispy.util.transforms import *
from vispy.io import imread
from vispy.geometry import create_cube
import numpy as np

from cgkit.cgtypes import mat4,vec3
from Camera import Camera
from Light import Light       


class OpenGLWidget(QtOpenGL.QGLWidget):
    """ docstring """
    def __init__(self, object_names = [], parent=None):
        """ docstring """
        QtOpenGL.QGLWidget.__init__(self, parent)
        self._objectNames = object_names

    def getObjectNames(self):
        """ Reload openGLWidget """
        return self._objectNames

    def setObjects(self, object_names):
        """ docstring """
        GL.glDeleteLists(1, GL.GL_COMPILE)
        GL.glDeleteTextures(len(self.objects), [i+1 for i in range(len(self.objects))])
        self._objectNames = object_names
        self.loadObjects()

    # ---------- Partie : Qt ------------
 
    def minimumSizeHint(self):
        """ docstring """
        return QtCore.QSize(50, 50)
 
    def sizeHint(self):
        """ docstring """
        return QtCore.QSize(400, 400)
 
    def setXRotation(self, angle):
        """ docstring """
        res = self._camera.setX(angle)
        if res:
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()
 
    def setYRotation(self, angle):
        """ docstring """
        res = self._camera.setY(angle)
        if res:
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()
 
    def setZRotation(self, angle):
        """ docstring """
        res = self._camera.setZ(angle)
        if res:
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()

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
        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self._camera.getX() + 8 * dy)
            self.setYRotation(self._camera.getY() + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self._camera.getX() + 8 * dy)
            self.setZRotation(self._camera.getZ() + 8 * dx)
        self.lastPos = QtCore.QPoint(event.pos())
 
    def wheelEvent(self, event):
        """ docstring """
        # TODO réparer le zoom, utiliser les frustums
        self.zoom += event.delta()/1000.0
        self.updateGL()

    def updateLights(self,position):
        """ """
        self._light.setLightsRatio(position)
        self.updateGL()


    # ---------- Partie : Opengl ------------
 
    # Called at startup
    def initializeGL(self):
        """ docstring """
        self.fbo = 0;
        self.textureBuffer = 0;
        self.renderBuffer = 0
        # initial rotation
        self.zoom = -2

        # save mouse cursor position for smooth rotation
        self.lastPos = QtCore.QPoint()

        # save mouse cursor position for smooth rotation
        self.lastPos = QtCore.QPoint()

        self.projection = np.eye(4, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.view = np.eye(4, dtype=np.float32)
        self.vertexshader = VertexShader("shaders/objvertex.shader")
        self.fragmentshader = FragmentShader("shaders/objfragment.shader")

        set_state(clear_color=(0.30, 0.30, 0.35, 1.00), depth_test=True,
                       polygon_offset=(1, 1),
                       blend_func=('src_alpha', 'one_minus_src_alpha'),
                       line_width=0.75)
        # create camera and light
        self._camera = Camera()
        self._light = Light()
        # create floor and load .obj objects
        # self.makeFloor()
        self.makeCube()

    # Objects construction methods
    def makeFloor(self):
        """ docstring """
        self.floor = Program(
            VertexShader("shaders/vertex.shader"), 
            FragmentShader("shaders/fragment.shader"))
        # self.floor['position'] = [(-1,0,-1), (-1,0,1), (-1,0,1), (1,0,-1)]
        self.floor['position'] =  [[ 10, 0, 10], [-10, 0, 10], [-10, 0.1, 10], [ 10,0.1, 10],
                 [ 10,0.1,-10], [ 10, 0,-10], [-10, 0,-10], [-10,0.1,-10]]
        I = [0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
             1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5]
        self.floor_indices = IndexBuffer(I)
        O = [0,1, 1,2, 2,3, 3,0,
             4,7, 7,6, 6,5, 5,4,
             0,5, 1,6, 2,7, 3,4 ]
        self.floor_outline = IndexBuffer(O)

    def makeCube(self):
        """ docstring """
        V, F, O = create_cube()
        vertices = VertexBuffer(V)
        self.cube_indices = IndexBuffer(F)
        self.cube_outline = IndexBuffer(O)

        self.cube = Program(
            VertexShader("shaders/vertex.shader"), 
            FragmentShader("shaders/fragment.shader"))
        self.cube.bind(vertices)
        self.cube['u_light_position'] = 2, 2, 2
        self.cube['u_light_intensity'] = 1, 1, 1

    def loadObjects(self):
        """ docstring """
        self.objects = []
        for obj in self._objectNames:
            newObj = Program(self.vertexshader, self.fragmentshader)
            parser = ObjParser(obj[0])
            newObj['position'] = parser.getVertices()
            newObj['texcoord'] = parser.getTextureCoords()
            newObj['u_texture'] = Texture2D(imread(parser.getMtl().getTexture()))
            self.objects.append((newObj, obj[1], IndexBuffer(parser.getIndices())))
 
    # Called on each update/frame
    def paintGL(self):
        """ docstring """
        clear(color=True, depth=True)
        # paint objects
        # self._light.renderLight()

        # set frustum
        self.view = np.eye(4, dtype=np.float32)
        translate(self.view, 0, -1, self.zoom)
        self.projection = ortho(1*self.zoom, -1*self.zoom, 1*self.zoom, -1*self.zoom, 1, 100)

        # apply rotation
        self.model = np.eye(4, dtype=np.float32)
        rotate(self.model, self._camera.getX(), 1, 0, 0)
        rotate(self.model, self._camera.getY(), 0, 1, 0)
        rotate(self.model, self._camera.getZ(), 0, 0, 1)

        # self.paintFloor()
        self.paintCube()

    # Paint scene objects methods
    def paintFloor(self):
        """ docstring """
        normal = np.array(np.matrix(np.dot(self.view, self.model)).I.T)
        self.floor["u_light_position"] = 2, 2, 2
        self.floor["u_light_intensity"] = 1, 1, 1
        self.floor["u_normal"] = normal
        self.floor['u_model'] = self.model
        self.floor['u_view'] = self.view
        self.floor['u_projection'] = self.projection
        self.floor['u_color'] = (0.5,0.5,0.5,1)
        self.floor.draw(gl.GL_TRIANGLE_STRIP, self.floor_indices)
        self.floor['u_color'] = (0,0,0,1)
        self.floor.draw(gl.GL_LINES, self.floor_outline)

    # Paint scene objects methods
    def paintCube(self):
        """ docstring """
        normal = np.array(np.matrix(np.dot(self.view, self.model)).I.T)
        self.cube['u_normal'] = normal
        self.cube['u_model'] = self.model
        self.cube['u_view'] = self.view
        self.cube['u_projection'] = self.projection
        # set_state(blend=False, depth_test=True, polygon_offset_fill=True)
        self.cube['u_color'] = (1,1,1,1)
        self.cube.draw(gl.GL_TRIANGLE_STRIP, self.cube_indices)
        # set_state(polygon_offset_fill=False, blend=True, depth_mask=False)
        self.cube['u_color'] = (0,0,0,1)
        self.cube.draw(gl.GL_LINES, self.cube_outline)

    def paintObjects(self):
        """ docstring """
        for obj in self.objects:
            view = self.view
            translate(view, *obj[1])
            obj[0]['model'] = self.model
            obj[0]['view'] = view
            obj[0]['projection'] = self.projection
            obj[0].draw(GL.GL_TRIANGLE_STRIP)

 
    # Called when window is resized
    def resizeGL(self, width, height):
        """ docstring """
        # set openGL in the center of the widget
        GL.glViewport(0, 0, width, height)
        # #from tuto
        #projection = perspective( 45.0, width/float(height), 2.0, 10.0 )
        #program['projection'] = projection
 
 