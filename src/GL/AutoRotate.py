#!/usr/bin/python2
# -*- coding: utf8 -*-


import time
import threading


class AutoRotate(object):
    """ This class rotate the view constantly
    It manage race condition"""
    def __init__(self, camera):
        self._camera = camera
        # receiver of signal to update
        self._thread = None
        self._alive = False
        self.lock = threading.Lock()


    def _worker(self):
        """ The thread's worker """
        self.lock.acquire()
        alive = self._alive
        self.lock.release()
        while alive:
            self._camera.incrementeY(0.5)
            time.sleep(0.05)
            self.lock.acquire()
            alive = self._alive
            self.lock.release()
            #updateGL()


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
