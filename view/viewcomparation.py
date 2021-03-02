from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import pyqtgraph as pg
import numpy as np
import sys, csv, io


class viewComparation(QtWidgets.QWidget, QtCore.QAbstractTableModel):

    def declareInit(self):
        self.counterComparation = 0
        self.rgb = [[255, 123, 123],  # pink tua
                    [190, 200, 50],  # kuning ijo tua
                    [37, 178, 55],  # ijo tua
                    [158, 158, 158],  # abu abu
                    [125, 225, 214],  # biru langit
                    [255, 216, 70],  # kuning
                    [67, 136, 0],  # ijo lumut
                    [15, 218, 255],  # biru muda
                    [187, 81, 200],  # ungu tua
                    [100, 120, 150],  # abu tua
                    [255, 147, 266]]  # hitam

    def setupUi(self, MainWindow, centralwidget, mainTabLayout):
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        self.declareInit()

        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.verticalLayout_ComparationTab = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_ComparationTab.setObjectName("verticalLayout_ComparationTab")

        self.labelGraph_ComparationTab = QtWidgets.QLabel(self.tab_5)
        self.labelGraph_ComparationTab.setFont(font)
        self.labelGraph_ComparationTab.setObjectName("labelGraph_ComparationTab")

        self.graph_ComparationTab = pg.PlotWidget(self.tab_5)
        self.graph_ComparationTab.setObjectName("graph_ComparationTab")
        self.graph_ComparationTab.setBackground('w')
        self.graph_ComparationTab.setLabel('left', 'Rainfall (mm)')
        self.graph_ComparationTab.setLabel('bottom', 'Month')
        self.legendComparation = self.graph_ComparationTab.addLegend()

        self.labelTable_ComparationTab = QtWidgets.QLabel()
        self.labelTable_ComparationTab.setFont(font)
        self.labelTable_ComparationTab.setObjectName("labelTable_ComparationTab")

        self.table_ComparationTab = QtWidgets.QTableWidget()
        self.table_ComparationTab.setObjectName("table_ComparationTab")
        self.table_ComparationTab.setColumnCount(100)
        self.table_ComparationTab.setRowCount(100)
        self.table_ComparationTab.installEventFilter(self)
        
        self.label_bulanan = QtWidgets.QLabel()
        self.label_bulanan.setFont(font)
        self.label_bulanan.setObjectName("label_bulanan")

        self.label_28 = QtWidgets.QLabel()
        self.label_28.setObjectName("label_28")

        self.label_time_bulanan = QtWidgets.QLabel()
        self.label_time_bulanan.setObjectName("label_time_bulanan")

        self.annTime_bulanan = QtWidgets.QLabel()
        self.annTime_bulanan.setObjectName("annTime_bulanan")

        self.tfTime_bulanan = QtWidgets.QLabel()
        self.tfTime_bulanan.setObjectName("tfTime_bulanan")


        self.annMSE_bulanan = QtWidgets.QLabel()
        self.annMSE_bulanan.setObjectName("annMSE_bulanan")

        self.annRsqr_bulanan = QtWidgets.QLabel()
        self.annRsqr_bulanan.setObjectName("annRsqr_bulanan")

        self.label_29 = QtWidgets.QLabel()
        self.label_29.setObjectName("label_29")

        self.tfMSE = QtWidgets.QLabel()
        self.tfMSE.setObjectName("tfMSE")

        self.tfRsqr = QtWidgets.QLabel()
        self.tfRsqr.setObjectName("tfRsqr")

        self.model_bulanan = QtWidgets.QLabel()
        self.model_bulanan.setObjectName("model_bulanan")

        self.mse_bulanan = QtWidgets.QLabel()
        self.mse_bulanan.setObjectName("mse_bulanan")

        self.rsqr_bulanan = QtWidgets.QLabel()
        self.rsqr_bulanan.setObjectName("rsqr_bulanan")

        self.label_bulanan_no = QtWidgets.QLabel()
        self.label_bulanan_no.setObjectName("label_bulanan_no")

        self.label_bulanan_1 = QtWidgets.QLabel()
        self.label_bulanan_1.setObjectName("label_bulanan_1")

        self.label_bulanan_2 = QtWidgets.QLabel()
        self.label_bulanan_2.setObjectName("label_bulanan_label_bulanan_2")

        self.gridLayout_bulanan = QtWidgets.QGridLayout()



        self.gridLayout_bulanan.addWidget(self.label_bulanan_no, 0, 0, 1, 1)
        self.gridLayout_bulanan.addWidget(self.model_bulanan, 0, 1, 1, 1)
        self.gridLayout_bulanan.addWidget(self.label_time_bulanan, 0, 2, 1, 1)
        self.gridLayout_bulanan.addWidget(self.mse_bulanan, 0, 3, 1, 1)
        self.gridLayout_bulanan.addWidget(self.rsqr_bulanan, 0, 4, 1, 1)

        self.gridLayout_bulanan.addWidget(self.label_bulanan_1, 1, 0, 1, 1)
        self.gridLayout_bulanan.addWidget(self.label_28, 1, 1, 1, 1)
        self.gridLayout_bulanan.addWidget(self.annTime_bulanan, 1, 2, 1, 1)
        self.gridLayout_bulanan.addWidget(self.annMSE_bulanan, 1, 3, 1, 1)
        self.gridLayout_bulanan.addWidget(self.annRsqr_bulanan, 1, 4, 1, 1)


        self.gridLayout_bulanan.addWidget(self.label_bulanan_2, 2, 0, 1, 1)
        self.gridLayout_bulanan.addWidget(self.label_29, 2, 1, 1, 1)
        self.gridLayout_bulanan.addWidget(self.tfTime_bulanan, 2, 2, 1, 1)
        self.gridLayout_bulanan.addWidget(self.tfMSE, 2, 3, 1, 1)
        self.gridLayout_bulanan.addWidget(self.tfRsqr, 2, 4, 1, 1)



        self.label_harian_no = QtWidgets.QLabel()
        self.label_harian_no.setObjectName("label_harian_no")

        self.label_harian_1 = QtWidgets.QLabel()
        self.label_harian_1.setObjectName("label_harian_1")

        self.label_harian_2 = QtWidgets.QLabel()
        self.label_harian_2.setObjectName("label_harian_2")

        self.label_time_harian = QtWidgets.QLabel()
        self.label_time_harian.setObjectName("label_time_harian")

        self.annTime_harian = QtWidgets.QLabel()
        self.annTime_harian.setObjectName("annTime_harian")

        self.wwoTime_harian = QtWidgets.QLabel()
        self.wwoTime_harian.setObjectName("wwoTime_harian")

        self.label_harian = QtWidgets.QLabel()
        self.label_harian.setFont(font)
        self.label_harian.setObjectName("label_harian")

        self.label_ann_harian = QtWidgets.QLabel()
        self.label_ann_harian.setObjectName("label_ann_harian")

        self.annMSE_harian = QtWidgets.QLabel()
        self.annMSE_harian.setObjectName("annMSE_harian")

        self.annRsqr_harian = QtWidgets.QLabel()
        self.annRsqr_harian.setObjectName("annRsqr_harianharian")

        self.label_wwo = QtWidgets.QLabel()
        self.label_wwo.setObjectName("label_wwo")

        self.wwoMSE = QtWidgets.QLabel()
        self.wwoMSE.setObjectName("wwoMSE")

        self.wwoRsqr = QtWidgets.QLabel()
        self.wwoRsqr.setObjectName("wwoRsqr")

        self.model_harian = QtWidgets.QLabel()
        self.model_harian.setObjectName("model_harian")

        self.mse_harian = QtWidgets.QLabel()
        self.mse_harian.setObjectName("mse_harian")

        self.rsqr_harian = QtWidgets.QLabel()
        self.rsqr_harian.setObjectName("rsqr_harian")

        self.gridLayout_harian = QtWidgets.QGridLayout()

        self.gridLayout_harian.addWidget(self.label_harian_no, 0, 0, 1, 1)
        self.gridLayout_harian.addWidget(self.model_harian, 0, 1, 1, 1)
        self.gridLayout_harian.addWidget(self.label_time_harian, 0, 2, 1, 1)
        self.gridLayout_harian.addWidget(self.mse_harian, 0, 3, 1, 1)
        self.gridLayout_harian.addWidget(self.rsqr_harian, 0, 4, 1, 1)

        self.gridLayout_harian.addWidget(self.label_harian_1, 1, 0, 1, 1)
        self.gridLayout_harian.addWidget(self.label_ann_harian, 1, 1, 1, 1)
        self.gridLayout_harian.addWidget(self.annTime_harian, 1, 2, 1, 1)
        self.gridLayout_harian.addWidget(self.annMSE_harian, 1, 3, 1, 1)
        self.gridLayout_harian.addWidget(self.annRsqr_harian, 1, 4, 1, 1)

        self.gridLayout_harian.addWidget(self.label_harian_2, 2, 0, 1, 1)
        self.gridLayout_harian.addWidget(self.label_wwo, 2, 1, 1, 1)
        self.gridLayout_harian.addWidget(self.wwoTime_harian, 2, 2, 1, 1)
        self.gridLayout_harian.addWidget(self.wwoMSE, 2, 3, 1, 1)
        self.gridLayout_harian.addWidget(self.wwoRsqr, 2, 4, 1, 1)

        # garis horizontal
        self.line_1 = QtWidgets.QFrame()
        self.line_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setObjectName("line_1")

        self.ConclusionVerticalLayout_ComparationTab = QtWidgets.QVBoxLayout()
        self.ConclusionVerticalLayout_ComparationTab.setAlignment(QtCore.Qt.AlignTop)
        self.ConclusionVerticalLayout_ComparationTab.setObjectName("ConclusionVerticalLayout_ComparationTab")
        self.ConclusionVerticalLayout_ComparationTab.addWidget(self.label_bulanan)
        self.ConclusionVerticalLayout_ComparationTab.addLayout(self.gridLayout_bulanan)
        self.ConclusionVerticalLayout_ComparationTab.addWidget(self.line_1)
        self.ConclusionVerticalLayout_ComparationTab.addWidget(self.label_harian)
        self.ConclusionVerticalLayout_ComparationTab.addLayout(self.gridLayout_harian)

        self.graphComparationTabGroupLayout = QtWidgets.QVBoxLayout()
        self.graphComparationTabGroupLayout.setObjectName("graphComparationTabGroupLayout")
        self.graphComparationTabGroupLayout.addWidget(self.labelGraph_ComparationTab)
        self.graphComparationTabGroupLayout.addWidget(self.graph_ComparationTab)

        self.packageForGraphComparationTabGroupLayout = QtWidgets.QWidget()
        self.packageForGraphComparationTabGroupLayout.setObjectName("packageForGraphComparationTabGroupLayout")
        self.packageForGraphComparationTabGroupLayout.setLayout(self.graphComparationTabGroupLayout)

        self.tableComparationTabGroupLayout = QtWidgets.QVBoxLayout()
        self.tableComparationTabGroupLayout.setObjectName("tableComparationTabGroupLayout")
        self.tableComparationTabGroupLayout.addWidget(self.labelTable_ComparationTab)
        self.tableComparationTabGroupLayout.addWidget(self.table_ComparationTab)

        self.packageForTableComparationTabGroupLayout = QtWidgets.QWidget()
        self.packageForTableComparationTabGroupLayout.setObjectName("packageForTableComparationTabGroupLayout")
        self.packageForTableComparationTabGroupLayout.setLayout(self.tableComparationTabGroupLayout)

        self.splitterGraphAndTable_ComparationTab = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitterGraphAndTable_ComparationTab.setObjectName("splitterGraphAndTable_ComparationTab")
        self.splitterGraphAndTable_ComparationTab.addWidget(self.packageForGraphComparationTabGroupLayout)
        self.splitterGraphAndTable_ComparationTab.addWidget(self.packageForTableComparationTabGroupLayout)

        self.packageConclution_ComparationTab = QtWidgets.QWidget()
        self.packageConclution_ComparationTab.setObjectName('packageConclution_ComparationTab')
        self.packageConclution_ComparationTab.setLayout(self.ConclusionVerticalLayout_ComparationTab)

        self.splitterHorizontal_ComparationTab = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitterHorizontal_ComparationTab.setObjectName("splitterHorizontal_ComparationTab")
        self.splitterHorizontal_ComparationTab.addWidget(self.packageConclution_ComparationTab)
        self.splitterHorizontal_ComparationTab.addWidget(self.splitterGraphAndTable_ComparationTab)

        self.verticalLayout_ComparationTab.addWidget(self.splitterHorizontal_ComparationTab)

        mainTabLayout.addTab(self.tab_5, "")
        self.retranslateUi(mainTabLayout)

    def setDeltaTimeDailyANN(self,value):
        self.annTime_harian.setText("{:.4f}".format(value))

    def setDeltaTimeMonthlyANN(self,value):
        self.annTime_bulanan.setText("{:.4f}".format(value))

    def setDeltaTimeTF(self,value):
        self.tfTime_bulanan.setText("{:.4f}".format(value))

    def setDeltaTimeWWO(self,value):
        self.wwoTime_harian.setText("{:.4f}".format(value))

    def resetAll(self):
        self.table_ComparationTab.clear()
        self.legendComparation.scene().removeItem(self.legendComparation)
        self.legendComparation = self.graph_ComparationTab.addLegend()
        for i in range(self.counterComparation, 0, -1):
            exec("self.graph_ComparationTab.removeItem(self.plotComparation" + str(i) + ")")
        self.counterComparation = 0

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and
                event.matches(QtGui.QKeySequence.Copy)):
            self.copySelection()
            return True
        return super(viewComparation, self).eventFilter(source, event)

    # add copy method
    def copySelection(self):
        selection = self.table_ComparationTab.selectedIndexes()
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

    def canvasComparation(self, data, info):
        self.counterComparation += 1
        pen = pg.mkPen(color=(self.rgb[self.counterComparation][0],
                              self.rgb[self.counterComparation][1],
                              self.rgb[self.counterComparation][2]),
                       width=2)
        y = data
        if info == "Thomas Fiering":
            exec("self.plotComparation" + str(self.counterComparation) + " = self.graph_ComparationTab.plot(y, pen=pen, name=info)")
        elif info == "Artificial Neural Network":
            exec("self.plotComparation" + str(self.counterComparation) + " = self.graph_ComparationTab.plot(y, pen=pen, name=info)")
        elif info == "Actual":
            exec("self.plotComparation" + str(self.counterComparation) + " = self.graph_ComparationTab.plot(y, pen=pen, name=info)")

    def showTableComparation(self, dataset):
        if len(dataset) == 4:
            table = np.c_[dataset[0], dataset[1], dataset[3]]
            columns = ["Date", "Actual", dataset[2]]
        else:
            table = np.c_[dataset[0], dataset[1], dataset[3], dataset[5]]
            columns = ["Date", "Actual", dataset[2], dataset[4]]

        self.table_ComparationTab.setRowCount(table.shape[0])
        self.table_ComparationTab.setColumnCount(table.shape[1])
        for i in range(table.shape[1]):
            self.table_ComparationTab.setHorizontalHeaderLabels(columns)
        for j in range(table.shape[0]):
            for i in range(table.shape[1]):
                self.table_ComparationTab.setItem(j, i, QTableWidgetItem(str(table[j, i])))

    def annMSE_bulanancomparation(self, value):
        self.annMSE_bulanan.setText(value)

    def tfMSEcomparation(self, value):
        self.tfMSE.setText(value)

    def annRsqr_bulanancomparation(self, value):
        self.annRsqr_bulanan.setText(value)

    def tfRsqrcomparation(self, value):
        self.tfRsqr.setText(value)



    def annMSE_hariancomparation(self, value):
        self.annMSE_harian.setText(value)

    def wwoMSEcomparation(self, value):
        self.wwoMSE.setText(value)

    def annRsqr_hariancomparation(self, value):
        self.annRsqr_harian.setText(value)

    def wwoRsqrcomparation(self, value):
        self.wwoRsqr.setText(value)


    def retranslateUi(self, mainTabLayout):
        _translate = QtCore.QCoreApplication.translate
        self.labelGraph_ComparationTab.setText(_translate("MainWindow", "Graph"))
        self.labelTable_ComparationTab.setText(_translate("MainWindow", "Table"))
        self.label_bulanan.setText(_translate("MainWindow", "Monthly"))
        self.label_28.setText(_translate("MainWindow", "ANN"))
        self.annMSE_bulanan.setText(_translate("MainWindow", ""))
        self.label_29.setText(_translate("MainWindow", "Thomas"))
        self.tfMSE.setText(_translate("MainWindow", ""))
        self.model_bulanan.setText(_translate("MainWindow", "Model"))
        self.mse_bulanan.setText(_translate("MainWindow", "MSE"))
        self.rsqr_bulanan.setText(_translate("MainWindow", "R-Squared"))

        self.label_bulanan_no.setText(_translate("MainWindow", "No."))
        self.label_bulanan_1.setText(_translate("MainWindow", "1."))
        self.label_bulanan_2.setText(_translate("MainWindow", "2."))

        self.label_time_bulanan.setText(_translate("MainWindow", "Time(s)"))
        self.annTime_bulanan.setText(_translate("MainWindow", ""))
        self.tfTime_bulanan.setText(_translate("MainWindow", ""))

        self.label_harian_no.setText(_translate("MainWindow", "No."))
        self.label_harian_1.setText(_translate("MainWindow", "1."))
        self.label_harian_2.setText(_translate("MainWindow", "2."))

        self.label_time_harian.setText(_translate("MainWindow", "Time(s)"))
        self.annTime_harian.setText(_translate("MainWindow", ""))
        self.wwoTime_harian.setText(_translate("MainWindow", ""))

        self.label_harian.setText(_translate("MainWindow", "Daily"))
        self.label_ann_harian.setText(_translate("MainWindow", "ANN"))
        self.annMSE_harian.setText(_translate("MainWindow", ""))
        self.label_wwo.setText(_translate("MainWindow", "WWO"))
        self.wwoMSE.setText(_translate("MainWindow", ""))
        self.model_harian.setText(_translate("MainWindow", "Model"))
        self.mse_harian.setText(_translate("MainWindow", "MSE"))
        self.rsqr_harian.setText(_translate("MainWindow", "R-Squared"))



        mainTabLayout.setTabText(mainTabLayout.indexOf(self.tab_5), _translate("MainWindow", "Comparation"))