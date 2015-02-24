#!/usr/bin/python2
# -*- coding: utf-8 -*-

from OpenGL import GL, GLU
from vispy import gloo
from vispy.util.transforms import *
import numpy

from Camera import Camera
from Light import Light
from Utils import *


DEFAULT_COLOR = (0.7, 0.7, 0.7, 1)

def createViewMatrix(camera):
    view = numpy.eye(4, dtype=numpy.float32)
    translate(view, -camera.getX(), -camera.getY(), -camera.getZ())
    rotate(view, -camera.getDirectionX(), 1, 0, 0)
    rotate(view, -camera.getDirectionY(), 0, 1, 0)
    return view

class ShadowMapAlgorithm:
    FRAGMENT_SHADER_FILENAME = "shaders/shadowmapalgo.fragmentshader"
    VERTEX_SHADER_FILENAME = "shaders/shadowmapalgo.vertexshader"
    def __init__(self):
        # assign members that never change
        self._shadowProgram = gloo.Program("shaders/shadowmap.vertexshader",
                                        "shaders/shadowmap.fragmentshader")

    def _loadShaders(self):
        light_number = len(self._lights)
        light_number_float = float(light_number)
        fragment = open(self.FRAGMENT_SHADER_FILENAME, 'r')
        fragment_str = fragment.read()
        fragment_str = fragment_str.replace("$LIGHT_NUMBER$", str(light_number))
        fragment_str = fragment_str.replace("$LIGHT_NUMBER_FLOAT$", str(light_number_float))
        vertex = open(self.VERTEX_SHADER_FILENAME, 'r')
        vertex_str = vertex.read()
        vertex_str = vertex_str.replace("$LIGHT_NUMBER$", str(light_number))
        vertex_str = vertex_str.replace("$LIGHT_NUMBER_FLOAT$", str(light_number_float))
        self._program = gloo.Program(vertex_str, fragment_str)
        fragment.close()
        vertex.close()
        self._program['position'] = self._positions
        self._program['normal'] = self._normals
        self._shadowProgram['position'] = self._positions
        # Shadow map
        self._shadowMaps = []
        self._frameBuffers = []
        shape = 768,1366
        for light in self._lights:
            shadowMap = gloo.Texture2D(shape=(shape + (4,)), dtype=numpy.float32)
            self._shadowMaps.append(shadowMap)
            self._frameBuffers.append(gloo.FrameBuffer(shadowMap))
        self._old_light_number = light_number

    def init(self, positions, indices, normals, camera, lightList):
        """ Method that initialize the algorithm """
        self._positions = gloo.VertexBuffer(positions)
        self._indices = gloo.IndexBuffer(numpy.array(indices))
        self._normals = gloo.VertexBuffer(normals)
        self._camera = camera
        self._lights = lightList
        self._loadShaders()
        self.active = True

        # matrices
        self._projection = perspective(60, 16.0/9.0, 0.1, 50)
        self._shadow_projection = ortho(-5, +5, -5, +5, 10, 50)

    def update(self):
        if len(self._lights) != self._old_light_number:
            self._loadShaders()
        """ Method to call on each OpenGL update """
        if self.active:
            # create render matrices
            view = createViewMatrix(self._camera)
            model = numpy.eye(4, dtype=numpy.float32)
            for i in range(len(self._frameBuffers)):
                # create shadow map matrices
                shadow_model = numpy.eye(4, dtype=numpy.float32)
                shadow_view = lookAt(self._lights[i].getPosition(), (0,2,0), (0,1,0))
                self._program['u_depth_model[%d]' % i] = shadow_model
                self._program['u_depth_view[%d]' % i] = shadow_view
                self._program['u_depth_projection[%d]' % i] = self._shadow_projection
                # create shadow map
                with self._frameBuffers[i]:
                    self._shadowProgram['u_projection'] = self._shadow_projection
                    self._shadowProgram['u_model'] = shadow_model
                    self._shadowProgram['u_view'] = shadow_view
                    self._shadowProgram.draw('triangles', self._indices)

            # draw scene
            biasMatrix = numpy.matrix( [[0.5, 0.0, 0.0, 0.0],
                                        [0.0, 0.5, 0.0, 0.0],
                                        [0.0, 0.0, 0.5, 0.0],
                                        [0.5, 0.5, 0.5, 1.0]])
            # normal = numpy.array(numpy.matrix(numpy.dot(view, model)).I.T)
            self._program['u_model'] = model
            self._program['u_view'] = view
            self._program['u_projection'] = self._projection
            self._program['u_bias_matrix'] = biasMatrix
            for i in range(len(self._shadowMaps)):
                self._program['u_shadow_maps[%d]' % i] = self._shadowMaps[i]
            self._program['u_color'] = DEFAULT_COLOR # TODO remove hardcoded value
            for i in range(len(self._lights)):
                self._program['u_lights_intensity[%d]' % i] = self._lights[i].getIntensity()
            for i in range(len(self._lights)):
                self._program['u_lights_position[%d]' % i] = self._lights[i].getPosition()
            self._program.draw('triangles', self._indices)

            # draw shadowmap as minimap
            # GL.glViewport(0,0,228,128)
            # self._shadowMap.draw('triangles', self._indices)
            GL.glViewport(0,0,1366,768)

    def terminate(self):
        """ Method to stop algorithm """
        self.active = False
        self._positions = []
        self._indices = []
        self._normals = []
        self._camera = None
        self._light = None

