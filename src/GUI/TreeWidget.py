#!/usr/bin/python2
# -*- coding: utf8 -*-



import sys
from PyQt4 import QtCore, QtGui


class TreeWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.addItems(self.treeWidget.invisibleRootItem())
        self.treeWidget.itemChanged.connect (self.handleChanged)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)

    def addItems(self, parent):
        column = 0
        scene1 = self.addParent(parent, column, "Scene numero un", "description")
        scene2 = self.addParent(parent, column, "Scene numero deux", "description")

        item1 = self.addChild(scene1, column, "Algo A", "description Algo A")
        item1.setCheckState(column, QtCore.Qt.Checked)
        self.addChild(scene1, column, "Algo B", "description Algo B")

        self.addChild(scene2, column, "Algo A", "description Algo A")
        self.addChild(scene2, column, "Algo B", "description Algo B")


    def addParent(self, parent, column, title, data):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        return item

    def addChild(self, parent, column, title, data):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setCheckState(column, QtCore.Qt.Unchecked)
        return item

    def unckeckEverythingExceptItem(self,itemExcluded):
        """ """
        root = self.treeWidget.invisibleRootItem()
        childCountRoot = root.childCount()
        for firstLevelchild in range(childCountRoot):
            firstChild = root.child(firstLevelchild)
            childCountFirst = firstChild.childCount()
            for SecondLevelchild in range(childCountFirst):
                secondChild = firstChild.child(SecondLevelchild)
                if secondChild!= itemExcluded:
                    secondChild.setCheckState(0, QtCore.Qt.Unchecked)


    def handleChanged(self, item, column):
        if item.checkState(column) == QtCore.Qt.Checked:
            self.unckeckEverythingExceptItem(item)
            #print "checked", item, item.text(column)
        #if item.checkState(column) == QtCore.Qt.Unchecked:
            #item.setCheckState(0, QtCore.Qt.Checked)
            #print "unchecked", item, item.text(column)
