#!/usr/bin/python2
# -*- coding: utf8 -*-


import math, random
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
from OpenGL.GL import shaders
from ObjParser import ObjParser
import vispy.gloo as gloo
from vispy.util.transforms import *
from vispy.io import imread
from vispy.geometry import *
import numpy

from cgkit.cgtypes import mat4,vec3
from Camera import Camera
from Light import Light   
from SceneObject import SceneObject    


class OpenGLWidget(QtOpenGL.QGLWidget):
    """ docstring """
    def __init__(self, object_names = [], parent=None):
        """ docstring """
        QtOpenGL.QGLWidget.__init__(self, parent)
        self._objectNames = object_names[0]

    def getObjectNames(self):
        """ Reload openGLWidget """
        return self._objectNames

    def setObjects(self, object_names):
        """ docstring """
        GL.glDeleteLists(1, GL.GL_COMPILE)
        GL.glDeleteTextures(len(self.objects), [i+1 for i in range(len(self.objects))])
        self._objectNames = object_names[0]
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

        self.vertexshader = gloo.VertexShader("shaders/vertex.shader")
        self.fragmentshader = gloo.FragmentShader("shaders/fragment.shader")

        gloo.set_state(clear_color=(0.30, 0.30, 0.35, 1.00), depth_test=True,
                       polygon_offset=(1, 1),
                       blend_func=('src_alpha', 'one_minus_src_alpha'),
                       line_width=0.75)
        # create camera and light
        self._camera = Camera()
        self._light = Light()
        # create floor and load .obj objects

        self.objects = []

        self.makeFloor()
        self.makeCube((0,1.1,0),(1,1,1,1))
        self.makeSphere((0,3,0),(1,1,1,1))
        self.loadObjects()

    # Objects construction methods
    def makeFloor(self):
        """ docstring """
        program = gloo.Program(self.vertexshader, self.fragmentshader)
        vertices = [[ 10, 0, 10], [10, 0, -10], [-10, 0, -10], [-10,0, 10],
                    [ 10, -0.1, 10], [10, -0.1, -10], [-10, -0.1, -10], [-10, -0.1, 10]]
        program['position'] =  gloo.VertexBuffer(vertices)
        normals = []
        for index in range(len(vertices)):
            prev = vertices[index-1]
            curr = vertices[index]
            next = vertices[(index+1)%len(vertices)]
            diff1 = numpy.subtract(prev, curr)
            diff2 = numpy.subtract(next, curr)
            normals.append(numpy.cross(diff2, diff1))
        program['normal'] = gloo.VertexBuffer(normals)
        I = [0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
             1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5]
        indices = gloo.IndexBuffer(I)
        O = [0,1, 1,2, 2,3, 3,0,
             4,7, 7,6, 6,5, 5,4,
             0,5, 1,6, 2,7, 3,4 ]
        outlines = gloo.IndexBuffer(O)
        program['u_light_position'] = 2, 2, 2
        program['u_light_intensity'] = 1, 1, 1
        self.objects.append(SceneObject(program, 
                                        (0,0,0),
                                        (0.5,0.5,0.5,1),
                                        indices,
                                        outlines))

    def makeCube(self, position, color):
        """ docstring """
        V, F, O = create_cube()
        vertices = gloo.VertexBuffer(V)
        indices = gloo.IndexBuffer(F)
        outlines = gloo.IndexBuffer(O)

        program = gloo.Program(self.vertexshader, self.fragmentshader)
        program.bind(vertices)
        program['u_light_position'] = 2, 2, 2
        program['u_light_intensity'] = 1, 1, 1
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
        program['u_light_position'] = 2, 2, 2
        program['u_light_intensity'] = 1, 1, 1
        self.objects.append(SceneObject(program,
                                        position,
                                        color,
                                        indices))

    def loadObjects(self):
        for obj in self._objectNames:
            parser = ObjParser(obj[0])
            position = obj[1]
            color = (0.5,0.5,0.8,1)
            face = parser.getFaces()
            indices = gloo.IndexBuffer(face.astype(numpy.uint16))
            program = gloo.Program(self.vertexshader, self.fragmentshader)
            program['position'] = gloo.VertexBuffer(parser.getVertices())
            # should use a VertexBuffer but it says datatype float64 is not ok
            program['normal'] = parser.getNormals()
            program['u_light_position'] = 2, 2, 2
            program['u_light_intensity'] = 1, 1, 1
            #program['u_texture'] = gloo.Texture2D(imread(parser.getMtl().getTexture()))
            self.objects.append(SceneObject(program,
                                            position,
                                            color,
                                            indices))
 
    # Called on each update/frame
    def paintGL(self):
        """ docstring """
        gloo.clear(color=True, depth=True)
        # paint objects
        # self._light.renderLight()

        # set frustum
        self.view = numpy.eye(4, dtype=numpy.float32)
        translate(self.view, 0, -1, self.zoom)
        self.projection = perspective(60, 4.0/3.0, 0.1, 100)

        # apply rotation
        self.model = numpy.eye(4, dtype=numpy.float32)
        rotate(self.model, self._camera.getX(), 1, 0, 0)
        rotate(self.model, self._camera.getY(), 0, 1, 0)
        rotate(self.model, self._camera.getZ(), 0, 0, 1)

        self.paintObjects()

    def paintObjects(self):
        normal = numpy.array(numpy.matrix(numpy.dot(self.view, self.model)).I.T)
        for obj in self.objects:
            model = self.model.copy()
            translate(model, *obj.position)
            obj.program['u_normal'] = normal
            obj.program['u_model'] = model
            obj.program['u_view'] = self.view
            obj.program['u_projection'] = self.projection
            if (obj.visible):
                obj.program['u_color'] = obj.color
                if (obj.indices):
                    obj.program.draw('triangles', obj.indices)
                else:
                    obj.program.draw('triangles')
                if (obj.outline):
                    obj.program['u_color'] = (0,0,0,1)
                    obj.program.draw('lines', obj.outline)

 
    # Called when window is resized
    def resizeGL(self, width, height):
        """ docstring """
        # set openGL in the center of the widget
        GL.glViewport(0, 0, width, height)
        # #from tuto
        #projection = perspective( 45.0, width/float(height), 2.0, 10.0 )
        #program['projection'] = projection
 
 