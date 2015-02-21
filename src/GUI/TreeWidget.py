#!/usr/bin/python2
# -*- coding: utf8 -*-



import sys
from PyQt4 import QtCore, QtGui


class TreeWidget(QtGui.QWidget):
    """ """
    def __init__(self,selectController):
        """ """
        QtGui.QWidget.__init__(self)
        self._controller = selectController
        self._treeWidget = QtGui.QTreeWidget()
        self._treeWidget.setHeaderHidden(True)
        self._treeWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self._addItems(self._treeWidget.invisibleRootItem())
        self._treeWidget.itemChanged.connect (self.handleChanged)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._treeWidget)
        self.setLayout(layout)

    def _addItems(self, parent):
        """ """
        column = 0
        sceneDictionnary = self._controller.getAllScene()
        iterable = sceneDictionnary.keys()
        iterable.sort()
        for scene in iterable:
            name = sceneDictionnary[scene]["name"]
            description = sceneDictionnary[scene]["description"]
            algosCompatible = sceneDictionnary[scene]["algo-compatible"]
            scene1 = self._addScene(parent, column, name, description)
            for algo in algosCompatible:
                self._addAlgorithm(scene1, column, algo, "description ")
        
        # TODO : associer les algo

    def _addScene(self, parent, column, title, data):
        """ """
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        return item

    def _addAlgorithm(self, parent, column, title, data):
        """ """
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setCheckState(column, QtCore.Qt.Unchecked)
        return item

    def _unckeckEverythingExceptItem(self,itemExcluded):
        """ """
        root = self._treeWidget.invisibleRootItem()
        childCountRoot = root.childCount()
        for firstLevelchild in range(childCountRoot):
            firstChild = root.child(firstLevelchild)
            childCountFirst = firstChild.childCount()
            for SecondLevelchild in range(childCountFirst):
                secondChild = firstChild.child(SecondLevelchild)
                if secondChild!= itemExcluded:
                    secondChild.setCheckState(0, QtCore.Qt.Unchecked)


    def handleChanged(self, item, column):
        """ This method is trigered when something is selectionned in the treeview """
        if item.checkState(column) == QtCore.Qt.Checked:
            self._unckeckEverythingExceptItem(item)
            self._controller.showGL(item)
        if item.checkState(column) == QtCore.Qt.Unchecked:
            self._controller.showHelp()
            #print "unchecked", item, item.text(column)
