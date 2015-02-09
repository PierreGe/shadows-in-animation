#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 

LIGHT_POSSIBILITY = ["Point", "Directionnel", "Spot", "Ligne", "Rond"]
LIGHT_WITH_DIRECTION = ["Directionnel","Ligne","Spot"]

COLOR_POSSIBILITY = ["Blanc", "Rouge", "Jaune", "Bleu"]


class LightPanel(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initGui()

    def initGui(self):
        """ """
        self.resize(640,480)
        self.layout = QtGui.QVBoxLayout(self)
        self.setWindowTitle("Ajouter une lampe")

        choiceLabel = QtGui.QLabel("Choississez un type de lampe :", self)
        self.layout.addWidget(choiceLabel)
        self._choiceType = LIGHT_POSSIBILITY[0]
        combo = QtGui.QComboBox(self)
        for possibility in LIGHT_POSSIBILITY:
            combo.addItem(possibility)
        combo.activated[str].connect(self.onTypeSelection)
        self.layout.addWidget(combo)


        choiceLabel = QtGui.QLabel("Choississez une couleur de lampe :", self)
        self.layout.addWidget(choiceLabel)
        self._choiceType = COLOR_POSSIBILITY[0]
        combo = QtGui.QComboBox(self)
        for possibility in COLOR_POSSIBILITY:
            combo.addItem(possibility)
        combo.activated[str].connect(self.onColorSelection)
        self.layout.addWidget(combo)

        textWidget = QtGui.QLabel(self)
        textWidget.setText("\n".decode("utf8"))
        self.layout.addWidget(textWidget)

        self._lightIntensity = 0
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Intensité de la lumière".decode("utf8"))
        self.layout.addWidget(textWidget)
        sliderI = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderI.valueChanged.connect(self.lightIntensityPercent)
        sliderI.setSliderPosition(75)
        self.layout.addWidget(sliderI)


        textWidget = QtGui.QLabel(self)
        textWidget.setText("\n".decode("utf8"))
        self.layout.addWidget(textWidget)


        self._lightPosition = [0,0,0]
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Position lumière".decode("utf8"))
        self.layout.addWidget(textWidget)
        textWidget = QtGui.QLabel(self)
        textWidget.setText("X".decode("utf8"))
        self.layout.addWidget(textWidget)
        sliderX = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderX.valueChanged.connect(self.lightPositionPercentX)
        sliderX.setSliderPosition(99)
        self.layout.addWidget(sliderX)
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Z".decode("utf8"))
        self.layout.addWidget(textWidget)
        sliderZ = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderZ.valueChanged.connect(self.lightPositionPercentZ)
        sliderZ.setSliderPosition(99)
        self.layout.addWidget(sliderZ)
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Hauteur".decode("utf8"))
        self.layout.addWidget(textWidget)
        sliderY = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderY.valueChanged.connect(self.lightPositionPercentY)
        sliderY.setSliderPosition(99)
        self.layout.addWidget(sliderY)


        textWidget = QtGui.QLabel(self)
        textWidget.setText("\n".decode("utf8"))
        self.layout.addWidget(textWidget)

        self._lightDirection = [0,0]
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Direction lumière".decode("utf8"))
        self.layout.addWidget(textWidget)
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Angle Horizontal".decode("utf8"))
        self.layout.addWidget(textWidget)
        sliderX = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderX.valueChanged.connect(self.lightPositionPercentX)
        sliderX.setSliderPosition(99)

        self.layout.addWidget(sliderX)
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Angle Vertical".decode("utf8"))
        self.layout.addWidget(textWidget)
        sliderZ = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderZ.valueChanged.connect(self.lightPositionPercentZ)
        sliderZ.setSliderPosition(99)
        self.layout.addWidget(sliderZ)

        textWidget = QtGui.QLabel(self)
        textWidget.setText("\n".decode("utf8"))
        self.layout.addWidget(textWidget)

        btn = QtGui.QPushButton("Ajouter!", self)
        btn.clicked.connect(self.buttonClicked)
        self.layout.addWidget(btn) 

        self.show()    

    def onTypeSelection(self, text):
        self._choiceType = text

    def onColorSelection(self, text):
        self._choiceColor = text

    def lightIntensityPercent(self,i):
        """ """
        self._lightIntensity = i

    def lightPositionPercentX(self,x):
        """ """
        self._lightPosition[0] = x

    def lightPositionPercentY(self,y):
        """ """
        self._lightPosition[1] = y

    def lightPositionPercentZ(self,z):
        """ """
        self._lightPosition[2] = z

    def lightDirectionPercentHorizontalAngle(self,x):
        """ """
        self._lightDirection[0] = x

    def lightDirectionPercentVerticalAngle(self,y):
        """ """
        self._lightDirection[1] = y


    def buttonClicked(self):
        """ """
        print("Clicked!")


if __name__ == "__main__":
    app = QtGui.QApplication([])
    w = LightPanel()
    w.show()
    #w.raise_()
    app.exec_()