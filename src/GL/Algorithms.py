#!/usr/bin/python2
# -*- coding: utf-8 -*-

from OpenGL import GL, GLU
from vispy import gloo
from vispy.util.transforms import *
import numpy
from operator import add
from vispy.geometry import *

from Camera import Camera
from Light import Light
from Utils import *

def concatPositions(verticesList, positionList):
    ret = []
    for i in range(len(verticesList)):
        ret.extend(move(verticesList[i], positionList[i]))
    return ret

def move(vertices, position):
    return [[vertex[i]+position[i] for i in range(len(vertex))] for vertex in vertices]

# add index so mesh reference only their vertices
def concatIndices(indicesList):
    def addIndices(newIndices, indices):
        max_index = max(newIndices)+1 if len(newIndices) > 0 else 0
        try:
            newIndices.extend([item+max_index for sublist in indices for item in sublist])
        except:
            newIndices.extend([item+max_index for item in indices])
        return newIndices
    return reduce(addIndices, indicesList, [])

def concatNormals(normalsList):
    return reduce(add, normalsList, [])

DEFAULT_COLOR = (0.7, 0.7, 0.7, 1)

class AbstractAlgorithm:
    def __init__(self):
        pass

    def init(self, objects, camera, lights):
        self._objects = objects
        self._positions = gloo.VertexBuffer(concatPositions([obj.getVertices().tolist() for obj in objects], \
                                                            [obj.getPosition() for obj in objects]))
        self._indices = gloo.IndexBuffer(numpy.array(concatIndices([obj.getIndices().tolist() for obj in objects])))
        self._normals = gloo.VertexBuffer(concatNormals([obj.getNormals().tolist() for obj in objects]))
        self._camera = camera
        self._lights = lights
        vertex_str, fragment_str = self._loadShaders()

        self._projection = self._createProjectionMatrix()
        self._programs = []
        for obj in self._objects:
            newProg = gloo.Program(vertex_str, fragment_str)
            newProg['position'] = obj.getVertexBuffer()
            if not obj.getColor():
                newProg['u_color'] = DEFAULT_COLOR
            else:
                newProg['u_color'] = obj.getColorAlpha()
            newProg['u_projection'] = self._projection
            self._programs.append(newProg)
        self.active = True

    def update(self):
        if len(self._lights) != self._old_light_number:
            print "lights"
            self._loadShaders()

    def draw(self):
        view = self._createViewMatrix()
        for i in range(len(self._objects)):
            obj = self._objects[i]
            prog = self._programs[i]
            model = numpy.eye(4, dtype=numpy.float32)
            translate(model, *obj.getPosition())
            prog['u_model'] = model
            prog['u_view'] = view
            prog.draw('triangles', obj.getIndexBuffer())

    def terminate(self):
        """ Method to stop algorithm """
        self.active = False
        self._objects = []
        self._positions = []
        self._indices = []
        self._normals = []
        self._camera = None
        self._lights = []

    def _createViewMatrix(self):
        view = numpy.eye(4, dtype=numpy.float32)
        translate(view, -self._camera.getX(), -self._camera.getY(), -self._camera.getZ())
        rotate(view, -self._camera.getDirectionY(), 0, 1, 0)
        rotate(view, -self._camera.getDirectionX(), 1, 0, 0)
        return view

    def _createProjectionMatrix(self):
        return perspective(60, 16.0/9.0, 0.1, 50)

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
        fragment.close()
        vertex.close()
        self._old_light_number = light_number
        return vertex_str, fragment_str


