from OpenGL import GL, GLU
from vispy import gloo
from vispy.util.transforms import *
import numpy

from Camera import Camera
from Light import Light
from Utils import *

class ShadowMapAlgorithm:
    def __init__(self, positions, indices, normals, camera, light):
        # assign members that never change
        self._program = gloo.Program("shaders/shadowmapalgo.vertexshader",
                                    "shaders/shadowmapalgo.fragmentshader")
        self._shadowMap = gloo.Program("shaders/shadowmap.vertexshader",
                                        "shaders/shadowmap.fragmentshader")
        # assign members that change when changing scene
        self.init(positions, indices, normals, camera, light)

        # Shadow map
        shape = 1024,1024
        self._renderTexture = gloo.Texture2D(shape=(shape + (4,)), dtype=numpy.float32)
        self._fbo = gloo.FrameBuffer(self._renderTexture)

        # matrices
        self._projection = perspective(60, 4.0/3.0, 0.1, 100)
        self._shadow_projection = ortho(-20,20,-20,30,0,100)

    def init(self, positions, indices, normals, camera, light):
        """ Method that initialize the algorithm """
        self._positions = gloo.VertexBuffer(positions)
        self._indices = gloo.IndexBuffer(numpy.array(indices))
        self._normals = gloo.VertexBuffer(normals)
        self._camera = camera
        self._light = light
        self._program['position'] = self._positions
        self._program['normal'] = self._normals
        self._shadowMap['position'] = self._positions
        self.active = True

    def update(self):
        """ Method to call on each OpenGL update """
        if self.active:
            # create render matrices
            view = numpy.eye(4, dtype=numpy.float32)
            translate(view, 0, -4, self._camera.getZoom())
            model = numpy.eye(4, dtype=numpy.float32)
            rotate(model, self._camera.getX(), 1, 0, 0)
            rotate(model, self._camera.getY(), 0, 1, 0)
            rotate(model, self._camera.getZ(), 0, 0, 1)
            # create shadow map matrices
            shadow_model = numpy.eye(4, dtype=numpy.float32)
            shadow_view = lookAt(self._light.getPosition(), (0,0,0), (0,1,0))
            # create shadow map
            with self._fbo:
                self._shadowMap['u_projection'] = self._shadow_projection
                self._shadowMap['u_model'] = shadow_model
                self._shadowMap['u_view'] = shadow_view
                self._shadowMap.draw('triangles', self._indices)

            # draw scene
            biasMatrix = numpy.matrix([[0.5, 0.0, 0.0, 0.0],
                                    [0.0, 0.5, 0.0, 0.0],
                                    [0.0, 0.0, 0.5, 0.0],
                                    [0.5, 0.5, 0.5, 1.0]])
            normal = numpy.array(numpy.matrix(numpy.dot(view, model)).I.T)
            self._program['u_normal'] = normal
            self._program['u_light_position'] = self._light.getPosition()
            self._program['u_light_intensity'] = self._light.getIntensity()
            self._program['u_model'] = model
            self._program['u_view'] = view
            self._program['u_projection'] = self._projection
            self._program['u_bias_matrix'] = biasMatrix
            self._program['u_depth_model'] = shadow_model
            self._program['u_depth_view'] = shadow_view
            self._program['u_depth_projection'] = self._shadow_projection
            self._program['u_shadow_map'] = self._renderTexture
            self._program['u_color'] = (0.5, 0.5, 0.8, 1) # TODO remove hardcoded value
            self._program.draw('triangles', self._indices)

            # draw shadowmap as minimap
            GL.glViewport(0,0,256,256)
            self._shadowMap.draw('triangles', self._indices)
            GL.glViewport(0,0,1024,1024)

    def terminate(self):
        """ Method to stop algorithm """
        self.active = False
        self._positions = []
        self._indices = []
        self._normals = []
        self._camera = None
        self._light = None

class RayTracingAlgorithm:
    def __init__(self, positions, indices, normals, camera, light):

        self.program = gloo.Program("shaders/raytracingalgo.vertexshader", "shaders/raytracingalgo.fragmentshader")

        self.init(positions, indices, normals, camera, light)

    def init(self, positions, indices, normals, camera, light):
        self._positions = gloo.VertexBuffer(positions)
        self._indices = gloo.IndexBuffer(numpy.array(indices))
        self._normals = gloo.VertexBuffer(normals)
        self._camera = camera
        self._light = light
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
        self.program = gloo.Program("shaders/noshadowalgo.vertexshader", "shaders/noshadowalgo.fragmentshader")
        self.init()

    def init(self):
        self._positions = gloo.VertexBuffer(positions)
        self._indices = gloo.IndexBuffer(numpy.array(indices))
        self._normals = gloo.VertexBuffer(normals)
        self._camera = camera
        self._light = light

        self.program['light_intensity'] = 1.
        self.program['light_specular'] = (1., 50.)
        self.program['light_position'] = (5., 5., -10.)
        self.program['light_color'] = (1., 1., 1.)
        self._program.draw('triangles', self._indices)
        self.active = True

    def update(self):

        if self.active:
            # create render matrices
            view = numpy.eye(4, dtype=numpy.float32)
            translate(view, 0, -4, self._camera.getZoom())
            model = numpy.eye(4, dtype=numpy.float32)
            rotate(model, self._camera.getX(), 1, 0, 0)
            rotate(model, self._camera.getY(), 0, 1, 0)
            rotate(model, self._camera.getZ(), 0, 0, 1)
            # create shadow map
            with self._fbo:
                self._shadowMap['u_projection'] = self._shadow_projection
                self._shadowMap['u_model'] = shadow_model
                self._shadowMap['u_view'] = shadow_view
                self._shadowMap.draw('triangles', self._indices)

            # draw scene
            self._program['u_light_position'] = self._light.getPosition()
            self._program['u_light_intensity'] = self._light.getIntensity()
            self._program['u_model'] = model
            self._program['u_view'] = view
            self._program['u_projection'] = self._projection
            self._program['u_color'] = (0.5, 0.5, 0.8, 1) # TODO remove hardcoded value
            self._program.draw('triangles', self._indices)

    def terminate(self):
        self.active = False
        self._positions = []
        self._indices = []
        self._normals = []
        self._camera = None
        self._light = None



