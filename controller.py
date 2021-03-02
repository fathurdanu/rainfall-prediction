import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    from PyQt5 import QtWidgets
    from view.main import main
    from view.viewann import viewAnn
    from view.viewcomparation import viewComparation
    from view.viewpopup import viewPopup
    import numpy as np
    import model.ann as ann
    import sys
    from sklearn.preprocessing import MinMaxScaler
    from tensorflow.keras.models import load_model
    import string

class controller:
    def __init__(self):
        # menghubungkan semua class yg diperlukan dengan controller
        self._app = QtWidgets.QApplication(sys.argv)
        self._MainWindow = QtWidgets.QMainWindow()
        self._MainWindow.show()
        self._ann = ann.ANN()
        #self._comparation = comparataion.Comparation()
        self._mainView = main()
        self._mainView.play(self._MainWindow)
        self._viewANN = viewAnn()
        self._viewANN.setupUi(self._MainWindow,self._mainView.centralwidget, self._mainView.mainTabLayout)
        self._viewComparation = viewComparation()
        self._viewComparation.setupUi(self._MainWindow, self._mainView.centralwidget, self._mainView.mainTabLayout)
        self._viewPopup = viewPopup()


        #panggil semua fungsi penerima sinyal
        self.saveModelSignal()
        self.openModelSignal()

        self.browseANNButtonSignal()
        self.resetANNButtonSignal()
        self.hidLayerANNspinBoxSignal()
        self.processANNButtonSignal()
        self.tempHidLayerSpinBox = 0
        self.comboboxChooseTargetSignal()
        self.predictingANNButtonSignal()
        self.newProjectSignal()
        self.radioButtonSignal()
        #self.printModelSignal()

        sys.exit(self._app.exec_())

        self.datasetVerticalDfANN = None



    '''-----------------------------------------------------------------------------------------------
    #menghubungkan sinya tombol di view dengan fungsi proses "menerima sinyal ketika tombol ditekan" 
    (Fungsi penerima sinyal)
    -----------------------------------------------------------------------------------------------'''
    def newProjectSignal(self):
        self._mainView.newProjectVerifysSignal.connect(self.newProject)

    def saveModelSignal(self):
        self._mainView.saveVerifysSignal.connect(self.saveKerasModel)

    def openModelSignal(self):
        self._mainView.openVerifysSignal.connect(self.openKerasModel)

    def predictingANNButtonSignal(self):
        self._viewANN.predictingANNVerifySignal.connect(self.predictingANNPressed)

    def hidLayerANNspinBoxSignal(self):
        self._viewANN.hidLayerSpinBoxANNvalueVerifySignal.connect(self.hidLayerANNvalueChanged)

    def browseANNButtonSignal(self):
        self._viewANN.browseANNverifySignal.connect(self.browseANNButtonPressed)

    def resetANNButtonSignal(self):
        self._viewANN.resetANNverifySignal.connect(self.resetANNButtonPressed)

    def processANNButtonSignal(self):
        self._viewANN.processANNVerifySignal.connect(self.processANNPressed)

    def comboboxChooseTargetSignal(self):
        self._viewANN.comboboxChooseTargetVerifySignal.connect(self.targetWasSelected)

    def radioButtonSignal(self):
        self._viewANN.radioVerifySignal.connect(self.radioPressed)

    #===============================================================================================

    '''-----------------------------------------------------------------------------------------------
    #perintah tombol ditekan (fungsi proses) : ANN
    -----------------------------------------------------------------------------------------------'''

    def radioPressed(self):
        self.radioDailyMonthly = self._viewANN.onRadioBtn().text()
        if 'datasetDailyVerticalBackup' in dir(self):
            if self.radioDailyMonthly == 'Daily':
                self.datasetVerticalDfANN = self.datasetDailyVerticalBackup[:]
                self.datasetVerticalDfANN.index = self.datasetDailyVerticalBackup.index
                #self.datasetVerticalDfANN.reset_index(inplace=True)
                self._viewANN.showTableANN(self._ann.timestampToStr(self.datasetVerticalDfANN.drop(['t-3','t-2','t-1'], axis=1)))
                self.setANNDataset(self.datasetVerticalDfANN)
                self._viewANN.setXgraphLegend('Day')
            elif self.radioDailyMonthly == 'Monthly':
                self.datasetVerticalDfANN = self._ann.dailyToMonthlyDataset(self.datasetDailyVerticalBackup)
                self._viewANN.showTableANN(self._ann.timestampToStr(self.datasetVerticalDfANN.drop(['t-3','t-2','t-1'], axis=1)))
                self.setANNDataset(self.datasetVerticalDfANN)
                self._viewANN.setXgraphLegend('Month')

    def setRadioButtonDailyTrue(self):
        self._viewANN.radioButton_daily.setChecked(True)
        self._viewANN.onRadioBtn().text()
        self.radioDailyMonthly = "Daily"

    def newProject(self):
        ans = self._viewPopup.confirmationBox()
        if ans == 16384: # if the answer is 'yes'
            global anyActual
            global tableANNandThomas

            self._viewANN.resetArchitecture()
            if 'datasetVerticalDfANN' in dir(self):
                self._viewANN.resetTable(self.datasetVerticalDfANN.columns)
                self._viewANN.resetGraph()
                self._viewComparation.annMSE_bulanancomparation("")
                self._viewComparation.annMSE_hariancomparation("")
                self._viewComparation.annRsqr_bulanancomparation("")
                self._viewComparation.annRsqr_hariancomparation("")

            if 'datasetVerticalDFTF' in dir(self):
                self._viewComparation.tfMSEcomparation("")
                self._viewComparation.tfRsqrcomparation("")

            self._viewComparation.resetAll()
            if "anyActual" in globals():
                del anyActual
            if "tableANNandThomas" in globals():
                del tableANNandThomas
            if "datasetDailyVerticalBackup" in dir(self):
                del self.datasetDailyVerticalBackup

    def predictingANNPressed(self):
        global tableANNandThomas
        global kerasModel

        popup = 0
        dailyOrMonthly = 0

        if (self._viewANN.comboboxChooseTarget.currentText() == 'None'):
            popup = 1
        elif self._viewANN.radioButton_daily.isChecked():
            dailyOrMonthly = 1
        elif self._viewANN.radioButton_monthly.isChecked():
            dailyOrMonthly = 2
        elif dailyOrMonthly == 0:
            popup = 2

        if popup == 0:

            self.datasetVerticalIndexedANN = self.datasetVerticalDfANN.set_index([self.datasetVerticalDfANN.columns[0]],
                                                                                 inplace=False)
            # spliting data target
            # splitDataTarget index 0 -> parameter
            # splitDataTarget index 1 -> target
            temp = self._ann.splitDataTarget(self.datasetVerticalIndexedANN,
                                             self._viewANN.comboboxChooseTarget.currentText())
            dataX = temp[0]
            targetX = temp[1]

            # spliting data input training & testing
            # dataSplitTrainTest index 0 -> data training
            # dataSplitTrainTest index 1 -> data testing
            if dailyOrMonthly == 1:
                temp = self._ann.dataSplitTrainTestDaily(dataX)
            elif dailyOrMonthly == 2:
                temp = self._ann.dataSplitTrainTestMonthly(dataX)
            trainX = temp[0]
            testX = temp[1]


            # spliting target training & testing
            # dataSplitTrainTest index 0 -> target training
            # dataSplitTrainTest index 1 -> data aktual 1 tahun terakhir (validation)
            if dailyOrMonthly == 1:
                temp = self._ann.dataSplitTrainTestDaily(targetX)
            elif dailyOrMonthly == 2:
                temp = self._ann.dataSplitTrainTestMonthly(targetX)
            targetTrainX = temp[0].to_frame()
            actualTest = temp[1].to_frame()

            # mengubah ke skala [0,1]
            scaler = MinMaxScaler(feature_range=(0, 1))
            X_train_scaled = scaler.fit_transform(trainX)
            X_test_scaled = scaler.fit_transform(testX)
            targetTrainX_scaled = scaler.fit_transform(targetTrainX)
            actual_scaled = scaler.fit_transform(actualTest)


            testPredict = self._ann.predictingOnly(X_test_scaled,kerasModel)
            testPredict_unscaled = scaler.inverse_transform(testPredict)

            # penempatan data prediksi dari hasil validasi/pengujian
            testPredictPlot = np.empty_like(dataX.iloc[:, 0])
            testPredictPlot[:] = np.nan
            testPredictPlot[len(trainX):len(dataX)] = testPredict_unscaled[:, 0]

            # kirim ke view (Graph)
            self._viewANN.canvasANN(testPredictPlot, 'Testing')
            if "anyActual" not in globals():
                global anyActual
                anyActual = True
                self._viewANN.canvasANNtestingTab(temp[1].to_numpy().astype(np.float), "Actual")
                self._viewComparation.canvasComparation(temp[1].to_numpy().astype(np.float), "Actual")
            self._viewANN.canvasANNtestingTab(testPredict_unscaled[:, 0], "Testing Result")

            self._viewComparation.canvasComparation(testPredict_unscaled[:, 0], 'Artificial Neural Network')

            # persiapan data untuk Tabel
            dateTesting = testX.index.tolist()


            tableTesting = np.c_[dateTesting, actualTest.values.tolist(), testPredict_unscaled[:, 0].tolist()]

            # kirim ke view (tabel)
            self._viewANN.showTableTestingANN(tableTesting)

            # nilai mse testing
            self.annmse = self._ann.getMSE([float(i) for i in temp[1]],
                                           testPredict_unscaled[:, 0].tolist())  # skala normal
            # self.annmse = self._ann.getMSE([float(i) for i in actual_scaled], testPredict[:, 0].tolist())  # skala [0,1]

            # nilai r-square testing
            self.annRsqr = self._ann.getRsquare([float(i) for i in temp[1]],
                                                testPredict_unscaled[:, 0].tolist())  # skala normal
            # self.annRsqr = self._ann.getRsquare([float(i) for i in actual_scaled], testPredict[:, 0].tolist())  # skala [0,1]


            # harian
            if dailyOrMonthly == 1:
                # float 2 digit di belakang koma
                # self._viewComparation.annMSE_hariancomparation("{:.2f}".format(self.annmse))
                # self._viewComparation.annRsqr_hariancomparation("{:.2f}".format(self.annRsqr))

                # float nilai asli
                self._viewComparation.annMSE_hariancomparation("{:.5f}".format(self.annmse))
                self._viewComparation.annRsqr_hariancomparation("{:.5f}".format(self.annRsqr))

            # bulanan
            elif dailyOrMonthly == 2:
                # float 2 digit di belakang koma
                # self._viewComparation.annMSE_bulanancomparation("{:.2f}".format(self.annmse))
                # self._viewComparation.annRsqr_bulanancomparation("{:.2f}".format(self.annRsqr))

                # float nilai asli
                self._viewComparation.annMSE_bulanancomparation("{:.5f}".format(self.annmse))
                self._viewComparation.annRsqr_bulanancomparation("{:.5f}".format(self.annRsqr))


    def saveKerasModel(self):
        global kerasModel
        self._mainView.saveModel(kerasModel)
        #self._mainView.saveModel()

    def openKerasModel(self):
        global kerasModel
        filename = self._mainView.openModel()
        print(filename)
        if filename != '':
            kerasModel = load_model(filename)
            temp = []
            #print(kerasModel.summary())
            kerasModel.summary(print_fn=lambda x: temp.append(''.join([word for word in x if word not in string.punctuation])))
            temp = list(map(lambda x: x.split(), temp))
            temp = temp[4:-5]
            temp = [i for i in temp if i]
            temp2 = []
            #print(temp,temp2)
            for i in range(len(temp)):
                temp2.append(kerasModel.layers[i].get_config()["activation"])
            self._viewANN.setOpenArchitecture(temp,temp2)

    #ambil dataset dari model ANN
    def setANNDataset(self, dataset):
        self.datasetVerticalIndexedANN = dataset.set_index([dataset.columns[0]],
                                                                             inplace=False)
    #split data input dengan data target
    def setDataInputAndDataTarget(self):
        # spliting data target
        # splitDataTarget index 0 -> parameter
        # splitDataTarget index 1 -> target
        temp = self._ann.splitDataTarget(self.datasetVerticalIndexedANN, self._viewANN.comboboxChooseTarget.currentText())
        self.dataX = temp[0]
        self.targetX = temp[1]

    #Ketika jumlah hidden layer berubah
    def hidLayerANNvalueChanged(self):
        self._viewANN.changeTheHidLayer(self._viewANN.numOfHiddenLayer.value(), self.tempHidLayerSpinBox)
        self.tempHidLayerSpinBox = self._viewANN.numOfHiddenLayer.value()

    #Ketika tombol browse ANN ditekan
    def browseANNButtonPressed(self):
        temporaryDataset = self._ann.openFileANN(self._viewPopup)
        if temporaryDataset is not None:
            if temporaryDataset.shape[1] < 3:
                self._viewPopup.ANNdatasetColumnsWarning()
            else:
                self.datasetVerticalDfANN = temporaryDataset[list(temporaryDataset.columns)]
                self.datasetDailyVerticalBackup = temporaryDataset[list(temporaryDataset.columns)]
                self._viewANN.showTableANN(self._ann.timestampToStr(self.datasetVerticalDfANN.drop(['t-3','t-2','t-1'], axis=1)))
                #self._viewANN.showTableANN(self._ann.timestampToStr(self.datasetVerticalDfANN))
                self.setRadioButtonDailyTrue()
                self._viewANN.setXgraphLegend('Day')
                self._viewANN.showChooseTargetList(self.datasetVerticalDfANN.columns[1:])
                self.setANNDataset(self.datasetVerticalDfANN)

    #Ketika tombol reset ANN ditekan
    def resetANNButtonPressed(self):

        self._viewANN.resetArchitecture()
        if 'datasetVerticalDfANN' in dir(self):
            self._viewANN.resetTable(self.datasetVerticalDfANN.columns)
            self._viewANN.resetGraph()

    #Ketika tombol train + testing ANN ditekan
    def processANNPressed(self):
        #buat notifikasi + prasyarat pemilihan bulanan atau harian
        popup = 0
        dailyOrMonthly = 0
        if (self._viewANN.comboboxChooseTarget.currentText() == 'None'):
            popup = 1
        elif self._viewANN.radioButton_daily.isChecked():
            dailyOrMonthly = 1
        elif self._viewANN.radioButton_monthly.isChecked():
            dailyOrMonthly = 2
        elif dailyOrMonthly == 0:
            popup = 2

        #ketika tidak ada masalah
        if popup == 0:
            global tableANNandThomas

            #mengubah date menjadi index (date tidak menjadi parameter input)
            self.datasetVerticalIndexedANN = self.datasetVerticalDfANN.set_index([self.datasetVerticalDfANN.columns[0]],
                                                                                 inplace=False)

            #Pembobotan
            #self.datasetVerticalIndexedANN = self._ann.dataWeighting(self.datasetVerticalIndexedANN, self._viewANN.comboboxChooseTarget.currentText())

            # spliting data target
            # splitDataTarget index 0 -> parameter
            # splitDataTarget index 1 -> target
            temp = self._ann.splitDataTarget(self.datasetVerticalIndexedANN,
                                             self._viewANN.comboboxChooseTarget.currentText())
            dataX = temp[0] # data parameter input
            targetX = temp[1] # data target


            # spliting data training & testing data parameter input
            # dataSplitTrainTest index 0 -> data parameter input training
            # dataSplitTrainTest index 1 -> data parameter input testing
            if dailyOrMonthly == 1: #harian
                temp = self._ann.dataSplitTrainTestDaily(dataX)
            elif dailyOrMonthly == 2: #bulanan
                temp = self._ann.dataSplitTrainTestMonthly(dataX)
            trainX = temp[0]
            testX = temp[1]

            # spliting target training & testing khusus data target
            # dataSplitTrainTest index 0 -> target training
            # dataSplitTrainTest index 1 -> data aktual 1 tahun terakhir (validation)
            if dailyOrMonthly == 1: #harian
                temp = self._ann.dataSplitTrainTestDaily(targetX)
            elif dailyOrMonthly == 2: #bulanan
                temp = self._ann.dataSplitTrainTestMonthly(targetX)

            #konversi series ke Dataframe
            targetTrainX = temp[0].to_frame()
            actualTest = temp[1].to_frame()

            # menghitung jumlah parameter input dan output
            numOfParameterInput = dataX.shape[1] #jumlah input
            # numberOfOutput = targetTrainX.shape[1] #jumlah output

            # mengubah ke skala 0-1 dengan minmaxscaler
            scaler = MinMaxScaler(feature_range=(0, 1))
            X_train_scaled = scaler.fit_transform(trainX)
            X_test_scaled = scaler.fit_transform(testX)
            targetTrainX_scaled = scaler.fit_transform(targetTrainX)
            actual_scaled = scaler.fit_transform(actualTest)
            print(X_train_scaled[0])
            #X_train_scaled = trainX.to_numpy()
            #X_test_scaled = testX.to_numpy()
            #targetTrainX_scaled = targetTrainX.to_numpy()

            #ambil arsitektur dari view yang telah diinputkan
            selectedTarget0_And_optimizer1 = [self._viewANN.comboboxChooseTarget.currentText(),
                                              self._viewANN.optimizerBox.currentText()]
            numberOfHidLayer = self._viewANN.numOfHiddenLayer.value()
            output1_Activation = self._viewANN.actOutputLayerBox.currentText()
            epoch = self._viewANN.spinBoxEpoch.value()

            # ambil arsitektur dari view (hidden neuron dan fungsi aktivasinya) yang telah diinputkan
            numOfHidNeuron = []
            actHidLayer = []
            for i in range(numberOfHidLayer):
                exec("numOfHidNeuron.append(self._viewANN.spinBoxLayerNum_" + str(i) + ".value())")
                exec("actHidLayer.append(self._viewANN.actHidLayerBoxLayerNum_" + str(i) + ".currentText())")
                # print('loop = '+ str(i))

            #proses ANN training dan testing
            trainPredict0_testPredict1_history2_model3_time4 = self._ann.processANN(
                X_train_scaled, X_test_scaled, targetTrainX_scaled, numOfParameterInput, selectedTarget0_And_optimizer1,
                numberOfHidLayer, output1_Activation, numOfHidNeuron, actHidLayer, epoch, self._viewANN)


            #set progres bar ke nol lagi
            self._viewANN.progressTrainingBar(0)
            #popout "proses training selesai"
            self._viewPopup.ANNtrainingComplete()

            #memindahkan model ke variable global
            global kerasModel
            kerasModel = trainPredict0_testPredict1_history2_model3_time4[3]
            self._mainView.actionSave.setDisabled(False) #unlock fitur save model

            #pindahin hasil prediksi ke variable baru
            trainPredict = trainPredict0_testPredict1_history2_model3_time4[0]
            testPredict = trainPredict0_testPredict1_history2_model3_time4[1]

            #pindahin hasil prediksi ke variable baru + post processing (balikin ke skala normal)
            trainPredict_unscaled = scaler.inverse_transform(trainPredict0_testPredict1_history2_model3_time4[0])
            testPredict_unscaled = scaler.inverse_transform(trainPredict0_testPredict1_history2_model3_time4[1])
            #trainPredict_unscaled = trainPredict0_testPredict1_history2_model3_time4[0]
            #testPredict_unscaled = trainPredict0_testPredict1_history2_model3_time4[1]

            # penempatan data prediksi dari hasil training
            trainPredictPlot = np.empty_like(dataX.iloc[:, 0])
            trainPredictPlot[:] = np.nan
            trainPredictPlot[0:len(trainPredict_unscaled)] = trainPredict_unscaled[:, 0]

            # penempatan data prediksi dari hasil validasi/pengujian
            testPredictPlot = np.empty_like(dataX.iloc[:, 0])
            testPredictPlot[:] = np.nan
            testPredictPlot[len(trainPredict_unscaled):len(dataX)] = testPredict_unscaled[:, 0]

            # kirim ke view (Graph)
            self._viewANN.canvasANN(trainPredictPlot, 'Training')
            self._viewANN.canvasANN(testPredictPlot, 'Testing')
            if "anyActual" not in globals():
                global anyActual
                anyActual = True
                self._viewANN.canvasANNtrainingTab(temp[0].to_numpy().astype(np.float), "Actual")
                self._viewANN.canvasANNtestingTab(temp[1].to_numpy().astype(np.float), "Actual")
                self._viewComparation.canvasComparation(temp[1].to_numpy().astype(np.float), "Actual")
            self._viewANN.canvasANNtrainingTab(trainPredictPlot, "Training Result")
            self._viewANN.canvasANNtestingTab(testPredict_unscaled[:, 0], "Testing Result")

            self._viewComparation.canvasComparation(testPredict_unscaled[:, 0], 'Artificial Neural Network')
            # self._viewANN.canvasANNtestingTab(trainPredict0_testPredict1_history2_model3_time4[2].history['loss'],"loss")

            #weights = self.kerasModel.layers[0].get_weights()[0]
            # weights = (weights[:].tolist())
            #biases = self.kerasModel.layers[0].get_weights()[1]
            # biases = (biases[:].tolist())

            # memindahkan nilai index ke list (persiapan data untuk Tabel)
            dateTraining = trainX.index.tolist()
            dateTesting = testX.index.tolist()

            if "tableANNandThomas" not in globals():
                tableANNandThomas = []

            if not tableANNandThomas:
                tableANNandThomas.append(dateTesting)
                tableANNandThomas.append(actualTest.values.tolist())
            tableANNandThomas.append('ANN')
            tableANNandThomas.append(testPredict_unscaled[:, 0].tolist())

            #persiapan kolom apa saja yang akan ditampilkan dalam tabel training dan testing
            tableTraining = np.c_[dateTraining, targetTrainX.values.tolist(), trainPredict_unscaled[:, 0].tolist()]
            tableTesting = np.c_[dateTesting, actualTest.values.tolist(), testPredict_unscaled[:, 0].tolist()]

            # kirim ke view (tabel)
            self._viewANN.showTableTrainingANN(tableTraining)
            self._viewANN.showTableTestingANN(tableTesting)
            self._viewComparation.showTableComparation(tableANNandThomas)

            # nilai mse testing
            #self.annmse = self._ann.getMSE([float(i) for i in temp[1]], testPredict_unscaled[:, 0].tolist()) #skala normal
            self.annmse = self._ann.getMSE([float(i) for i in actual_scaled], testPredict[:, 0].tolist())  # skala [0,1]

            # nilai r-square testing
            #self.annRsqr = self._ann.getRsquare([float(i) for i in temp[1]], testPredict_unscaled[:, 0].tolist()) #skala normal
            self.annRsqr = self._ann.getRsquare([float(i) for i in actual_scaled], testPredict[:, 0].tolist())  # skala [0,1]
            print(self.annmse,self.annRsqr)
            self.annTime = trainPredict0_testPredict1_history2_model3_time4[4]

            #harian
            if dailyOrMonthly == 1:
                #menampilkan float 2 digit di belakang koma
                #self._viewComparation.annMSE_hariancomparation("{:.2f}".format(self.annmse))
                #self._viewComparation.annRsqr_hariancomparation("{:.2f}".format(self.annRsqr))

                # menampilkan float 5 digit di belakang koma
                self._viewComparation.annMSE_hariancomparation("{:.5f}".format(self.annmse))
                self._viewComparation.annRsqr_hariancomparation("{:.5f}".format(self.annRsqr))

                #time sekon
                self._viewComparation.setDeltaTimeDailyANN(self.annTime)
            #bulanan
            elif dailyOrMonthly == 2:
                #menampilkan float 2 digit di belakang koma
                #self._viewComparation.annMSE_bulanancomparation("{:.2f}".format(self.annmse))
                #self._viewComparation.annRsqr_bulanancomparation("{:.2f}".format(self.annRsqr))

                #menampilkan float 5 digit di belakang koma
                self._viewComparation.annMSE_bulanancomparation("{:.5f}".format(self.annmse))
                self._viewComparation.annRsqr_bulanancomparation("{:.5f}".format(self.annRsqr))

                #time sekon
                self._viewComparation.setDeltaTimeMonthlyANN(self.annTime)

        #ketika radio button harian bulanan belum terpilih
        elif popup == 2:
            self._viewPopup.ANNselectDailyMonthlyWarning()
        #ketika combobox target belum dipilih
        elif popup == 1:
            self._viewPopup.ANNselectTargetWarning()

    #Ketika target dataset dipilih melalui combobox
    def targetWasSelected(self):
        if(self._viewANN.comboboxChooseTarget.currentText() != 'None'):
            #new_data = self._ann.time_series(self.datasetVerticalIndexedANN, self._viewANN.comboboxChooseTarget.currentText())
            self.setDataInputAndDataTarget()
            self._viewANN.canvasANN(self.targetX.to_numpy().astype(np.float), 'Actual')
            self._viewANN.setYgraphANN(self._viewANN.comboboxChooseTarget.currentText())

#main program (mengaktifkan controller)
if __name__ == '__main__':
    c = controller()
    sys.exit(c.exec_())



