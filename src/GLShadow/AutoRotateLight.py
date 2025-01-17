#!/usr/bin/python2
# -*- coding: utf8 -*-


import time
import threading


class AutoRotateLight(object):
    """ This class rotate the view constantly
    It manage race condition"""
    def __init__(self, light, incrementation=0.5):
        self._light = light
        # receiver of signal to update
        self._thread = None
        self._alive = False
        self._incrementation = incrementation
        self.lock = threading.Lock()


    def _worker(self):
        """ The thread's worker """
        self.lock.acquire()
        alive = self._alive
        self.lock.release()
        self._light.setThetaAngle()
        while alive:
            self._light.incrementeRotate(self._incrementation)
            time.sleep(0.03) # set by frame per second
            self.lock.acquire()
            alive = self._alive
            self.lock.release()


    def start(self):
        """ start the rotation"""
        self.lock.acquire()
        self._alive = True
        self.lock.release()
        self._thread = threading.Thread(target=self._worker)
        self._thread.start()


    def stop(self):
        """ """
        self.lock.acquire()
        self._alive = False
        self.lock.release()

    def getAlive(self):
        """ """
        self.lock.acquire()
        alive = self._alive
        self.lock.release()
        return alive