class ShadowMapAlgorithm(AbstractAlgorithm):
    FRAGMENT_SHADER_FILENAME = "shaders/shadowmapalgo.fragmentshader"
    VERTEX_SHADER_FILENAME = "shaders/shadowmapalgo.vertexshader"
    BIAS_MATRIX = numpy.matrix([[0.5, 0.0, 0.0, 0.0],
                                [0.0, 0.5, 0.0, 0.0],
                                [0.0, 0.0, 0.5, 0.0],
                                [0.5, 0.5, 0.5, 1.0]])
    def __init__(self):
        AbstractAlgorithm.__init__(self)
        # assign members that never change
        self._shadowProgram = gloo.Program("shaders/shadowmap.vertexshader",
                                        "shaders/shadowmap.fragmentshader")

    def init(self, objects, camera, lights):
        """ Method that initialize the algorithm """
        AbstractAlgorithm.init(self, objects, camera, lights)

        for i in range(len(self._programs)):
            obj = self._objects[i]
            prog = self._programs[i]
            prog['u_bias_matrix'] = self.BIAS_MATRIX
            prog['normal'] = obj.getNormalBuffer()

        self._shadowProgram['position'] = self._positions
        # Shadow map
        self._shadowMaps = []
        self._frameBuffers = []
        shape = 768,1366
        for light in self._lights:
            shadowMap = gloo.Texture2D(shape=(shape + (4,)), dtype=numpy.float32)
            self._shadowMaps.append(shadowMap)
            self._frameBuffers.append(gloo.FrameBuffer(shadowMap))

    def update(self):
        """ Method to call on each OpenGL update """
        if self.active:
            AbstractAlgorithm.update(self)
            # create shadow map for each light
            for i in range(len(self._frameBuffers)):
                # create shadow map matrices
                shadow_model = numpy.eye(4, dtype=numpy.float32)
                shadow_view = lookAt(self._lights[i].getPosition(), (0,2,0), (0,1,0))
                # TODO change in function of light type
                shadow_projection = ortho(-5, +5, -5, +5, 10, 50)
                for prog in self._programs:
                    prog['u_depth_model[%d]' % i] = shadow_model
                    prog['u_depth_view[%d]' % i] = shadow_view
                    prog['u_depth_projection[%d]' % i] = shadow_projection
                # create shadow map
                with self._frameBuffers[i]:
                    self._shadowProgram['u_model'] = shadow_model
                    self._shadowProgram['u_view'] = shadow_view
                    self._shadowProgram['u_projection'] = shadow_projection
                    self._shadowProgram.draw('triangles', self._indices)

            # draw each object
            for prog in self._programs:
                for i in range(len(self._lights)):
                    prog['u_lights_intensity[%d]' % i] = self._lights[i].getIntensity()
                for i in range(len(self._lights)):
                    prog['u_lights_position[%d]' % i] = self._lights[i].getPosition()
                for i in range(len(self._shadowMaps)):
                    prog['u_shadow_maps[%d]' % i] = self._shadowMaps[i]
            self.draw()

            # draw shadowmap as minimap
            # GL.glViewport(0,0,228,128)
            # self._shadowMap.draw('triangles', self._indices)
            GL.glViewport(0,0,1366,768)

class RayTracingAlgorithm:
    def __init__(self):
        self.program = gloo.Program("shaders/raytracingalgo.vertexshader", "shaders/raytracingalgo.fragmentshader")

    def init(self, objects, camera, lightList):
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

class NoShadowAlgorithm(AbstractAlgorithm):
    VERTEX_SHADER_FILENAME="shaders/noshadowalgo.vertexshader"
    FRAGMENT_SHADER_FILENAME="shaders/noshadowalgo.fragmentshader"
    def __init__(self):
        AbstractAlgorithm.__init__(self)

    def init(self, objects, camera, lights):
        AbstractAlgorithm.init(self, objects, camera, lights)

    def update(self):
        if self.active:
            self.draw()

class SelfShadowAlgorithm(AbstractAlgorithm):
    VERTEX_SHADER_FILENAME="shaders/selfshadowalgo.vertexshader"
    FRAGMENT_SHADER_FILENAME="shaders/selfshadowalgo.fragmentshader"
    def __init__(self):
        AbstractAlgorithm.__init__(self)

    def init(self, objects, camera, lights):
        AbstractAlgorithm.init(self, objects, camera, lights)

        for i in range(len(self._programs)):
            obj = self._objects[i]
            prog = self._programs[i]
            prog['normal'] = obj.getNormalBuffer()

    def update(self):
        if self.active:
            for i in range(len(self._programs)):
                obj = self._objects[i]
                prog = self._programs[i]
                model = numpy.eye(4, dtype=numpy.float32)
                translate(model, *obj.getPosition())
                view = self._createViewMatrix()
                normal = numpy.array(numpy.matrix(numpy.dot(view, model)).I.T)
                prog['u_normal'] = normal
                prog['u_light_position'] = self._lights[0].getPosition()
                prog['u_light_intensity'] = self._lights[0].getIntensity()
            self.draw()


