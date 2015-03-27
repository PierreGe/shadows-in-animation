#!/usr/bin/python2
# -*- coding: utf-8 -*-

from OpenGL import GL, GLU
from vispy import gloo
from vispy.util.transforms import *
from vispy.io import imread, imsave
from vispy.scene import Image
from operator import add
from vispy.geometry import *
from ctypes import *
import numpy
import time
libvolume = cdll.LoadLibrary("GLShadow/shadow_volume.so")

from GLShadow.Camera import Camera
from GLShadow.Light import Light
from GLShadow.Utils import *
from GLShadow.SceneObject import SceneObject
from GLShadow.ObjParser import ObjParser

DEFAULT_COLOR = (0.7, 0.7, 0.7, 1)
DEFAULT_SHAPE = (1920,1080)

class AbstractAlgorithm:
    def __init__(self):
        pass

    def init(self, objects, camera, lights, options):
        self._objects = objects
        self._positions = gloo.VertexBuffer(self._concatPositions())
        self._indices = gloo.IndexBuffer(numpy.array(self._concatIndices()))
        self._normals = gloo.VertexBuffer(self._concatNormals())
        self._camera = camera
        self._lights = lights
        self._options = options
        if not self._options:
            self._options = {"anti-aliasing-int" : "4", 
                             "anti-aliasing-float" : "4.0",
                             "spreading" : "700.0",
                             "bias" : "0.05"}
        vertex_str, fragment_str = self._loadShaders()
        vertex_texture, fragment_texture = self._loadShaders(texture=True)

        self._projection = self._createProjectionMatrix()
        self._programs = []
        for obj in self._objects:
            if obj.getTexture():
                newProg = gloo.Program(vertex_texture, fragment_texture)
                newProg['u_texture'] = gloo.Texture2D(imread(obj.getTexture()))
                newProg['texcoord'] = obj.getTexBuffer()
            else:
                newProg = gloo.Program(vertex_str, fragment_str)
                if obj.getColor():
                    newProg['u_color'] = obj.getColorAlpha()
                else:
                    newProg['u_color'] = DEFAULT_COLOR
            newProg['position'] = obj.getVertexBuffer()
            newProg['u_projection'] = self._projection
            self._programs.append(newProg)

        self._lightObjects = self._createLightObjects()
        self._lightPrograms = self._createLightPrograms()
        self.active = True
        self._fps = 1

    def timedUpdate(self):
        start = time.time() 
        self.update()
        elapsed = time.time()
        elapsed = elapsed - start
        self._fps = 1/elapsed

    def getFPS(self):
        """ """
        return self._fps

    def update(self):
        pass

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

        for i in range(len(self._lightPrograms)):
            obj = self._lightObjects[i]
            prog = self._lightPrograms[i]
            model = numpy.eye(4,dtype=numpy.float32)
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
        return perspective(60, 16.0/9.0, 0.1, 200)

    def _loadShaders(self, texture=False, vertex_filename=None, fragment_filename=None):
        if not vertex_filename:
            vertex_filename = self.VERTEX_SHADER_FILENAME
        if not fragment_filename:
            fragment_filename = self.FRAGMENT_SHADER_FILENAME
        light_number = len(self._lights)
        light_number_float = float(light_number)
        fragment = open(fragment_filename, 'r')
        fragment_str = fragment.read()
        fragment_str = fragment_str.replace("$LIGHT_NUMBER$", str(light_number))
        fragment_str = fragment_str.replace("$LIGHT_NUMBER_FLOAT$", str(light_number_float))
        vertex = open(vertex_filename, 'r')
        vertex_str = vertex.read()
        vertex_str = vertex_str.replace("$LIGHT_NUMBER$", str(light_number))
        vertex_str = vertex_str.replace("$LIGHT_NUMBER_FLOAT$", str(light_number_float))
        if texture:
            vertex_str = vertex_str.replace("$COLOR_VARIABLES$", "attribute vec2 texcoord;\nvarying vec2 v_texcoord;\n")
            vertex_str = vertex_str.replace("$COLOR_CODE$", "v_texcoord = texcoord;\n")
            fragment_str = fragment_str.replace("$COLOR_VARIABLES$", "varying vec2 v_texcoord;\nuniform sampler2D u_texture;\n")
            fragment_str = fragment_str.replace("$COLOR_CODE$", "vec4 v_color = texture2D(u_texture, v_texcoord);\n")

        else:
            vertex_str = vertex_str.replace("$COLOR_VARIABLES$", "uniform vec4 u_color;\nvarying vec4 v_color;\n")
            vertex_str = vertex_str.replace("$COLOR_CODE$", "v_color = u_color;\n")
            fragment_str = fragment_str.replace("$COLOR_VARIABLES$", "varying vec4 v_color;\n")
            fragment_str = fragment_str.replace("$COLOR_CODE$", "");

        if (self._options):
            for key, value in self._options.iteritems():
                vertex_str = vertex_str.replace('$'+key+'$', value)
                fragment_str = fragment_str.replace('$'+key+'$', value)

        fragment.close()
        vertex.close()
        self._old_light_number = light_number
        return vertex_str, fragment_str

    def _createLightObjects(self):
        objects = []
        for light in self._lights:
            sphere = ObjParser("assets/obj/spotlight/spotlight.obj")
            newObj = SceneObject(sphere.getVertices(), sphere.getFaces(), sphere.getNormals(), light.getPosition(), [0.5,0.5,0.5])
            objects.append(newObj)
        return objects

    def _createLightPrograms(self):
        programs = []
        for obj in self._lightObjects:
            newProg = gloo.Program("shaders/light.vertexshader", "shaders/light.fragmentshader")
            newProg['position'] = obj.getVertexBuffer()
            newProg['u_color'] = obj.getColorAlpha()
            newProg['u_projection'] = self._projection
            programs.append(newProg)
        return programs

    def _concatPositions(self):
        def move(vertices, position):
            return [[vertex[i]+position[i] for i in range(len(vertex))] for vertex in vertices]
        verticesList = [obj.getVertices().tolist() for obj in self._objects]
        positionList = [obj.getPosition() for obj in self._objects]
        ret = []
        for i in range(len(verticesList)):
            ret.extend(move(verticesList[i], positionList[i]))
        return ret

    # add index so mesh reference only their vertices
    def _concatIndices(self):
        indicesList = [obj.getIndices().tolist() for obj in self._objects]
        def addIndices(newIndices, indices):
            max_index = max(newIndices)+1 if len(newIndices) > 0 else 0
            try:
                newIndices.extend([item+max_index for sublist in indices for item in sublist])
            except:
                newIndices.extend([item+max_index for item in indices])
            return newIndices
        return reduce(addIndices, indicesList, [])

    def _concatNormals(self):
        normalsList = [obj.getNormals().tolist() for obj in self._objects]
        return reduce(add, normalsList, [])


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

    def init(self, objects, camera, lights, options):
        """ Method that initialize the algorithm """
        AbstractAlgorithm.init(self, objects, camera, lights, options)

        for i in range(len(self._programs)):
            obj = self._objects[i]
            prog = self._programs[i]
            prog['u_bias_matrix'] = self.BIAS_MATRIX
            prog['normal'] = obj.getNormalBuffer()

        self._shadowProgram['position'] = self._positions
        # Shadow map
        self._shadowMaps = []
        self._frameBuffers = []
        for light in self._lights:
            shadowMap = gloo.Texture2D(shape=(DEFAULT_SHAPE[1], DEFAULT_SHAPE[0], 4), dtype=numpy.float32)
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
                    prog['u_lights_position[%d]' % i] = self._lights[i].getPosition()
                for i in range(len(self._shadowMaps)):
                    prog['u_shadow_maps[%d]' % i] = self._shadowMaps[i]
            self.draw()

            # draw shadowmap as minimap
            # GLShadow.glViewport(0,0,228,128)
            # self._shadowMap.draw('triangles', self._indices)

