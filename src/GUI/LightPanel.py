#!/usr/bin/python2
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 

from GLShadow.Light import Light, LIGHT_POSSIBILITY, COLOR_POSSIBILITY


class AddLightPanel(QtGui.QWidget):

    def __init__(self, controller):
        QtGui.QWidget.__init__(self)
        self._controller = controller
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
        self._choiceColor = COLOR_POSSIBILITY[0]
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
        sliderI.setSliderPosition(85)
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
        sliderX.setSliderPosition(90)
        self.layout.addWidget(sliderX)
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Z".decode("utf8"))
        self.layout.addWidget(textWidget)
        sliderZ = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderZ.valueChanged.connect(self.lightPositionPercentZ)
        sliderZ.setSliderPosition(70)
        self.layout.addWidget(sliderZ)
        textWidget = QtGui.QLabel(self)
        textWidget.setText("Hauteur".decode("utf8"))
        self.layout.addWidget(textWidget)
        sliderY = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderY.valueChanged.connect(self.lightPositionPercentY)
        sliderY.setSliderPosition(90)
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
        newLight = Light()

        intensity = float(self._lightIntensity) / 100
        color = [1,1,1]
        colorRed = [1,0,0]
        colorYellow = [1,1,0]
        colorBlue = [0,0,1]
        if self._choiceColor == "Rouge":
            color = colorRed
        if self._choiceColor == "Jaune":
            color = colorYellow
        if self._choiceColor == "Bleu":
            color = colorBlue

        color[0] = color[0] * intensity
        color[1] = color[1] * intensity
        color[2] = color[2] * intensity
        
        newLight.setType(str(self._choiceType))

        newLight.setColor(color)
        newLight.setLightsRatio(self._lightPosition)

        newLight.setVerticalAngle(int(self._lightDirection[1]*1.8))
        newLight.setHorizontalAngle(int(self._lightDirection[0]*3.6))

        # direction

        self._controller.addLight(newLight)

        self.hide()





class RemoveLightPanel(QtGui.QWidget):

    def __init__(self, controller):
        QtGui.QWidget.__init__(self)
        self._controller = controller
        self.initGui()

    def initGui(self):
        """ """
        self.resize(300,150)
        self.layout = QtGui.QVBoxLayout(self)
        self.setWindowTitle("Supprimer une lampe")

        lightCollection = self._controller.getLightCollection()
        if len(lightCollection) > 0:
            choiceLabel = QtGui.QLabel("Choississez un type de lampe :", self)
            self.layout.addWidget(choiceLabel)
            lightCollection = self._controller.getLightCollection()
            self._choiceType = "0 Default"
            combo = QtGui.QComboBox(self)
            for lightIndex in range(len(lightCollection)):
                string = str(lightIndex) + " " + lightCollection[lightIndex].getType()
                string += " "
                if lightCollection[lightIndex].getColor()[1] == 0 and lightCollection[lightIndex].getColor()[2] == 0:
                    string += "Rouge"
                elif lightCollection[lightIndex].getColor()[2] == 0 :
                    string += "Jaune"
                elif lightCollection[lightIndex].getColor()[0] == 0 and lightCollection[lightIndex].getColor()[1] == 0:
                    string += "Bleu"
                else :
                    string += "Blanc"
                string += " "
                string += "X=" + str(lightCollection[lightIndex].getPosition()[0])
                string += " "
                string += "Z=" + str(lightCollection[lightIndex].getPosition()[1])
                string += " "
                string += "Hauteur=" + str(lightCollection[lightIndex].getPosition()[2])
                
                combo.addItem(string)
            combo.activated[str].connect(self.onTypeSelection)
            self.layout.addWidget(combo)

            btn = QtGui.QPushButton("Supprimer", self)
            btn.clicked.connect(self.buttonClicked)
            self.layout.addWidget(btn) 

            self.show() 
        else:
            QtGui.QMessageBox.information(self, "Erreur", "Aucune lampe")   

    def onTypeSelection(self, text):
        self._choiceType = text

    def buttonClicked(self):
        """ """
        index = str(self._choiceType).split()[0]
        index = int(index)
        self._controller.deleteLight(index)

        self.hide()