#!/usr/bin/python2
# -*- coding: utf-8 -*-

from OpenGL import GL
from OpenGL.GLUT import *
from OpenGL.GLU import *

import os
import time
import subprocess

class GPUUsageHelper(object):
    """Check the hardware compatibility"""
    def __init__(self):
        # init GL
        pass

    def getOutput(self):
        """ """
        p = subprocess.Popen("top", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        #time.sleep(1)
        (output, err) = p.communicate()
        os.killpg(p.pid, signal.SIGTERM) 
        print(output)

if __name__ == '__main__':
    g = GPUUsageHelper()
    g.getOutput()

        