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

        self.projection = numpy.eye(4, dtype=numpy.float32)
        self.model = numpy.eye(4, dtype=numpy.float32)
        self.view = numpy.eye(4, dtype=numpy.float32)
        self.vertexshader = gloo.VertexShader("shaders/objvertex.shader")
        self.fragmentshader = gloo.FragmentShader("shaders/objfragment.shader")

        gloo.set_state(clear_color=(0.30, 0.30, 0.35, 1.00), depth_test=True,
                       polygon_offset=(1, 1),
                       blend_func=('src_alpha', 'one_minus_src_alpha'),
                       line_width=0.75)
        # create camera and light
        self._camera = Camera()
        self._light = Light()
        # create floor and load .obj objects
        self.makeFloor()
        self.makeCube()
        self.makeSphere()
        self.loadObjects()

    # Objects construction methods
    def makeFloor(self):
        """ docstring """
        self.floor = gloo.Program(
            gloo.VertexShader("shaders/vertex.shader"), 
            gloo.FragmentShader("shaders/fragment.shader"))
        vertices = [[ 10, 0, 10], [10, 0, -10], [-10, 0, -10], [-10,0, 10],
                    [ 10, 0.1, 10], [10, 0.1, -10], [-10, 0.1, -10], [-10, 0.1, 10]]
        self.floor['position'] =  gloo.VertexBuffer(vertices)
        normals = []
        for index in range(len(vertices)):
            prev = vertices[index-1]
            curr = vertices[index]
            next = vertices[(index+1)%len(vertices)]
            diff1 = numpy.subtract(prev, curr)
            diff2 = numpy.subtract(next, curr)
            normals.append(numpy.cross(diff2, diff1))
        self.floor['normal'] = gloo.VertexBuffer(normals)
        I = [0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
             1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5]
        self.floor_indices = gloo.IndexBuffer(I)
        O = [0,1, 1,2, 2,3, 3,0,
             4,7, 7,6, 6,5, 5,4,
             0,5, 1,6, 2,7, 3,4 ]
        self.floor_outline = gloo.IndexBuffer(O)

    def makeCube(self):
        """ docstring """
        V, F, O = create_cube()
        vertices = gloo.VertexBuffer(V)
        self.cube_indices = gloo.IndexBuffer(F)
        self.cube_outline = gloo.IndexBuffer(O)

        self.cube = gloo.Program(
            gloo.VertexShader("shaders/vertex.shader"), 
            gloo.FragmentShader("shaders/fragment.shader"))
        self.cube.bind(vertices)
        self.cube['u_light_position'] = 2, 2, 2
        self.cube['u_light_intensity'] = 1, 1, 1

    def makeSphere(self):
        sphere = create_sphere(36,36)
        V = sphere.vertices()
        N = sphere.vertex_normals()
        F = sphere.faces()
        vertices = gloo.VertexBuffer(V)
        normals = gloo.VertexBuffer(N)
        self.sphere_indices = gloo.IndexBuffer(F)

        self.sphere = gloo.Program(
            gloo.VertexShader("shaders/vertex.shader"),
            gloo.FragmentShader("shaders/fragment.shader"))
        self.sphere['position'] = vertices
        self.sphere['normal'] = normals
        self.sphere['u_light_position'] = 2, 2, 2
        self.sphere['u_light_intensity'] = 1, 1, 1

    def loadObjects(self):
        self.objects = []
        print(self._objectNames)
        for obj in self._objectNames:
            newObj = gloo.Program(self.vertexshader, self.fragmentshader)
            parser = ObjParser(obj[0])
            face = parser.getFaces()
            faceBuff = gloo.IndexBuffer(face.astype(numpy.uint16))
            newObj['a_position'] = gloo.VertexBuffer(parser.getVertices())
            newObj['a_texcoord'] = gloo.VertexBuffer(parser.getTextureCoords())
            #newObj['u_texture'] = gloo.Texture2D(imread(parser.getMtl().getTexture()))
            newObj['color'] = (0.5,0.5,0.8,1)
            self.objects.append((newObj, obj[1], faceBuff))
 
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

        self.paintFloor()
        self.paintCube()
        self.paintSphere()
        self.paintObjects()

    # Paint scene objects methods
    def paintFloor(self):
        """ docstring """
        normal = numpy.array(numpy.matrix(numpy.dot(self.view, self.model)).I.T)
        self.floor["u_normal"] = normal
        self.floor['u_model'] = self.model
        self.floor['u_view'] = self.view
        self.floor['u_projection'] = self.projection
        self.floor['u_color'] = (0.5,0.5,0.5,1)
        self.floor.draw('triangles', self.floor_indices)
        self.floor['u_color'] = (0,0,0,1)
        self.floor.draw('lines', self.floor_outline)

    # Paint scene objects methods
    def paintCube(self):
        """ docstring """
        model = self.model
        translate(model, 0, 1.1, 0)
        normal = numpy.array(numpy.matrix(numpy.dot(self.view, self.model)).I.T)
        self.cube['u_normal'] = normal
        self.cube['u_model'] = self.model
        self.cube['u_view'] = self.view
        self.cube['u_projection'] = self.projection
        self.cube['u_color'] = (1,1,1,1)
        self.cube.draw('triangles', self.cube_indices)
        self.cube['u_color'] = (0,0,0,1)
        self.cube.draw('lines', self.cube_outline)

    def paintSphere(self):
        model = self.model
        translate(model, 0, 2, 0)
        normal = numpy.array(numpy.matrix(numpy.dot(self.view, self.model)).I.T)
        self.sphere['u_normal'] = normal
        self.sphere['u_model'] = self.model
        self.sphere['u_view'] = self.view
        self.sphere['u_projection'] = self.projection
        self.sphere['u_color'] = (1,1,1,1)
        self.sphere.draw('triangles', self.sphere_indices)


    def paintObjects(self):
        for obj in self.objects:
            view = self.view
            translate(view, *obj[1])
            obj[0]['model'] = self.model
            obj[0]['view'] = view
            obj[0]['projection'] = self.projection
            obj[0].draw('triangles',obj[2])

 
    # Called when window is resized
    def resizeGL(self, width, height):
        """ docstring """
        # set openGL in the center of the widget
        GL.glViewport(0, 0, width, height)
        # #from tuto
        #projection = perspective( 45.0, width/float(height), 2.0, 10.0 )
        #program['projection'] = projection
 
 