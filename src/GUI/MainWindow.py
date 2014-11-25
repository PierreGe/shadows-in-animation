#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
from PyQt4 import QtGui, QtCore

import SplitPane

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self): 
        """ This methode will  """             
        # Windows title
        self.setWindowTitle("Les ombres au sein des jeux et des animations")



        textEdit1 = QtGui.QTextEdit()
        textEdit2 = QtGui.QTextEdit()
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(textEdit1)
        splitter.addWidget(textEdit1)
        ex = SplitPane.SplitPane()
        self.setCentralWidget(ex)

        # si on veut mettre une bar en bas qui dit par exemple "Computing ..."
        statusBar = self.statusBar()

        self.initToolsBar()
        self.initMenu()
   
        self.showMaximized()

    def initToolsBar(self):
        """ """
        exitAction = QtGui.QAction(QtGui.QIcon('images/application-exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)


        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(exitAction)

    def initMenu(self):
        """ """
        exitAction = QtGui.QAction(QtGui.QIcon('images/application-exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        
def main():  
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()