class ShadowVolumeAlgorithm:
    def __init__(self):
        self._program = gloo.Program("shaders/shadowvolume.vertexshader",
            "shaders/shadowvolume.fragmentshader")

    def init(self, objects, camera, lightList):
        self._objects = objects
        self._camera = camera
        self._light = lightList[0]
        self._projection = createProjectionMatrix()
        # self._program['normal'] = self._normals
        # self._program['position'] = self._positions

        # shape=(1366,768)
        # self._color_buffer = gloo.ColorBuffer(shape=(shape + (4,)))
        # self._depth_buffer = gloo.DepthBuffer(shape=(shape + (4,)))
        # self._stencil_buffer = gloo.StencilBuffer(shape=(shape + (4,)))
        # self._frame_buffer = gloo.FrameBuffer(self._color_buffer,
                                                # self._depth_buffer,
                                                # self._stencil_buffer)
        self.active = True

    # http://nuclear.mutantstargoat.com/articles/volume_shadows_tutorial_nuclear.pdf
    def drawVolumes(self):
        # for each object
        for i in range(len(self._objects)):
            contour_edges = self.findContourEdges(i)
            shadow_triangles = self.drawShadowTriangles(contour_edges)

    def findContourEdges(self, index):
        positions = self._objects[index].getVertices()
        indices = self._objects[index].getIndices()
        normals = self._objects[index].getNormals()
        ret = numpy.array([])
        lightPosition = numpy.dot(self._light.getPosition() + [0], numpy.linalg.inv(self._model))
        for i in range(0,len(indices), 3):
            a = indices[i]
            b = indices[i+1]
            c = indices[i+2]
            triangle = numpy.array([positions[a], positions[b], positions[c]])
            averageTrianglePos = numpy.array([sum([x[0] for x in triangle])/3.0,
                                  sum([x[1] for x in triangle])/3.0,
                                  sum([x[2] for x in triangle])/3.0, 0.0])
            lightDir = numpy.subtract(averageTrianglePos, lightPosition)
            triangleNormal = numpy.append(numpy.cross(numpy.subtract(triangle[1], triangle[0]), numpy.subtract(triangle[2], triangle[0])), numpy.array([1]))
            if numpy.dot(lightDir, triangleNormal) >= 0:
                for edge in numpy.nditer(numpy.array([[positions[a], positions[b]],[positions[a], positions[c]],[positions[b], positions[c]]])):
                    if edge in ret.tolist() or [edge[1], edge[0]] in ret.tolist():
                        try:
                            ret.remove(edge)
                        except Exception, e:
                            ret.remove([edge[1], edge[0]])
                    else:
                        numpy.append(ret,edge)
        return ret

    def drawShadowTriangles(self, contour_edges):
        lightPosition = numpy.dot(self._light.getPosition() + [0], numpy.linalg.inv(self._model))
        extrudeMagnitude = 20
        shadow_triangles = []
        for edge in contour_edges:
            a = edge[0]
            b = edge[1]
            c = numpy.add(numpy.append(edge[1], [0]), extrudeMagnitude * numpy.subtract(numpy.append(edge[1], [0]), lightPosition)).tolist()
            d = numpy.add(numpy.append(edge[0], [0]), extrudeMagnitude * numpy.subtract(numpy.append(edge[0], [0]), lightPosition)).tolist()
            shadow_triangles.append([a, b, c])
            shadow_triangles.append([a, c, d])
        vertices = []
        for triangle in shadow_triangles:
            for vertex in triangle:
                vertices.append([vertex[0], vertex[1], vertex[2]])
        program = gloo.Program("shaders/noshadowalgo.vertexshader", "shaders/noshadowalgo.fragmentshader")
        program['position'] = gloo.VertexBuffer(vertices)
        program['u_model'] = self._model
        program['u_view'] = self._view
        program['u_projection'] = self._projection
        program['u_color'] = DEFAULT_COLOR
        program.draw('triangles')


    def update(self):
        if self.active:
            # create render matrices
            self._view = createViewMatrix(self._camera)
            self._model = numpy.eye(4, dtype=numpy.float32)

            #create shadow volumes
            self._volumes = self.drawVolumes()

            # draw scene
            # normal = numpy.array(numpy.matrix(numpy.dot(view, model)).I.T)
            # self._program['u_normal'] = normal
            # self._program['u_light_position'] = self._light.getPosition()
            # self._program['u_light_color'] = self._light.getColor()
            # self._program['u_model'] = self._model
            # self._program['u_view'] = self._view
            # self._program['u_projection'] = self._projection
            # self._program['u_color'] = (0.5, 0.5, 0.8)
            # # shadow volumes creation
            # # http://archive.gamedev.net/archive/reference/articles/article1990.html
            # with self._frame_buffer:
            #     # step 1 : render scene with lights turned off
            #     self._color_buffer.activate()
            #     self._depth_buffer.activate()
            #     self._program['u_light_color'] = (0,0,0)
            #     self._program.draw('triangles', self._indices)
            #     self._program['u_light_color'] = self._light.getColor()
            #     # step 2 : turn off color and depth buffers
            #     self._color_buffer.deactivate()
            #     self._depth_buffer.deactivate()
            #     self._stencil_buffer.activate()
            #     gloo.set_state(None, cull_face=True)
            #     gloo.set_state(None, stencil_test=True)
            #     # step 3 : draw front faces, depth test and stencil buffer increment
            #     gloo.set_stencil_func('always', 0, 0)
            #     gloo.set_stencil_op('keep', 'incr', 'keep')
            #     gloo.set_cull_face('front')
            #     self._program.draw('triangles', self._indices) # SHOULD DRAW SHADOW VOLUMES
            #     # step 4 : draw back faces, depth test and stencil buffer decrement
            #     gloo.set_stencil_op('keep', 'decr', 'keep')
            #     gloo.set_cull_face('back')
            #     self._program.draw('triangles', self._indices) # SHOULD DRAW SHADOW VOLUMES
            # self._color_buffer.activate()
            # self._depth_buffer.activate()
            # # step 5 : turn on color and depth buffers
            # gloo.set_depth_func('equal')
            # gloo.set_state(None, stencil_test=True)
            # gloo.set_stencil_func('equal', 0, 0)
            # gloo.set_stencil_op('keep', 'keep', 'keep')
            # # step 6 : draw scene with lights turned on where stencil buffer is 0


            # # draw scene
            # self._program.draw('triangles', self._indices)

    def terminate(self):
        self.active = False
        self._positions = []
        self._indices = []
        self._normals = []
        self._camera = None
        self._light = None


if __name__ == '__main__':
    # unit test for shadow volume contour edges
    cube_positions = [[1,1,1],[1,1,0],[0,1,0],[0,1,1],
                       [1,0,1],[1,0,0],[0,0,0],[0,0,1]]
    cube_indices =  [0,1,2, 0,2,3, 0,3,4, 7,4,3, 0,4,5, 0,5,1,
                      2,1,5, 2,5,6, 7,3,2, 7,2,6, 6,5,4, 6,4,7]
    cube_normals = []
    for index in range(len(cube_positions)):
        prev = cube_positions[index-1]
        curr = cube_positions[index]
        next = cube_positions[(index+1)%len(cube_positions)]
        diff1 = numpy.subtract(prev, curr)
        diff2 = numpy.subtract(next, curr)
        cube_normals.append(numpy.cross(diff2, diff1))
    camera = Camera()
    camera.setX(2)
    camera.setY(2)
    camera.setZ(-2)
    light = Light()
    light.setPosition([2,2,-2])
    shadowvolumealgo = ShadowVolumeAlgorithm()
    shadowvolumealgo.init([cube_positions], [cube_indices], [cube_normals], camera, light)
    shadowvolumealgo.update()
    # print shadowvolumealgo.findContourEdges(0)
