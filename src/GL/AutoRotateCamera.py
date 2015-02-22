#!/usr/bin/python2
# -*- coding: utf8 -*-


import time
import threading


class AutoRotateCamera(object):
    """ This class rotate the view constantly
    It manage race condition"""
    def __init__(self, camera, incrementation=0.5):
        self._camera = camera
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
        self._camera.setThetaAngle()
        while alive:
            self._camera.incrementeRotate(self._incrementation)
            time.sleep(0.04) # set by frame per second
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
        """ Stop the thread"""
        self.lock.acquire()
        self._alive = False
        self.lock.release()

    def getAlive(self):
        """ get the state of the thread """
        self.lock.acquire()
        alive = self._alive
        self.lock.release()
        return alive
