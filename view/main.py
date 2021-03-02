from PyQt5 import QtCore, QtGui, QtWidgets, uic
from view.viewann import viewAnn
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class main(QtWidgets.QWidget, QtCore.QAbstractTableModel):

    saveVerifysSignal = QtCore.pyqtSignal()
    openVerifysSignal = QtCore.pyqtSignal()
    newProjectVerifysSignal = QtCore.pyqtSignal()

    def play(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 720)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Layout untuk semua tab utama (metode) : Artificial Nerural Network, Thomas Fiering, Comparation
        self.mainTabLayout = QtWidgets.QTabWidget(self.centralwidget)
        self.mainTabLayout.setObjectName("mainTabLayout")
        self.gridLayout.addWidget(self.mainTabLayout, 1, 0, 1, 1)


        # '''-----------------------------------------------------------------------------------------------
        # Menu Bar
        # -----------------------------------------------------------------------------------------------'''

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 957, 18))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.triggered.connect(self.newProjectVerifysSignal)

        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")

        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        
        #================================

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStatusTip('Open Model')
        self.actionOpen.triggered.connect(self.openVerifysSignal)
        
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setDisabled(True)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setStatusTip('Save Model')
        self.actionSave.triggered.connect(self.saveVerifysSignal)

        #=================================

        #self.actionPrint_Graphic = QtWidgets.QAction(MainWindow)
        #self.actionPrint_Graphic.setObjectName("actionPrint_Graphic")

        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        #self.menuFile.addAction(self.actionPrint_Graphic)

        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # ------------------------------------------

        self.retranslateUi(MainWindow)
        self.mainTabLayout.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def saveModel(self, model):
        filename = QtGui.QFileDialog.getSaveFileName(
            self, 'Save Model', '', "Keras Model (*.h5)")
        #name, extension = QtGui.QFileDialog.getSaveFileNameAndFilter(
            #self, 'Save file', 'Keras Model', filter=self.tr("*.h5"))
        print(type(filename))
        print(filename[0])
        model.save(filename[0])

    def openModel(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Model', '', "Keras Model (*.h5)")
        print(filename[0])
        return(filename[0])


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Rainfall Prediction", "Rainfall Prediction"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "New Project"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open Model"))
        self.actionSave.setText(_translate("MainWindow", "Save Model"))
        #self.actionPrint_Graphic.setText(_translate("MainWindow", "Print"))
        #self.declareInit()