class RayTracingAlgorithm:
    def __init__(self):

        self.program = gloo.Program("shaders/raytracingalgo.vertexshader", "shaders/raytracingalgo.fragmentshader")

    def init(self, positions, indices, normals, camera, lightList):
        self._positions = gloo.VertexBuffer(positions)
        self._indices = gloo.IndexBuffer(numpy.array(indices))
        self._normals = gloo.VertexBuffer(normals)
        self._camera = camera
        self._light = lightList[0]
        self.program['a_position'] = [(-1., -1.), (-1., +1.),
                                      (+1., -1.), (+1., +1.)]

        self.program['plane_position'] = (0., -.5, 0.)
        self.program['plane_normal'] = (0., 1., 0.)

        self.program['light_intensity'] = 1.
        self.program['light_specular'] = (1., 50.)
        self.program['light_position'] = (5., 5., -10.)
        self.program['light_color'] = (1., 1., 1.)
        self.program['ambient'] = .05
        self.program['O'] = (0., 0., -1.)
        self.active = True

    def update(self):
        if self.active:
            pass

    def terminate(self):
        self.active = False
        self._positions = []
        self._indices = []
        self._normals = []
        self._camera = None
        self._light = None

class NoShadowAlgorithm:
    def __init__(self):
        self._program = gloo.Program("shaders/noshadowalgo.vertexshader", "shaders/noshadowalgo.fragmentshader")

    def init(self, positions, indices, normals, camera, lightList):
        self._positions = gloo.VertexBuffer(positions)
        self._indices = gloo.IndexBuffer(numpy.array(indices))
        self._normals = gloo.VertexBuffer(normals)
        self._camera = camera
        self._light = lightList[0]
        self._projection = perspective(60, 4.0/3.0, 0.1, 100)

        self.active = True


        self._program['position'] = self._positions
        self._program.draw('triangles', self._indices)

    def update(self):
        if self.active:
            # create render matrices
            view = createViewMatrix(self._camera)
            model = numpy.eye(4, dtype=numpy.float32)
            # draw scene
            self._program['u_model'] = model
            self._program['u_view'] = view
            self._program['u_projection'] = self._projection
            self._program['u_color'] = DEFAULT_COLOR 
            self._program.draw('triangles', self._indices)

    def terminate(self):
        self.active = False
        self._positions = []
        self._indices = []
        self._normals = []
        self._camera = None
        self._light = None


class SelfShadowAlgorithm:
    def __init__(self):
        self._program = gloo.Program("shaders/selfshadowalgo.vertexshader", "shaders/selfshadowalgo.fragmentshader")

    def init(self, positions, indices, normals, camera, lightList):
        self._positions = gloo.VertexBuffer(positions)
        self._indices = gloo.IndexBuffer(numpy.array(indices))
        self._normals = gloo.VertexBuffer(normals)
        self._camera = camera
        self._light = lightList[0]
        self._projection = perspective(60, 4.0/3.0, 0.1, 100)

        self.active = True

        self._program['u_light_intensity'] = self._light.getIntensity()
        self._program['u_light_position'] = self._light.getPosition()
        self._program['normal'] = self._normals
        self._program['position'] = self._positions
        self._program.draw('triangles', self._indices)

    def update(self):
        if self.active:
            # create render matrices
            view = createViewMatrix(self._camera)
            model = numpy.eye(4, dtype=numpy.float32)
            # draw scene
            normal = numpy.array(numpy.matrix(numpy.dot(view, model)).I.T)
            self._program['u_normal'] = normal
            self._program['u_light_position'] = self._light.getPosition()
            self._program['u_light_intensity'] = self._light.getIntensity()
            self._program['u_model'] = model
            self._program['u_view'] = view
            self._program['u_projection'] = self._projection
            self._program['u_color'] = DEFAULT_COLOR 
            self._program.draw('triangles', self._indices)

    def terminate(self):
        self.active = False
        self._positions = []
        self._indices = []
        self._normals = []
        self._camera = None
        self._light = None


