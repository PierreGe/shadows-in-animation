from vispy import gloo
from vispy.util.transforms import *

from Utils import *

class RayTracingAlgorithm(app.Canvas):
    def __init__(self):

        self.program = gloo.Program("shaders/raytracingalgo.vertexshader", "shaders/raytracingalgo.fragmentshader")

    def init(self, positions, indices, normals, camera, light):
        """ """

        self.program['a_position'] = [(-1., -1.), (-1., +1.),(+1., -1.), (+1., +1.)]
        self.program['sphere_position_0'] = (.75, .1, 1.)
        self.program['sphere_radius_0'] = .6
        self.program['sphere_color_0'] = (0., 0., 1.)
        self.program['sphere_position_1'] = (-.75, .1, 2.25)
        self.program['sphere_radius_1'] = .6
        self.program['sphere_color_1'] = (.5, .223, .5)
        self.program['plane_position'] = (0., -.5, 0.)
        self.program['plane_normal'] = (0., 1., 0.)
        self.program['light_intensity'] = 1.
        self.program['light_specular'] = (1., 50.)
        self.program['light_position'] = (5., 5., -10.)
        self.program['light_color'] = (1., 1., 1.)
        self.program['ambient'] = .05
        self.program['O'] = (0., 0., -1.)

        self.program.draw('triangle_strip')

        self.active = True


    def on_timer(self, event):
        t = event.elapsed
        self.program['sphere_position_0'] = (+.75, .1, 2.0 + 1.0 * cos(4*t))
        self.program['sphere_position_1'] = (-.75, .1, 2.0 - 1.0 * cos(4*t))
        self.update()

    def on_resize(self, event):
        width, height = event.size
        gloo.set_viewport(0, 0, width, height)
        self.program['u_aspect_ratio'] = width/float(height)

    def on_draw(self, event):
        self.program.draw('triangle_strip')

    def terminate(self):
        self.active = False