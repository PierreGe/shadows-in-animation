#!/usr/bin/python2
# -*- coding: utf8 -*-

from PyQt4 import QtCore, QtGui
from vispy import gloo
from vispy.util.transforms import *
from vispy import app
import math

class RayTracingWidget(QtGui.QWidget):
    """ The QT widget of ray tracing"""
    def __init__(self):
        QtGui.QWidget.__init__(self, None)
        self.setMinimumSize(600, 400)
        self.canvas = Canvas(parent=self)
        hlayout = QtGui.QHBoxLayout(self)
        self.setLayout(hlayout)
        hlayout.addWidget(self.canvas.native, 1)

    def killThreads(self):
        """ In case of thread"""
        pass # do NOT delete method

class Canvas(app.Canvas):
    def __init__(self, **kwargs):
        app.Canvas.__init__(self, **kwargs)
        self.geometry = 0, 0, 400, 400

        self.program = gloo.Program("shaders/raytracingalgo.vertexshader", "shaders/raytracingalgo.fragmentshader")

        self.program['a_position'] = [(-1., -1.), (-1., +1.),(+1., -1.), (+1., +1.)]
        self.program['sphere_position_0'] = (.75, .1, 1.)
        self.program['sphere_radius_0'] = .6
        self.program['sphere_color_0'] = (1., 1., 1.)
        self.program['sphere_position_1'] = (-.75, .1, 2.25)
        self.program['sphere_radius_1'] = .6
        self.program['sphere_color_1'] = (1., 1., 1.)
        self.program['plane_position'] = (0., -.5, 0.)
        self.program['plane_normal'] = (0., 1., 0.)
        self.program['light_intensity'] = 1.
        self.program['light_specular'] = (1., 50.)
        self.program['light_position'] = (5., 5., -10.)
        self.program['light_color'] = (1., 1., 1.)
        self.program['ambient'] = .05
        self.program['O'] = (0., 0., -1.)

        gloo.set_clear_color((1, 1, 1, 1))
        gloo.set_state(depth_test=True)

        #self.program.draw('triangle_strip')

        #self.active = True
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)


    def on_timer(self, event):
        t = event.elapsed
        angle = t%360
        self.program['sphere_position_0'] = (+ math.sin(t), .1, 2.0 + 1.0 * math.cos(t))
        self.program['sphere_position_1'] = (- math.sin(t), .1, 2.0 - 1.0 * math.cos(t))
        self.update()

    def on_resize(self, event):
        width, height = event.size
        gloo.set_viewport(0, 0, width, height)
        self.program['u_aspect_ratio'] = width/float(height)

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('triangle_strip')

    def terminate(self):
        self.active = False

if __name__ == '__main__':
    app.create()
    m = RayTracingWidget()
    m.show()
    app.run()