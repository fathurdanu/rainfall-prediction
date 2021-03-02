from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QShortcut, QGroupBox, QRadioButton
import pyqtgraph as pg
import sys, csv, io
import datetime
from pyqtgraph import AxisItem
from datetime import datetime, timedelta
from time import mktime
import numpy

activationList = ['None', 'sigmoid', 'tanh', 'relu', 'selu', 'elu', 'softmax', 'softplus', 'softsign']
optimizerList = ['adam', 'adadelta', 'adagrad', 'nadam', 'SGD']

class viewAnn(QtWidgets.QWidget, QtCore.QAbstractTableModel):
    browseANNverifySignal = QtCore.pyqtSignal()
    resetANNverifySignal = QtCore.pyqtSignal()
    hidLayerSpinBoxANNvalueVerifySignal = QtCore.pyqtSignal()
    processANNVerifySignal = QtCore.pyqtSignal()
    comboboxChooseTargetVerifySignal = QtCore.pyqtSignal()
    predictingANNVerifySignal = QtCore.pyqtSignal()
    radioVerifySignal = QtCore.pyqtSignal()
    #printModelVerifySignal = QtCore.pyqtSignal()

    def setupUi(self, MainWindow, centralwidget, mainTabLayout):
        super(viewAnn, self).__init__()

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        #self.printModel = QShortcut(QtGui.QKeySequence('Ctrl+P'), self)
        #self.printModel.activated.connect(self.printModelVerifySignal)

        # Artificial Neural Network Tab
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        # vericalLayout membagi dua bagian tempat kerja dan footer
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # gridLayout yang membagi dua bagian, sisi kiri (tabel dataset) dan sisi kanan (sub tab ANN)
        self.gridLayout_devide2side_ANNtab = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.gridLayout_devide2side_ANNtab.setObjectName("gridLayout_devide2side_ANNtab")

        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.groupBox_DailyMonthly = QGroupBox("Forecast Daily or Monthly?")
        #self.groupBox_DailyMonthly.setFont(font)
        self.radioButton_daily = QRadioButton("Daily")
        self.radioButton_monthly = QRadioButton("Monthly")
        self.radioButton_daily.clicked.connect(self.radioVerifySignal)
        self.radioButton_monthly.clicked.connect(self.radioVerifySignal)
        #self.groupBox_DailyMonthly..connect(self.radioVerifySignal)

        self.hboxLayout = QtWidgets.QHBoxLayout()
        self.hboxLayout.addWidget(self.radioButton_daily)
        self.hboxLayout.addWidget(self.radioButton_monthly)
        self.hboxLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_DailyMonthly.setLayout(self.hboxLayout)


        # tombol browse ANN
        self.browseANNButton = QtWidgets.QPushButton(self.tab)
        self.browseANNButton.setObjectName("browseANNButton")
        self.browseANNButton.clicked.connect(self.browseANNverifySignal)

        # tombol reset ANN
        self.resetANNButton = QtWidgets.QPushButton(self.tab)
        self.resetANNButton.setObjectName("resetANNButton")
        self.resetANNButton.clicked.connect(self.resetANNverifySignal)

        self.verLayout_leftSide_ANNtab = QtWidgets.QVBoxLayout()
        self.verLayout_leftSide_ANNtab.setObjectName("verLayout_leftSide_ANNtab")
        self.verLayout_leftSide_ANNtab.addWidget(self.browseANNButton)
        self.verLayout_leftSide_ANNtab.addWidget(self.resetANNButton)

        # horizontalLayout yang berisikan tombol browse dan reset ANN
        self.horizLayout_leftSide_ANNtab = QtWidgets.QHBoxLayout()
        self.horizLayout_leftSide_ANNtab.setObjectName("horizLayout_leftSide_ANNtab")
        self.horizLayout_leftSide_ANNtab.addWidget(self.groupBox_DailyMonthly)
        self.horizLayout_leftSide_ANNtab.addLayout(self.verLayout_leftSide_ANNtab)

        # tabel ANN Dataset
        self.tableANNDataset = QtWidgets.QTableWidget(self.tab)
        self.tableANNDataset.setObjectName("tableANNDataset")
        self.tableANNDataset.setRowCount(100)
        self.tableANNDataset.setColumnCount(100)
        self.tableANNDataset.horizontalHeader()
        self.tableANNDataset.installEventFilter(self)

        # label Choose Target
        self.labelChooseTarget = QtWidgets.QLabel()
        self.labelChooseTarget.setFont(font)
        self.labelChooseTarget.setObjectName("labelChooseTarget")

        # combobox Choose Target
        self.comboboxChooseTarget = QtWidgets.QComboBox()
        self.comboboxChooseTarget.setObjectName("actInputLayerBox")
        self.comboboxChooseTarget.addItem("None")
        self.comboboxChooseTarget.currentTextChanged.connect(self.comboboxChooseTargetVerifySignal)

        # horizontal Layout Choose Target berisikan label dan combobox choose target
        self.horizLayoutChooseTarget_leftSide_ANNtab = QtWidgets.QHBoxLayout()
        self.horizLayoutChooseTarget_leftSide_ANNtab.setObjectName("horizLayoutChooseTarget_leftSide_ANNtab")
        self.horizLayoutChooseTarget_leftSide_ANNtab.addWidget(self.labelChooseTarget)
        self.horizLayoutChooseTarget_leftSide_ANNtab.addWidget(self.comboboxChooseTarget)

        # vertical Layout sisi kiri pada tab ANN
        self.verticalLayout_leftSide_ANNtab = QtWidgets.QVBoxLayout()
        self.verticalLayout_leftSide_ANNtab.setObjectName("verticalLayout_leftSide_ANNtab")
        #self.verticalLayout_leftSide_ANNtab.addWidget(self.groupBox_DailyMonthly)
        self.verticalLayout_leftSide_ANNtab.addLayout(self.horizLayout_leftSide_ANNtab)
        self.verticalLayout_leftSide_ANNtab.addWidget(self.tableANNDataset)
        self.verticalLayout_leftSide_ANNtab.addLayout(self.horizLayoutChooseTarget_leftSide_ANNtab)

        #dipake buat syarat QtSplitter (resize window)
        self.rightWidget_forSplitter = QtWidgets.QWidget()
        #self.rightWidget_forSplitter.objectName("rightWidget_forSplitter")
        self.rightWidget_forSplitter.setLayout(self.verticalLayout_leftSide_ANNtab)

        # tab widget sisi kanan pada tab ANN
        self.tabWidget_rightSide_ANNtab = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_rightSide_ANNtab.setObjectName("tabWidget_rightSide_ANNtab")
        self.gridLayout_devide2side_ANNtab.addWidget(self.rightWidget_forSplitter)

        '''----------------------------------ANN Configuration Tab--------------------------------------------'''

        # tab konfigurasi ANN
        self.ANNconfigurationTab = QtWidgets.QWidget()
        self.ANNconfigurationTab.setObjectName("ANNconfigurationTab")

        # text pada tab konfigurasi ANN : Graph
        self.labelGraph_ANNconfigurationTab = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelGraph_ANNconfigurationTab.setFont(font)
        self.labelGraph_ANNconfigurationTab.setObjectName("labelGraph_ANNconfigurationTab")
        #self.verticalLayout_ANNconfigurationTab.addWidget(self.labelGraph_ANNconfigurationTab)

        # graph ANN pada tab konfigurasi ANN
        self.graphANN = pg.PlotWidget(self.ANNconfigurationTab)
        self.graphANN.setObjectName("graphANN")
        self.graphANN.setBackground('w')
        self.graphANN.setLabel('left', '')
        self.graphANN.setLabel('bottom', 'Month')
        self.legendGraph_ANNconfigurationTab = self.graphANN.addLegend()
        #self.verticalLayout_ANNconfigurationTab.addWidget(self.graphANN)


        #contoh xy tahun error 1970
        #axis = DateAxisItem(orientation='bottom')
        #axis.attachToPlotItem(self.graphANN.getPlotItem())
        #now = time.time()
        #timestamps = numpy.linspace(now - 3600, now, 100)
        #self.graphANN.plot(x=timestamps, y=numpy.random.rand(100))

        # text pada tab konfigurasi ANN : Architecture
        self.labelArchitecture_ANNconfigurationTab = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelArchitecture_ANNconfigurationTab.setFont(font)
        self.labelArchitecture_ANNconfigurationTab.setObjectName("labelArchitecture_ANNconfigurationTab")
        #self.verticalLayout_ANNconfigurationTab.addWidget(self.labelArchitecture_ANNconfigurationTab)

        # grid Layout membagi layer dengan Neuron
        self.gridLayout_devideLayerAndNeuron = QtWidgets.QGridLayout()
        self.gridLayout_devideLayerAndNeuron.setObjectName("gridLayout_devideLayerAndNeuron")

        # vertical Layout Layer : hidden layer dan output layer
        self.verticalLayoutLayer = QtWidgets.QVBoxLayout()
        self.verticalLayoutLayer.setObjectName("verticalLayoutLayer")

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        # garis horizontal atas
        self.line_2 = QtWidgets.QFrame(self.ANNconfigurationTab)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayoutLayer.addWidget(self.line_2)

        # text pada tab konfigurasi ANN : Hidden Layer
        self.labelHidLayer_ANNconfigurationTab = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelHidLayer_ANNconfigurationTab.setFont(font)
        self.labelHidLayer_ANNconfigurationTab.setAlignment(QtCore.Qt.AlignCenter)
        self.labelHidLayer_ANNconfigurationTab.setObjectName("labelHidLayer_ANNconfigurationTab")
        self.verticalLayoutLayer.addWidget(self.labelHidLayer_ANNconfigurationTab)

        # form layout untuk memisahkan text dan spinbox hidden layer
        self.formLayout_devideTextAndSpinboxHiddenLayer = QtWidgets.QFormLayout()
        self.formLayout_devideTextAndSpinboxHiddenLayer.setObjectName("formLayout_devideTextAndSpinboxHiddenLayer")
        self.labelNumberOfHidLayer_ANNconfigurationTab = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelNumberOfHidLayer_ANNconfigurationTab.setObjectName("labelNumberOfHidLayer_ANNconfigurationTab")
        self.formLayout_devideTextAndSpinboxHiddenLayer.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                                                  self.labelNumberOfHidLayer_ANNconfigurationTab)

        # spin box hidden layer
        self.numOfHiddenLayer = QtWidgets.QSpinBox(self.ANNconfigurationTab)
        self.numOfHiddenLayer.setObjectName("numOfHiddenLayer")
        self.numOfHiddenLayer.valueChanged.connect(self.hidLayerSpinBoxANNvalueVerifySignal)
        self.formLayout_devideTextAndSpinboxHiddenLayer.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                                                                  self.numOfHiddenLayer)
        self.verticalLayoutLayer.addLayout(self.formLayout_devideTextAndSpinboxHiddenLayer)

        # garis horizontal tengah
        self.line_3 = QtWidgets.QFrame(self.ANNconfigurationTab)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setObjectName("line_3")
        self.verticalLayoutLayer.addWidget(self.line_3)

        # text pada tab konfigurasi ANN : Output Layer
        self.labelOutputLayer_ANNconfigurationTab = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelOutputLayer_ANNconfigurationTab.setFont(font)
        self.labelOutputLayer_ANNconfigurationTab.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOutputLayer_ANNconfigurationTab.setObjectName("labelOutputLayer_ANNconfigurationTab")
        self.verticalLayoutLayer.addWidget(self.labelOutputLayer_ANNconfigurationTab)

        # form layout untuk memisahkan text dan spinbox hidden layer
        self.formLayout_devideTextAndComboboxOutputLayer = QtWidgets.QFormLayout()
        self.formLayout_devideTextAndComboboxOutputLayer.setObjectName("formLayout_devideTextAndComboboxOutputLayer")

        # text pada tab konfigurasi ANN : Activation
        self.labelActivation_ANNconfigurationTab = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelActivation_ANNconfigurationTab.setObjectName("labelActivation_ANNconfigurationTab")
        self.formLayout_devideTextAndComboboxOutputLayer.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                                                   self.labelActivation_ANNconfigurationTab)

        # aktifasi output
        self.actOutputLayerBox = QtWidgets.QComboBox(self.ANNconfigurationTab)
        self.actOutputLayerBox.setObjectName("actOutputLayerBox")
        self.actOutputLayerBox.addItems(activationList)
        self.formLayout_devideTextAndComboboxOutputLayer.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                                                                   self.actOutputLayerBox)

        # sulit dijelaskan
        self.verticalLayoutLayer.addLayout(self.formLayout_devideTextAndComboboxOutputLayer)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutLayer.addItem(spacerItem)
        self.gridLayout_devideLayerAndNeuron.addLayout(self.verticalLayoutLayer, 0, 1, 1, 1)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)

        # garis vertikal diantara vertikalLayoutLayer dengan gridLayoutNeuron
        self.line = QtWidgets.QFrame(self.ANNconfigurationTab)
        self.line.setFont(font)
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.gridLayout_devideLayerAndNeuron.addWidget(self.line, 0, 2, 1, 1)

        # grid layout neuron : tabel hidden neuron
        self.gridLayoutNeuron = QtWidgets.QGridLayout()
        self.gridLayoutNeuron.setObjectName("gridLayoutNeuron")

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        # text pada tab konfigurasi ANN : kolom Layer
        self.labelLayerColumn_ANNconfigurationTab = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelLayerColumn_ANNconfigurationTab.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLayerColumn_ANNconfigurationTab.setObjectName("labelLayerColumn_ANNconfigurationTab")

        # text pada tab konfigurasi ANN : kolom Neuron
        self.label = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        # text pada tab konfigurasi ANN : kolom activation
        self.label_2 = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        # sulit dijelaskan
        self.gridLayout_devideLayerAndNeuron.addLayout(self.gridLayoutNeuron, 0, 3, 1, 1)
        #self.verticalLayout_ANNconfigurationTab.addLayout(self.gridLayout_devideLayerAndNeuron)


        # scroll area vertical
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 379, 207))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # tabel pada grid layout neuron
        self.gridLayoutTable_gridLayoutNeuron = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayoutTable_gridLayoutNeuron.setObjectName("gridLayoutTable_gridLayoutNeuron")
        self.gridLayoutTable_gridLayoutNeuron.addWidget(self.labelLayerColumn_ANNconfigurationTab, 0, 0, 1, 1)
        self.gridLayoutTable_gridLayoutNeuron.addWidget(self.label, 0, 1, 1, 1)
        self.gridLayoutTable_gridLayoutNeuron.addWidget(self.label_2, 0, 2, 1, 1)
        # self.gridLayoutNeuron.addLayout(self.gridLayoutTable_gridLayoutNeuron, 1, 0, 1, 1)

        # scrollArea
        self.scrollArea = QtWidgets.QScrollArea(centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_devideLayerAndNeuron.addWidget(self.scrollArea, 0, 4, 1, 1)

        self.spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayoutTable_gridLayoutNeuron.addItem(self.spacerItem1, 1, 1, 1, 1)

        # garis horizontal bawah
        self.line_4 = QtWidgets.QFrame(self.ANNconfigurationTab)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setObjectName("line_4")
        #self.verticalLayout_ANNconfigurationTab.addWidget(self.line_4)


        # grid Layout optimizer
        self.gridLayoutOptimizer = QtWidgets.QGridLayout()
        self.gridLayoutOptimizer.setObjectName("gridLayoutOptimizer")

        # text pada tab konfigurasi ANN : optimizer
        self.label_4 = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayoutOptimizer.addWidget(self.label_4, 0, 0, 1, 1)

        # text pada tab konfigurasi ANN : titik dua optimizer
        self.label_6 = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayoutOptimizer.addWidget(self.label_6, 0, 1, 1, 1)

        # combobox optimizer
        self.optimizerBox = QtWidgets.QComboBox(self.ANNconfigurationTab)
        self.optimizerBox.setObjectName("optimizerBox")
        self.optimizerBox.addItems(optimizerList)
        self.gridLayoutOptimizer.addWidget(self.optimizerBox, 0, 2, 1, 1)

        # text pada tab konfigurasi ANN : epoch
        self.labelEpoch = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelEpoch.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEpoch.setObjectName("labelEpoch")
        self.gridLayoutOptimizer.addWidget(self.labelEpoch, 1, 0, 1, 1)

        # text pada tab konfigurasi ANN : titik dua epoch
        self.labelColonEpoch = QtWidgets.QLabel(self.ANNconfigurationTab)
        self.labelColonEpoch.setAlignment(QtCore.Qt.AlignCenter)
        self.labelColonEpoch.setObjectName("labelColonEpoch")
        self.gridLayoutOptimizer.addWidget(self.labelColonEpoch, 1, 1, 1, 1)

        # spinbox epoch
        self.spinBoxEpoch = QtWidgets.QSpinBox(self.ANNconfigurationTab)
        self.spinBoxEpoch.setMaximum(100000)
        self.spinBoxEpoch.setValue(100)
        self.spinBoxEpoch.setObjectName("spinBoxEpoch")
        self.gridLayoutOptimizer.addWidget(self.spinBoxEpoch, 1, 2, 1, 1)

        # text pada tab konfigurasi ANN : prediction until
        #self.label_16 = QtWidgets.QLabel(self.ANNconfigurationTab)
        #self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        #self.label_16.setObjectName("label_16")
        #self.gridLayoutOptimizer.addWidget(self.label_16, 2, 0, 1, 1)

        # text pada tab konfigurasi ANN : titik dua prediction until
        #self.label_17 = QtWidgets.QLabel(self.ANNconfigurationTab)
        #self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        #self.label_17.setObjectName("label_17")
        #self.gridLayoutOptimizer.addWidget(self.label_17, 2, 1, 1, 1)

        # tahun prediksi
        #self.dateEdit = QtWidgets.QDateEdit(self.ANNconfigurationTab)
        #self.dateEdit.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        #self.dateEdit.setDate(QtCore.QDate(2020, 1, 1))
        #self.dateEdit.setObjectName("dateEdit")
        #self.gridLayoutOptimizer.addWidget(self.dateEdit, 2, 2, 1, 1)

        # sulit dijelaskan
        #self.verticalLayout_ANNconfigurationTab.addLayout(self.gridLayoutOptimizer)


        # tombol proses ANN (dengan training)
        self.processANNButton = QtWidgets.QPushButton(self.ANNconfigurationTab)
        self.processANNButton.setObjectName("processANNButton")
        self.processANNButton.clicked.connect(self.processANNVerifySignal)

        # tombol generate / predict dengan model yang sudah ada (tanpa training)
        self.predictingANNButton = QtWidgets.QPushButton(self.ANNconfigurationTab)
        self.predictingANNButton.setObjectName("predictingANNButton")
        self.predictingANNButton.setDisabled(True)
        self.predictingANNButton.clicked.connect(self.predictingANNVerifySignal)

        # layout horizontal khusus button
        self.buttonprocessLayout = QtWidgets.QHBoxLayout()
        self.buttonprocessLayout.setObjectName("buttonprocessLayout")
        self.buttonprocessLayout.addWidget(self.processANNButton)
        self.buttonprocessLayout.addWidget(self.predictingANNButton)

        # sulit dijelaskan
        self.tabWidget_rightSide_ANNtab.addTab(self.ANNconfigurationTab, "")

        self.graphANNgroupLayout = QtWidgets.QVBoxLayout()
        self.graphANNgroupLayout.setObjectName("graphANNgroupLayout")
        self.graphANNgroupLayout.addWidget(self.labelGraph_ANNconfigurationTab)
        self.graphANNgroupLayout.addWidget(self.graphANN)


        self.packageForGraphANNgroupLayout = QtWidgets.QWidget()
        self.packageForGraphANNgroupLayout.setObjectName("packageForGraphANNgroupLayout")
        self.packageForGraphANNgroupLayout.setLayout(self.graphANNgroupLayout)

        self.tableANNgroupLayout = QtWidgets.QVBoxLayout()
        self.tableANNgroupLayout.setObjectName("tableANNgroupLayout")
        self.tableANNgroupLayout.addWidget(self.labelArchitecture_ANNconfigurationTab)
        self.tableANNgroupLayout.addLayout(self.gridLayout_devideLayerAndNeuron)
        self.tableANNgroupLayout.addWidget(self.line_4)
        self.tableANNgroupLayout.addLayout(self.gridLayoutOptimizer)
        self.tableANNgroupLayout.addLayout(self.buttonprocessLayout)

        self.packageForTableANNgroupLayout = QtWidgets.QWidget()
        self.packageForTableANNgroupLayout.setObjectName("packageForTableANNgroupLayout")
        self.packageForTableANNgroupLayout.setLayout(self.tableANNgroupLayout)

        self.splitterGraphAndTable = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitterGraphAndTable.setObjectName("splitterGraphAndTable")
        self.splitterGraphAndTable.addWidget(self.packageForGraphANNgroupLayout)
        self.splitterGraphAndTable.addWidget(self.packageForTableANNgroupLayout)

        # vertical Layout dalam tab konfigurasi ANN
        self.verticalLayout_ANNconfigurationTab = QtWidgets.QVBoxLayout(self.ANNconfigurationTab)
        self.verticalLayout_ANNconfigurationTab.setObjectName("verticalLayout_ANNconfigurationTab")
        self.verticalLayout_ANNconfigurationTab.addWidget(self.splitterGraphAndTable)

        # footer
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.addWidget(self.label_5)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setValue(0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.progressBar.setVisible(True)

        self.gridLayout_devide2side_ANNtab.addWidget(self.tabWidget_rightSide_ANNtab)
        self.verticalLayout.addWidget(self.gridLayout_devide2side_ANNtab)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        mainTabLayout.addTab(self.tab, "")



        '''----------------------------------ANN Training Tab--------------------------------------------'''

        self.ANNtrainingTab = QtWidgets.QWidget()
        self.ANNtrainingTab.setObjectName("ANNtrainingTab")
        self.verticalLayout_ANNtrainingTab = QtWidgets.QVBoxLayout(self.ANNtrainingTab)
        self.verticalLayout_ANNtrainingTab.setObjectName("verticalLayout_ANNtrainingTab")

        self.labelGraph_ANNtrainingTab = QtWidgets.QLabel(self.ANNtrainingTab)
        self.labelGraph_ANNtrainingTab.setFont(font)
        self.labelGraph_ANNtrainingTab.setObjectName("labelGraph_ANNtrainingTab")
        #self.verticalLayout_ANNtrainingTab.addWidget(self.labelGraph_ANNtrainingTab)

        self.graph_ANNtrainingTab = pg.PlotWidget(self.ANNtrainingTab)
        self.graph_ANNtrainingTab.setBackground('w')
        self.graph_ANNtrainingTab.setObjectName("graph_ANNtrainingTab")

        self.graph_ANNtrainingTab.setLabel('bottom', 'Month')
        self.legendGraph_ANNtrainingTab = self.graph_ANNtrainingTab.addLegend()
        #self.verticalLayout_ANNtrainingTab.addWidget(self.graph_ANNtrainingTab)


        self.graphANNtrainingTabGroupLayout = QtWidgets.QVBoxLayout()
        self.graphANNtrainingTabGroupLayout.setObjectName("graphANNtrainingTabGroupLayout")
        self.graphANNtrainingTabGroupLayout.addWidget(self.labelGraph_ANNtrainingTab)
        self.graphANNtrainingTabGroupLayout.addWidget(self.graph_ANNtrainingTab)

        self.packageForGraphANNtrainingTabGroupLayout = QtWidgets.QWidget()
        self.packageForGraphANNtrainingTabGroupLayout.setObjectName("packageForGraphANNtrainingTabGroupLayout")
        self.packageForGraphANNtrainingTabGroupLayout.setLayout(self.graphANNtrainingTabGroupLayout)

        self.labelTable_ANNtrainingTab = QtWidgets.QLabel(self.ANNtrainingTab)
        self.labelTable_ANNtrainingTab.setFont(font)
        self.labelTable_ANNtrainingTab.setObjectName("labelTable_ANNtrainingTab")
        self.verticalLayout_ANNtrainingTab.addWidget(self.labelTable_ANNtrainingTab)

        self.horizontalLayout_ANNtrainingTab = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ANNtrainingTab.setObjectName("horizontalLayout_ANNtrainingTab")

        self.table_ANNtrainingTab = QtWidgets.QTableWidget(self.ANNtrainingTab)
        self.table_ANNtrainingTab.setObjectName("table_ANNtrainingTab")
        self.table_ANNtrainingTab.setColumnCount(100)
        self.table_ANNtrainingTab.setRowCount(100)
        #self.horizontalLayout_ANNtrainingTab.addWidget(self.table_ANNtrainingTab)

        self.tableANNtrainingTabGroupLayout = QtWidgets.QVBoxLayout()
        self.tableANNtrainingTabGroupLayout.setObjectName("tableANNtrainingTabGroupLayout")
        self.tableANNtrainingTabGroupLayout.addWidget(self.labelTable_ANNtrainingTab)
        self.tableANNtrainingTabGroupLayout.addWidget(self.table_ANNtrainingTab)

        self.packageForTableANNtrainingTabGroupLayout = QtWidgets.QWidget()
        self.packageForTableANNtrainingTabGroupLayout.setObjectName("packageForTableANNtrainingTabGroupLayout")
        self.packageForTableANNtrainingTabGroupLayout.setLayout(self.tableANNtrainingTabGroupLayout)

        self.splitterGraphAndTable_ANNtrainingTab = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitterGraphAndTable_ANNtrainingTab.setObjectName("splitterGraphAndTable_ANNtrainingTab")
        self.splitterGraphAndTable_ANNtrainingTab.addWidget(self.packageForGraphANNtrainingTabGroupLayout)
        self.splitterGraphAndTable_ANNtrainingTab.addWidget(self.packageForTableANNtrainingTabGroupLayout)

        #self.verticalLayout_ANNtrainingTab.addLayout(self.horizontalLayout_ANNtrainingTab)
        self.verticalLayout_ANNtrainingTab.addWidget(self.splitterGraphAndTable_ANNtrainingTab)
        self.tabWidget_rightSide_ANNtab.addTab(self.ANNtrainingTab, "")



        '''----------------------------------ANN Testing Tab--------------------------------------------'''

        self.ANNtestingTab = QtWidgets.QWidget()
        self.ANNtestingTab.setObjectName("ANNtestingTab")
        self.verticalLayout_ANNtestingTab = QtWidgets.QVBoxLayout(self.ANNtestingTab)
        self.verticalLayout_ANNtestingTab.setObjectName("verticalLayout_ANNtestingTab")

        self.labelGraph_ANNtestingTab = QtWidgets.QLabel(self.ANNtestingTab)
        self.labelGraph_ANNtestingTab.setFont(font)
        self.labelGraph_ANNtestingTab.setObjectName("labelGraph_ANNtestingTab")
        #self.verticalLayout_ANNtestingTab.addWidget(self.labelGraph_ANNtestingTab)

        self.graph_ANNtestingTab = pg.PlotWidget(self.ANNtrainingTab)
        self.graph_ANNtestingTab.setBackground('w')
        self.graph_ANNtestingTab.setObjectName("graph_ANNtestingTab")
        #self.graph_ANNtestingTab.setLabel('left', 'Rainfall (mm)')
        self.graph_ANNtestingTab.setLabel('bottom', 'Month')

        self.legendGraph_ANNtestingTab = self.graph_ANNtestingTab.addLegend()
        #self.verticalLayout_ANNtestingTab.addWidget(self.graph_ANNtestingTab)

        self.graphANNtestingTabGroupLayout = QtWidgets.QVBoxLayout()
        self.graphANNtestingTabGroupLayout.setObjectName("graphANNtestingTabGroupLayout")
        self.graphANNtestingTabGroupLayout.addWidget(self.labelGraph_ANNtestingTab)
        self.graphANNtestingTabGroupLayout.addWidget(self.graph_ANNtestingTab)

        self.packageForGraphANNtestingTabGroupLayout = QtWidgets.QWidget()
        self.packageForGraphANNtestingTabGroupLayout.setObjectName("packageForGraphANNtestingTabGroupLayout")
        self.packageForGraphANNtestingTabGroupLayout.setLayout(self.graphANNtestingTabGroupLayout)

        self.labelTable_ANNtestingTab = QtWidgets.QLabel(self.ANNtestingTab)
        self.labelTable_ANNtestingTab = QtWidgets.QLabel(self.ANNtestingTab)
        self.labelTable_ANNtestingTab.setFont(font)
        self.labelTable_ANNtestingTab.setObjectName("labelTable_ANNtestingTab")
        #self.verticalLayout_ANNtestingTab.addWidget(self.labelTable_ANNtestingTab)

        self.table_ANNtestingTab = QtWidgets.QTableWidget(self.ANNtestingTab)
        self.table_ANNtestingTab.setObjectName("table_ANNtestingTab")
        self.table_ANNtestingTab.setColumnCount(100)
        self.table_ANNtestingTab.setRowCount(100)

        #self.horizontalLayout_ANNtestingTab = QtWidgets.QHBoxLayout()
        #self.horizontalLayout_ANNtestingTab.setObjectName("horizontalLayout_ANNtestingTab")
        #self.horizontalLayout_ANNtestingTab.addWidget(self.table_ANNtestingTab)

        self.tableANNtestingTabGroupLayout = QtWidgets.QVBoxLayout()
        self.tableANNtestingTabGroupLayout.setObjectName("tableANNtestingTabGroupLayout")
        self.tableANNtestingTabGroupLayout.addWidget(self.labelTable_ANNtestingTab)
        self.tableANNtestingTabGroupLayout.addWidget(self.table_ANNtestingTab)

        self.packageForTableANNtestingTabGroupLayout = QtWidgets.QWidget()
        self.packageForTableANNtestingTabGroupLayout.setObjectName("packageForTableANNtestingTabGroupLayout")
        self.packageForTableANNtestingTabGroupLayout.setLayout(self.tableANNtestingTabGroupLayout)

        self.splitterGraphAndTable_ANNtestingTab = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitterGraphAndTable_ANNtestingTab.setObjectName("splitterGraphAndTable_ANNtestingTab")
        self.splitterGraphAndTable_ANNtestingTab.addWidget(self.packageForGraphANNtestingTabGroupLayout)
        self.splitterGraphAndTable_ANNtestingTab.addWidget(self.packageForTableANNtestingTabGroupLayout)

        # self.verticalLayout_ANNtrainingTab.addLayout(self.horizontalLayout_ANNtrainingTab)
        self.verticalLayout_ANNtestingTab.addWidget(self.splitterGraphAndTable_ANNtestingTab)

        #self.verticalLayout_ANNtestingTab.addLayout(self.horizontalLayout_ANNtestingTab)
        self.tabWidget_rightSide_ANNtab.addTab(self.ANNtestingTab, "")



        '''----------------------------------ANN Validation Tab--------------------------------------------

        self.tabValidationANN = QtWidgets.QWidget()
        self.tabValidationANN.setObjectName("tabValidationANN")
        self.tabWidget_rightSide_ANNtab.addTab(self.tabValidationANN, "")

        
        '''




        '''----------------------------------ANN Prediction Tab--------------------------------------------'''
        """
        self.ANNpredictionTab = QtWidgets.QWidget()
        self.ANNpredictionTab.setObjectName("ANNpredictionTab")
        self.verticalLayout_ANNpredictionTab = QtWidgets.QVBoxLayout(self.ANNpredictionTab)
        self.verticalLayout_ANNpredictionTab.setObjectName("verticalLayout_ANNpredictionTab")

        self.labelGraph_ANNpredictionTab = QtWidgets.QLabel(self.ANNpredictionTab)
        self.labelGraph_ANNpredictionTab.setFont(font)
        self.labelGraph_ANNpredictionTab.setObjectName("labelTable_ANNtrainingTab")
        #self.verticalLayout_ANNpredictionTab.addWidget(self.labelGraph_ANNpredictionTab)

        self.graph_ANNpredictionTab = pg.PlotWidget(self.ANNpredictionTab)
        self.graph_ANNpredictionTab.setBackground('w')
        self.graph_ANNpredictionTab.setObjectName("graph_ANNpredictionTab")
        self.graph_ANNpredictionTab.setLabel('left', 'Rainfall (mm)')
        self.graph_ANNpredictionTab.setLabel('bottom', 'Month')
        self.legendGraph_ANNpredictionTab = self.graph_ANNpredictionTab.addLegend()
        #self.verticalLayout_ANNpredictionTab.addWidget(self.graph_ANNpredictionTab)

        #self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        #self.horizontalLayout_14.setObjectName("horizontalLayout_14")

        self.labelTable_ANNpredictionTab = QtWidgets.QLabel(self.ANNpredictionTab)
        self.labelTable_ANNpredictionTab.setFont(font)
        self.labelTable_ANNpredictionTab.setObjectName("labelTable_ANNtrainingTab")
        #self.verticalLayout_ANNpredictionTab.addWidget(self.labelTable_ANNpredictionTab)

        self.table_ANNpredictionTab = QtWidgets.QTableWidget(self.ANNpredictionTab)
        self.table_ANNpredictionTab.setObjectName("table_ANNpredictionTab")
        self.table_ANNpredictionTab.setColumnCount(100)
        self.table_ANNpredictionTab.setRowCount(100)
        #self.horizontalLayout_14.addWidget(self.table_ANNpredictionTab)

        self.graphANNpredictionTabGroupLayout = QtWidgets.QVBoxLayout()
        self.graphANNpredictionTabGroupLayout.setObjectName("graphANNpredictionTabGroupLayout")
        self.graphANNpredictionTabGroupLayout.addWidget(self.labelGraph_ANNpredictionTab)
        self.graphANNpredictionTabGroupLayout.addWidget(self.graph_ANNpredictionTab)

        self.packageForGraphANNpredictionTabGroupLayout = QtWidgets.QWidget()
        self.packageForGraphANNpredictionTabGroupLayout.setObjectName("packageForGraphANNpredictionTabGroupLayout")
        self.packageForGraphANNpredictionTabGroupLayout.setLayout(self.graphANNpredictionTabGroupLayout)

        self.tableANNpredictionTabGroupLayout = QtWidgets.QVBoxLayout()
        self.tableANNpredictionTabGroupLayout.setObjectName("tableANNpredictionTabGroupLayout")
        self.tableANNpredictionTabGroupLayout.addWidget(self.labelTable_ANNpredictionTab)
        self.tableANNpredictionTabGroupLayout.addWidget(self.table_ANNpredictionTab)

        self.packageForTableANNpredictionTabGroupLayout = QtWidgets.QWidget()
        self.packageForTableANNpredictionTabGroupLayout.setObjectName("packageForTableANNpredictionTabGroupLayout")
        self.packageForTableANNpredictionTabGroupLayout.setLayout(self.tableANNpredictionTabGroupLayout)

        self.splitterGraphAndTable_ANNpredictionTab = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitterGraphAndTable_ANNpredictionTab.setObjectName("splitterGraphAndTable_ANNpredictionTab")
        self.splitterGraphAndTable_ANNpredictionTab.addWidget(self.packageForGraphANNpredictionTabGroupLayout)
        self.splitterGraphAndTable_ANNpredictionTab.addWidget(self.packageForTableANNpredictionTabGroupLayout)

        # self.verticalLayout_ANNtrainingTab.addLayout(self.horizontalLayout_ANNtrainingTab)
        self.verticalLayout_ANNpredictionTab.addWidget(self.splitterGraphAndTable_ANNpredictionTab)

        #self.verticalLayout_ANNpredictionTab.addLayout(self.horizontalLayout_14)
        
        self.tabWidget_rightSide_ANNtab.addTab(self.ANNpredictionTab, "")
        """
        '''----------------------------------------------------------------------------------------------'''
        self.tabWidget_rightSide_ANNtab.setCurrentIndex(0)
        #self.tabWidget_2.setCurrentIndex(0)
        self.retranslateUi(mainTabLayout)
        self.declareInit()

    def declareInit(self):
        self.counterANN = 0
        self.rgb = [[255, 123, 123],  #pink tua
                    [15, 218, 255],  # biru muda
                    [37, 178, 55],  #ijo tua
                    #[158, 158, 158],  #abu abu
                    #[255, 108, 0],  # abu abu
                    [187, 90, 200],  # ungu tua
                    [125, 225, 214],  # biru langit
                    [67, 136, 0],  #ijo lumut
                    [255, 216, 70],  # kuning
                    [187, 81, 200],  #ungu tua
                    [100, 120, 150],  # abu tua
                    [190, 200, 50],  #kuning ijo tua
                    [255, 147, 266]] #hitam
        self.counterANNtrainingTab = 0
        self.counterANNtestingTab = 0
        self.counterANNpredictionTab = 0

    '''-----------------------------------------------------------------------------------------------
    Fungsi Untuk mengubah tampilan pada tab konfigurasi ann
    -----------------------------------------------------------------------------------------------'''
    def setYgraphANN(self, y):
        self.graphANN.setLabel('left', y)
        self.graph_ANNtrainingTab.setLabel('left', y)
        self.graph_ANNtestingTab.setLabel('left', y)

    def setXgraphLegend(self, x):
        self.graphANN.setLabel('bottom', x)
        self.graph_ANNtrainingTab.setLabel('bottom', x)
        self.graph_ANNtestingTab.setLabel('bottom', x)

    def onRadioBtn(self):
         return(self.sender())

    def progressTrainingBar(self, value):
        self.progressBar.setValue(value)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and
                event.matches(QtGui.QKeySequence.Copy)):
            self.copySelection()
            return True
        return super(viewAnn, self).eventFilter(source, event)

    # add copy method
    def copySelection(self):
        selection = self.tableANNDataset.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            QtWidgets.qApp.clipboard().setText(stream.getvalue())

    def setOpenArchitecture(self, layer, activation):
        self.numOfHiddenLayer.setValue(len(layer)-1)
        for i in range(len(layer)-1):
            exec("self.spinBoxLayerNum_" + str(i) + ".setValue(" + layer[i][3] + ")")
            """
            if activation[i] == 'tanh':
                act = 0
            elif activation[i] == 'sigmoid':
                act = 1
            elif activation[i] == 'relu':
                act = 2
            """
            exec("self.actHidLayerBoxLayerNum_" + str(i) + ".setCurrentText('" + activation[i] + "')")
            self.actOutputLayerBox.setCurrentText(activation[i])
            self.predictingANNButton.setDisabled(False)
            """
            if activation[2] == 'tanh':
                act = 0
            elif activation[2] == 'sigmoid':
                act = 1
            elif activation[2] == 'relu':
                act = 2
            """


    def progressBar(self, value):
        self.progressBar.setValue(value)

    def resetArchitecture(self):
        self.numOfHiddenLayer.setValue(0)

    def canvasANN(self, dataset, info):
        pen = pg.mkPen(color=(self.rgb[self.counterANN][0],
                              self.rgb[self.counterANN][1],
                              self.rgb[self.counterANN][2]),
                       width=2)
        y = dataset
        #x = pd.to_datetime(dataset.index)
        #print(x)
        exec("self.plotANN" + str(self.counterANN) + " = self.graphANN.plot(y, pen=pen, name=info)")
        self.counterANN = self.counterANN + 1

    def resetTable(self,columns):
        self.comboboxChooseTarget.setCurrentIndex(0)

        for i in range(len(columns),0,-1):
            self.comboboxChooseTarget.removeItem(i)

        self.tableANNDataset.clear()
        self.tableANNDataset.setRowCount(100)
        self.tableANNDataset.setColumnCount(100)

        self.table_ANNtrainingTab.clear()
        self.table_ANNtestingTab.clear()
        #self.table_ANNpredictionTab.clear()

    def resetGraph(self):
        self.legendGraph_ANNconfigurationTab.scene().removeItem(self.legendGraph_ANNconfigurationTab)
        self.legendGraph_ANNtrainingTab.scene().removeItem(self.legendGraph_ANNtrainingTab)
        self.legendGraph_ANNtestingTab.scene().removeItem(self.legendGraph_ANNtestingTab)
        #self.legendGraph_ANNpredictionTab.scene().removeItem(self.legendGraph_ANNpredictionTab)

        self.legendGraph_ANNconfigurationTab = self.graphANN.addLegend()
        self.legendGraph_ANNtrainingTab = self.graph_ANNtrainingTab.addLegend()
        self.legendGraph_ANNtestingTab = self.graph_ANNtestingTab.addLegend()
        #self.legendGraph_ANNpredictionTab = self.graph_ANNpredictionTab.addLegend()

        for i in range(self.counterANN - 1, -1, -1):
            exec("self.graphANN.removeItem(self.plotANN" + str(i) + ")")
        for i in range(self.counterANNtrainingTab, 0, -1):
            exec("self.graph_ANNtrainingTab.removeItem(self.plotANN_graph_ANNtrainingTab" + str(i) + ")")
        for i in range(self.counterANNtestingTab, 0, -1):
            exec("self.graph_ANNtestingTab.removeItem(self.plotANN_graph_ANNtestingTab" + str(i) + ")")
        for i in range(self.counterANNpredictionTab, 0, -1):
            exec("self.graph_ANNpredictionTab.removeItem(self.plotANN_graph_ANNpredictionTab" + str(i) + ")")

        self.counterANN = 0
        self.counterANNtrainingTab = 0
        self.counterANNtestingTab = 0
        self.counterANNpredictionTab = 0

    def showChooseTargetList(self, list):
        self.comboboxChooseTarget.addItems(list)

    def showTableANN(self, dataset):
        self.tableANNDataset.setRowCount(dataset.shape[0])
        self.tableANNDataset.setColumnCount(dataset.shape[1])
        for i in range(dataset.shape[1]):
            self.tableANNDataset.setHorizontalHeaderLabels(dataset.columns)
        for j in range(dataset.shape[0]):
            for i in range(dataset.shape[1]):
                self.tableANNDataset.setItem(j, i, QTableWidgetItem(str(dataset.iat[j, i])))

    def showTableTrainingANN(self, dataset):
        columns = ["Date", "Actual", "Prediction"]
        self.table_ANNtrainingTab.setRowCount(dataset.shape[0])
        self.table_ANNtrainingTab.setColumnCount(dataset.shape[1])
        for i in range(dataset.shape[1]):
            self.table_ANNtrainingTab.setHorizontalHeaderLabels(columns)
        for j in range(dataset.shape[0]):
            for i in range(dataset.shape[1]):
                self.table_ANNtrainingTab.setItem(j, i, QTableWidgetItem(str(dataset[j, i])))
        #self.table_ANNtrainingTab.resizeColumnsToContents()

    def showTableTestingANN(self, dataset):
        columns = ["Date", "Actual", "Prediction"]
        self.table_ANNtestingTab.setRowCount(dataset.shape[0])
        self.table_ANNtestingTab.setColumnCount(dataset.shape[1])
        for i in range(dataset.shape[1]):
            self.table_ANNtestingTab.setHorizontalHeaderLabels(columns)
        for j in range(dataset.shape[0]):
            for i in range(dataset.shape[1]):
                self.table_ANNtestingTab.setItem(j, i, QTableWidgetItem(str(dataset[j, i])))

    def changeTheHidLayer(self, valueAfterChanged, valueBeforeChanged):
        if (valueBeforeChanged != 0):
            for i in range(valueBeforeChanged):
                exec("self.gridLayoutTable_gridLayoutNeuron.removeWidget(self.layerNum_"+str(i)+")")
                exec("self.layerNum_"+str(i)+".deleteLater()")
                exec("self.layerNum_"+str(i)+" = None")
                exec("self.gridLayoutTable_gridLayoutNeuron.removeWidget(self.spinBoxLayerNum_"+str(i)+")")
                exec("self.spinBoxLayerNum_"+str(i)+".deleteLater()")
                exec("self.spinBoxLayerNum_"+str(i)+" = None")
                exec("self.gridLayoutTable_gridLayoutNeuron.removeWidget(self.actHidLayerBoxLayerNum_"+str(i)+")")
                exec("self.actHidLayerBoxLayerNum_"+str(i)+".deleteLater()")
                exec("self.actHidLayerBoxLayerNum_"+str(i)+" = None")

                #exec("self.gridLayoutTable_gridLayoutNeuron.removeWidget(self.spacerItem1)")
                #exec("self.spacerItem1.deleteLater()")
                #exec("self.spacerItem1 = None")

        x1=1
        x2=0
        x3=1
        x4=1

        for i in range(valueAfterChanged):
            exec("self.layerNum_"+str(i)+"= QtWidgets.QLabel(self.ANNconfigurationTab)")
            exec("self.layerNum_"+str(i)+".setAlignment(QtCore.Qt.AlignCenter)")
            exec("self.layerNum_"+str(i)+".setObjectName('layerNum_"+str(i)+"')")
            exec("self.layerNum_"+str(i)+".setText('"+str(i+1)+"')")
            exec("self.gridLayoutTable_gridLayoutNeuron.addWidget(self.layerNum_"+str(i)+", "+str(x1)+", "+str(x2)+", "+str(x3)+", "+str(x4)+")")
            exec("self.spinBoxLayerNum_"+str(i)+" = QtWidgets.QSpinBox(self.ANNconfigurationTab)")
            exec("self.spinBoxLayerNum_"+str(i)+".setObjectName('spinBoxLayerNum_"+str(i)+"')")
            exec("self.spinBoxLayerNum_"+str(i)+".setMaximum(1000)")
            exec("self.gridLayoutTable_gridLayoutNeuron.addWidget(self.spinBoxLayerNum_"+str(i)+", "+str(x1)+", "+str(x2+1)+", "+str(x3)+", "+str(x4)+")")
            exec("self.actHidLayerBoxLayerNum_"+str(i)+" = QtWidgets.QComboBox(self.ANNconfigurationTab)")
            exec("self.actHidLayerBoxLayerNum_"+str(i)+".setObjectName('actHidLayerBoxLayerNum_"+str(i)+"')")
            exec("self.actHidLayerBoxLayerNum_"+str(i)+".addItems(activationList)")
            exec("self.gridLayoutTable_gridLayoutNeuron.addWidget(self.actHidLayerBoxLayerNum_"+str(i)+", "+str(x1)+", "+str(x2+2)+", "+str(x3)+", "+str(x4)+")")
            x1+=1

        self.gridLayoutTable_gridLayoutNeuron.addItem(self.spacerItem1, valueAfterChanged, 1, 1, 1)

    '''-----------------------------------------------------------------------------------------------
    Fungsi Untuk mengubah tampilan pada tab training ann
    -----------------------------------------------------------------------------------------------'''

    def canvasANNtrainingTab(self, dataset, info):
        self.counterANNtrainingTab = self.counterANNtrainingTab + 1
        pen = pg.mkPen(color=(self.rgb[self.counterANNtrainingTab-1][0],
                              self.rgb[self.counterANNtrainingTab-1][1],
                              self.rgb[self.counterANNtrainingTab-1][2]),
                       width=2)
        y = dataset
        exec("self.plotANN_graph_ANNtrainingTab" + str(self.counterANNtrainingTab) + " = self.graph_ANNtrainingTab.plot(y, pen=pen, name=info)")


    '''-----------------------------------------------------------------------------------------------
        Fungsi Untuk mengubah tampilan pada tab testing ann
        -----------------------------------------------------------------------------------------------'''

    def canvasANNtestingTab(self, dataset, info):
        self.counterANNtestingTab = self.counterANNtestingTab + 1
        if self.counterANNtestingTab == 1:
            pen = pg.mkPen(color=(self.rgb[self.counterANNtestingTab-1][0],
                                  self.rgb[self.counterANNtestingTab-1][1],
                                  self.rgb[self.counterANNtestingTab-1][2]),
                           width=3)
        elif self.counterANNtestingTab != 1:
            pen = pg.mkPen(color=(self.rgb[self.counterANNtestingTab][0],
                                  self.rgb[self.counterANNtestingTab][1],
                                  self.rgb[self.counterANNtestingTab][2]),
                           width=3)
        y = dataset
        exec("self.plotANN_graph_ANNtestingTab" + str(
            self.counterANNtestingTab) + " = self.graph_ANNtestingTab.plot(y, pen=pen, name=info)")

    def canvasANNpredictionTab(self, dataset, info):
        self.counterANNpredictionTab = self.counterANNpredictionTab + 1
        pen = pg.mkPen(color=(self.rgb[self.counterANNpredictionTab][0],
                              self.rgb[self.counterANNpredictionTab][1],
                              self.rgb[self.counterANNpredictionTab][2]),
                       width=3)
        y = dataset
        exec("self.plotANN_graph_ANNpredictionTab" + str(
            self.counterANNpredictionTab) + " = self.graph_ANNpredictionTab.plot(y, pen=pen, name=info)")

    def retranslateUi(self, mainTabLayout):
        _translate = QtCore.QCoreApplication.translate
        #ANN configuraion TAB
        self.browseANNButton.setText(_translate("MainWindow", "Browse File (.xlsx/.csv)"))
        self.resetANNButton.setText(_translate("MainWindow", "Reset Model"))
        self.labelGraph_ANNconfigurationTab.setText(_translate("MainWindow", "Graph"))
        self.labelArchitecture_ANNconfigurationTab.setText(_translate("MainWindow", "Architecture"))

        self.labelHidLayer_ANNconfigurationTab.setText(_translate("MainWindow", "Hidden Layer"))
        self.labelNumberOfHidLayer_ANNconfigurationTab.setText(_translate("MainWindow", "Number of Hidden Layer"))
        self.labelOutputLayer_ANNconfigurationTab.setText(_translate("MainWindow", "Output Layer"))
        self.labelActivation_ANNconfigurationTab.setText(_translate("MainWindow", "Activation"))
        self.label.setText(_translate("MainWindow", "Neuron"))

        self.label_2.setText(_translate("MainWindow", "Activation"))
        self.labelLayerColumn_ANNconfigurationTab.setText(_translate("MainWindow", "Layer"))
        self.labelChooseTarget.setText(_translate("MainWindow", "Choose The Target"))
        self.label_6.setText(_translate("MainWindow", ":"))
        self.label_4.setText(_translate("MainWindow", "Optimizer"))
        #self.label_16.setText(_translate("MainWindow", "Prediction until"))
        #self.label_17.setText(_translate("MainWindow", ":"))
        #self.dateEdit.setDisplayFormat(_translate("MainWindow", "yyyy"))
        self.labelEpoch.setText(_translate("MainWindow", "Epoch"))
        self.labelColonEpoch.setText(_translate("MainWindow", ":"))
        self.processANNButton.setText(_translate("MainWindow", "Train + Predict"))
        self.predictingANNButton.setText(_translate("MainWindow", "Predict Only"))
        self.tabWidget_rightSide_ANNtab.setTabText(self.tabWidget_rightSide_ANNtab.indexOf(self.ANNconfigurationTab),
                                                   _translate("MainWindow", "ANN Configuration"))
        mainTabLayout.setTabText(mainTabLayout.indexOf(self.tab),
                                      _translate("MainWindow", "Artificial Neural Network"))

        #ANN training Tab
        self.tabWidget_rightSide_ANNtab.setTabText(self.tabWidget_rightSide_ANNtab.indexOf(self.ANNtrainingTab),
                                                   _translate("MainWindow", "Training"))
        self.labelGraph_ANNtrainingTab.setText(_translate("MainWindow", "Graph"))
        self.labelTable_ANNtrainingTab.setText(_translate("MainWindow", "Table"))

        #ANN testing Tab
        self.tabWidget_rightSide_ANNtab.setTabText(self.tabWidget_rightSide_ANNtab.indexOf(self.ANNtestingTab),
                                                   _translate("MainWindow", "Testing/Validation"))
        self.labelGraph_ANNtestingTab.setText(_translate("MainWindow", "Graph"))
        self.labelTable_ANNtestingTab.setText(_translate("MainWindow", "Table"))


        #ANN prediction Tab
        #self.tabWidget_rightSide_ANNtab.setTabText(self.tabWidget_rightSide_ANNtab.indexOf(self.ANNpredictionTab),
        #                                           _translate("MainWindow", "Prediction"))
        #self.labelGraph_ANNpredictionTab.setText(_translate("MainWindow", "Graph"))
        #self.labelTable_ANNpredictionTab.setText(_translate("MainWindow", "Table"))

        '''
        #ANN validation Tab
        self.tabWidget_rightSide_ANNtab.setTabText(self.tabWidget_rightSide_ANNtab.indexOf(self.tabValidationANN),
                                                   _translate("MainWindow", "Validation"))
        '''
        self.label_5.setText(_translate("MainWindow", "TextLabel"))



class DateAxisItem(AxisItem):
    """
    A tool that provides a date-time aware axis. It is implemented as an
    AxisItem that interpretes positions as unix timestamps (i.e. seconds
    since 1970).
    The labels and the tick positions are dynamically adjusted depending
    on the range.
    It provides a  :meth:`attachToPlotItem` method to add it to a given
    PlotItem
    """

    # Max width in pixels reserved for each label in axis
    _pxLabelWidth = 80

    def __init__(self, *args, **kwargs):
        AxisItem.__init__(self, *args, **kwargs)
        self._oldAxis = None

    def tickValues(self, minVal, maxVal, size):
        """
        Reimplemented from PlotItem to adjust to the range and to force
        the ticks at "round" positions in the context of time units instead of
        rounding in a decimal base
        """

        maxMajSteps = int(size / self._pxLabelWidth)

        dt1 = datetime.fromtimestamp(minVal)
        dt2 = datetime.fromtimestamp(maxVal)

        dx = maxVal - minVal
        majticks = []

        if dx > 63072001:  # 3600s*24*(365+366) = 2 years (count leap year)
            d = timedelta(days=366)
            for y in range(dt1.year + 1, dt2.year):
                dt = datetime(year=y, month=1, day=1)
                majticks.append(mktime(dt.timetuple()))

        elif dx > 5270400:  # 3600s*24*61 = 61 days
            d = timedelta(days=31)
            dt = dt1.replace(day=1, hour=0, minute=0,
                             second=0, microsecond=0) + d
            while dt < dt2:
                # make sure that we are on day 1 (even if always sum 31 days)
                dt = dt.replace(day=1)
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 172800:  # 3600s24*2 = 2 days
            d = timedelta(days=1)
            dt = dt1.replace(hour=0, minute=0, second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 7200:  # 3600s*2 = 2hours
            d = timedelta(hours=1)
            dt = dt1.replace(minute=0, second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 1200:  # 60s*20 = 20 minutes
            d = timedelta(minutes=10)
            dt = dt1.replace(minute=(dt1.minute // 10) * 10,
                             second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 120:  # 60s*2 = 2 minutes
            d = timedelta(minutes=1)
            dt = dt1.replace(second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 20:  # 20s
            d = timedelta(seconds=10)
            dt = dt1.replace(second=(dt1.second // 10) * 10, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 2:  # 2s
            d = timedelta(seconds=1)
            majticks = range(int(minVal), int(maxVal))

        else:  # <2s , use standard implementation from parent
            return AxisItem.tickValues(self, minVal, maxVal, size)

        L = len(majticks)
        if L > maxMajSteps:
            majticks = majticks[::int(numpy.ceil(float(L) / maxMajSteps))]

        return [(d.total_seconds(), majticks)]

    def tickStrings(self, values, scale, spacing):
        """Reimplemented from PlotItem to adjust to the range"""
        ret = []
        if not values:
            return []

        if spacing >= 31622400:  # 366 days
            fmt = "%Y"

        elif spacing >= 2678400:  # 31 days
            fmt = "%Y %b"

        elif spacing >= 86400:  # = 1 day
            fmt = "%b/%d"

        elif spacing >= 3600:  # 1 h
            fmt = "%b/%d-%Hh"

        elif spacing >= 60:  # 1 m
            fmt = "%H:%M"

        elif spacing >= 1:  # 1s
            fmt = "%H:%M:%S"

        else:
            # less than 2s (show microseconds)
            # fmt = '%S.%f"'
            fmt = '[+%fms]'  # explicitly relative to last second

        for x in values:
            try:
                t = datetime.fromtimestamp(x)
                ret.append(t.strftime(fmt))
            except ValueError:  # Windows can't handle dates before 1970
                ret.append('')

        return ret

    def attachToPlotItem(self, plotItem):
        """Add this axis to the given PlotItem
        :param plotItem: (PlotItem)
        """
        self.setParentItem(plotItem)
        viewBox = plotItem.getViewBox()
        self.linkToView(viewBox)
        self._oldAxis = plotItem.axes[self.orientation]['item']
        self._oldAxis.hide()
        plotItem.axes[self.orientation]['item'] = self
        pos = plotItem.axes[self.orientation]['pos']
        plotItem.layout.addItem(self, *pos)
        self.setZValue(-1000)

    def detachFromPlotItem(self):
        """Remove this axis from its attached PlotItem
        (not yet implemented)
        """
        raise NotImplementedError()  # TODO