class RayTracingAlgorithm:
    def __init__(self):
        self.program = gloo.Program("shaders/raytracingalgo.vertexshader", "shaders/raytracingalgo.fragmentshader")

    def init(self, objects, camera, lightList, options):
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

    def init(self, objects, camera, lights, options):
        AbstractAlgorithm.init(self, objects, camera, lights, options)

    def update(self):
        if self.active:
            self.draw()

class SelfShadowAlgorithm(AbstractAlgorithm):
    VERTEX_SHADER_FILENAME="shaders/selfshadowalgo.vertexshader"
    FRAGMENT_SHADER_FILENAME="shaders/selfshadowalgo.fragmentshader"
    def __init__(self):
        AbstractAlgorithm.__init__(self)

    def init(self, objects, camera, lights, options):
        AbstractAlgorithm.init(self, objects, camera, lights, options)

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


class Vector(Structure):
    _fields_ = ("x", c_float), ("y", c_float), ("z", c_float)

class Edge(Structure):
    _fields_ = ("one", Vector), ("two", Vector)

class ShadowVolumeAlgorithm(AbstractAlgorithm):
    VERTEX_SHADER_FILENAME="shaders/shadowvolume.vertexshader"
    FRAGMENT_SHADER_FILENAME="shaders/shadowvolume.fragmentshader"
    def __init__(self):
        AbstractAlgorithm.__init__(self)

    def init(self, objects, camera, lights, options):
        AbstractAlgorithm.init(self, objects, camera, lights, options)

        shape=DEFAULT_SHAPE

        self.C_positions = [None for _ in range(len(self._objects))]
        self.C_indices = [None for _ in range(len(self._objects))]
        self.C_normals = [None for _ in range(len(self._objects))]
        self.C_size_indices = [None for _ in range(len(self._objects))]
        self.C_contour_edges = [None for _ in range(len(self._objects))]
        self.C_nb_edges = [None for _ in range(len(self._objects))]
        self._volumePrograms = [None for _ in range(len(self._objects))]
        vertex_str, fragment_str = \
            self._loadShaders(vertex_filename="shaders/shadowvolumealgo.vertexshader",\
                              fragment_filename="shaders/shadowvolumealgo.fragmentshader")
        for i in range(len(self._objects)):
            self.C_positions[i] = (Vector * len(self._objects[i].getVertices()))
            j = 0
            self.C_positions[i] = self.C_positions[i]()
            for pos in self.C_positions[i]:
                pos.x = self._objects[i].getVertices()[j][0]
                pos.y = self._objects[i].getVertices()[j][1]
                pos.z = self._objects[i].getVertices()[j][2]
                j += 1

            self.C_indices[i] = c_int * len(self._objects[i].getIndices())
            k = 0
            self.C_indices[i] = self.C_indices[i]()
            for index in self.C_indices[i]:
                self.C_indices[i][k] = self._objects[i].getIndices()[k]
                k += 1

            self.C_normals[i] = Vector * len(self._objects[i].getNormals())
            l = 0
            self.C_normals[i] = self.C_normals[i]()
            for normal in self.C_normals[i]:
                normal.x = self._objects[i].getNormals()[l][0]
                normal.y = self._objects[i].getNormals()[l][1]
                normal.z = self._objects[i].getNormals()[l][2]
                l += 1

            self.C_size_indices[i] = c_int(len(self._objects[i].getIndices()))

            len_edges = len(self._objects[i].getVertices()) * 3
            self.C_contour_edges[i] = Edge * len_edges
            self.C_contour_edges[i] = self.C_contour_edges[i]()

            self.C_nb_edges[i] = pointer(c_int(0))

            self._volumePrograms[i] = gloo.Program(vertex_str, fragment_str)
            self._volumePrograms[i]['u_projection'] = self._projection
            # ortho(-5, +5, -5, +5, 10, 50)
            self._volumePrograms[i]['u_bias_matrix'] = ShadowMapAlgorithm.BIAS_MATRIX
        self.createVolumes()

        self.active = True
            

    # http://nuclear.mutantstargoat.com/articles/volume_shadows_tutorial_nuclear.pdf
    def createVolumes(self):
        # for each object
        lightPosition = range(len(self._objects))
        for i in range(len(self._objects)):
            model = numpy.eye(4, dtype=numpy.float32)
            translate(model, *self._objects[i].getPosition())
            light = numpy.dot(self._lights[0].getPosition() + [0], numpy.linalg.inv(model))
            lightPosition[i] = Vector(x=light[0],y=light[1],z=light[2])

            libvolume.findContourEdges(self.C_positions[i], self.C_indices[i], self.C_normals[i], self.C_size_indices[i],lightPosition[i], self.C_contour_edges[i], self.C_nb_edges[i])
            retEdges = []
            size = self.C_nb_edges[i].contents.value
            for j in range(size):
                edge = self.C_contour_edges[i][j]
                retEdges.append([numpy.array([vec.x, vec.y, vec.z]) for vec in [edge.one, edge.two]])
            self.createShadowTriangles(retEdges, i)
        self._lights[0].setModified(False)

    def createShadowTriangles(self, contour_edges, index):
        model = numpy.eye(4, dtype=numpy.float32)
        translate(model, *self._objects[index].getPosition())
        lightPosition = numpy.array(numpy.dot(self._lights[0].getPosition() + [0], numpy.linalg.inv(model)).tolist()[:-1])
        extrudeMagnitude = 100
        vertices = []
        for edge in contour_edges:
            a = edge[0]
            b = edge[1]
            c = numpy.add(edge[1], extrudeMagnitude * numpy.subtract(edge[1], lightPosition))
            d = numpy.add(edge[0], extrudeMagnitude * numpy.subtract(edge[0], lightPosition))
            vertices.extend([a,b,c,d])
        self._volumePrograms[index]['position'] = gloo.VertexBuffer(vertices)

    def drawVolumes(self):
        # gloo.clear(color=True, depth=True, stencil=True)
        gloo.set_state(None, stencil_test=True, cull_face=True)
        gloo.set_stencil_func('always', 0, ~0)
        # step 3 : draw front faces, depth test and stencil buffer increment
        gloo.set_stencil_op('keep', 'keep', 'decr')
        gloo.set_cull_face('front')
        for i in range(len(self._objects)):
            prog = self._volumePrograms[i]
            obj = self._objects[i]
            model = numpy.eye(4, dtype=numpy.float32)
            translate(model, *obj.getPosition())
            prog['u_model'] = model
            prog['u_view'] = self._createViewMatrix()
            prog.draw('triangles')
        # step 4 : draw back faces, depth test and stencil buffer decrement
        gloo.set_stencil_op('keep', 'keep', 'incr')
        gloo.set_cull_face('back')
        for i in range(len(self._objects)):
            prog = self._volumePrograms[i]
            obj = self._objects[i]
            model = numpy.eye(4, dtype=numpy.float32)
            translate(model, *obj.getPosition())
            prog['u_model'] = model
            prog['u_view'] = self._createViewMatrix()
            prog.draw('triangles')

    def update(self):
        if self.active:
            if self._lights[0].wasModified():
                self.createVolumes()
            GL.glPushAttrib(GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT);
            for prog in self._programs:
                prog['u_light_color'] = [0,0,0]
            self.draw()
            for prog in self._programs:
                prog['u_light_color'] = self._lights[0].getColor()
            #create shadow volumes
            # with self._frame_buffer:
            GL.glPushAttrib(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_POLYGON_BIT | GL.GL_STENCIL_BUFFER_BIT);
            GL.glColorMask(0, 0, 0, 0); # do not write to the color buffer
            GL.glDepthMask(0); # do not write to the depth (Z) buffer
            self.drawVolumes()
            GL.glPopAttrib()
            gloo.set_depth_func('equal')
            gloo.set_state(None, stencil_test=True)
            gloo.set_stencil_func('equal', 0, ~0)
            gloo.set_stencil_op('keep','keep','keep')
            self.draw()
            GL.glPopAttrib()


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
    obj = SceneObject(cube_positions, cube_indices, cube_normals, [0,0,0])
    obj2 = SceneObject(cube_positions, cube_indices, cube_normals, [0,0,0])
    camera = Camera()
    camera._position = [2,2,-2]
    light = Light()
    light._position = [2,2,-2]
    shadowvolumealgo = ShadowVolumeAlgorithm()
    shadowvolumealgo.init([obj, obj2], camera, [light])
    shadowvolumealgo.update()
    while True:
        shadowvolumealgo.update()
    # print shadowvolumealgo.findContourEdges(0)
