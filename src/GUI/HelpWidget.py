#!/usr/bin/python2
# -*- coding: utf8 -*-


from PyQt4 import QtGui, QtCore


class HelpWidget(QtGui.QWidget):
    """ """
    
    def __init__(self):
        """ """
        super(HelpWidget, self).__init__()

        self.initUI()
        
    def initUI(self):
        """ """
        hbox = QtGui.QHBoxLayout(self)

        self.textWidget = QtGui.QLabel(self)
        self.textWidget.setText(self._getStringHelp())

        hbox.addWidget(self.textWidget)
        self.setLayout(hbox)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.show()

    def _getStringHelp(self):
        """ """
        s= ""
        s += "Bonjour!\n\n"
        s += "Ceci est l'aide \n\n\n" 
        s += "Sur votre gauche vous trouverez ... \n\n\n "
        s += "Mais oui c'est clair ! \n\n\n\n\n "
        s += "Selectionne quelque chose dans la tree view a gauche"
        return s
