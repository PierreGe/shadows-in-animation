#!/usr/bin/python2
# -*- coding: utf8 -*-


import threading
import psutil
import os


class PerformanceIndication(object):
    """ This class rotate the view constantly
    It manage race condition"""
    def __init__(self):
        # receiver of signal to update
        self._thread = None
        self._alive = False
        self._cpu = "None"
        self._p = psutil.Process(os.getpid())
        self.lock = threading.Lock()
        self.start()

    def getCpuPercent(self):
        return self._cpu

    def getMemoryPercent(self):
        return str(round(self._p.memory_percent(),1))


    def _worker(self):
        """ The thread's worker """
        self.lock.acquire()
        alive = self._alive
        self.lock.release()
        while alive:
            print("lol")
            cpu = str(round(self._p.cpu_percent(interval=1),1))
            self.lock.acquire()
            self._cpu = cpu
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
