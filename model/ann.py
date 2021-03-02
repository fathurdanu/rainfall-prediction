import warnings
with warnings.catch_warnings():
    from PyQt5.QtWidgets import QFileDialog, QWidget
    import pandas as pd
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    import keras
    from tensorflow.python.keras.models import Sequential
    from tensorflow.python.keras.layers import Dense
    from keras.initializers import RandomNormal
    from keras import backend as K
    import time
    from matplotlib import pyplot as plt
    from sklearn.preprocessing import PolynomialFeatures
    from scipy.stats.stats import pearsonr
    from sklearn.metrics import r2_score
    #from keras.constraints import maxnorm, min_max_norm
    #from keras.regularizers import l2,l1

#override abstract
class CustomCallback(keras.callbacks.Callback):
    def __init__(self, view, epo):
        global viewANN
        viewANN = view
        global epochs
        epochs = epo

    def on_epoch_end(self, epoch, logs=None):
        #keys = list(logs.values())
        #print("End epoch ", epoch)
        (epoch/epochs)*100
        global viewANN
        viewANN.progressTrainingBar(((epoch/epochs)*100)+1)


class ANN(QWidget):
    batch = 20

    # perintah pengambilan file pada tab ANN
    def openFileANN(self,popup):
        filename = QFileDialog.getOpenFileName(self,'Open File','./dataset','Spreadsheet(*.xlsx *.csv)')
        if filename[0] != '':
            if filename[0][-4:] == 'xlsx':
                tempDataset = pd.read_excel(filename[0])
            elif filename[0][-3:] == 'csv':
                tempDataset = pd.read_csv(filename[0])
            else:
                return None

            if (type(tempDataset.iloc[0][0]) is pd.Timestamp):
                datasetX = pd.DataFrame()
                datasetX[tempDataset.columns[0]] = tempDataset[tempDataset.columns[0]]
                #print(datasetX.iloc[5][0])
            elif (type(tempDataset.iloc[0][0]) is str) and (len(tempDataset.iloc[0][0]) >= 8 and len(tempDataset.iloc[0][0]) <= 10):
                datasetX = pd.DataFrame()
                datasetX[tempDataset.columns[0]] = pd.to_datetime(tempDataset[tempDataset.columns[0]],
                                                                  format='%d-%m-%Y')#.dt.strftime('%d-%m-%Y')
            else:
                popup.dateNotExistWarning()
                return None

            if type(tempDataset.iloc[0][1]) != str:
                for i in range(1, tempDataset.shape[1]):
                    datasetX[tempDataset.columns[i]] = tempDataset[tempDataset.columns[i]]#.map('{:,.2f}'.format)
                return datasetX
            else:
                popup.numericDatasetWarning()

    def timestampToStr(self, dataset):
        dataset[dataset.columns[0]] = dataset[dataset.columns[0]].dt.strftime('%d-%m-%Y')
        return dataset

    def dailyToMonthlyDataset(self, data):
        #print(dataset.columns[0])
        dataset = data[:]
        dataset[dataset.columns[0]] = pd.to_datetime(dataset[dataset.columns[0]])
        dataset.set_index(dataset.columns[0], inplace=True)
        rainfallTemp = dataset['precipMM'].resample('M').sum()
        dataset = dataset.resample('M').mean()
        dataset.drop(columns=['precipMM'], inplace=True)
        dataset['precipMM'] = rainfallTemp
        dataset.reset_index(inplace=True)
        return(dataset.round(2))

    # hitung nilai mse
    def getMSE(self, actual, predic):
        # rumus: mse = sum( (actual-predict)^2 ) / jumlah_data(n)

        error = []
        zip_object = zip(actual, predic)
        # error = (actual-predict)^2
        for actual_i, predic_i in zip_object:
            error.append((actual_i - predic_i) ** 2)

        # sum(error)/len(predic)
        return sum(error) / len(predic)
    """
    def splitUp(self, dataset):
        up = dataset[dataset[dataset.columns[0]].dt.year == dataset.iloc[0,0].year]
        down = dataset[dataset[dataset.columns[0]].dt.year != dataset.iloc[0,0].year]
        return up, down
    """

    def dataWeighting(self, data, targetColumn):
        coefCorr = data[data.columns].corr(method ='pearson')[targetColumn][:].drop(index=targetColumn)
        #print(coefCorr)
        listData = data.drop(targetColumn,axis=1).values.tolist()
        weightingData = [[0]*len(listData[0])]*len(listData)
        for i in range(len(weightingData)):
            for j in range(len(weightingData[0])):
                weightingData[i][j] = (listData[i][j] * coefCorr[j]) +listData[i][j]
        weightingData = pd.DataFrame(weightingData, columns=data.drop(targetColumn, axis=1).columns.values.tolist())
        weightingData.index = data.index
        weightingData[targetColumn] = data[targetColumn]
        return weightingData

    def dropVar(self, data, targetColumn):
        return data[data[["t-3","t-2","t-1",targetColumn]].columns]


    # hitung nilai R-Square
    def getRsquare(self, independent, dependent):
        # rumus: R-Square = sum( (rata-predict)^2 ) / sum( (aktual-predict)^2 )
        SS_res = sum(([(independent[i] - dependent[i]) ** 2 for i in range(len(independent))]))
        SS_tot = sum(([(independent[i] - (sum(independent) / len(independent))) ** 2 for i in range(len(independent))]))
        return 1 - SS_res / SS_tot

    def createRandom(self):
        initializer = RandomNormal(mean=0.034, stddev=0.039)
        return initializer

    def average(self, data):
        return sum(data)/len(data)

    def time_series(self,dataset,target):
        time_series = pd.DataFrame()
        time_series['t-3'] = dataset[target].shift(periods=3)
        time_series['t-2'] = dataset[target].shift(periods=2)
        time_series['t-1'] = dataset[target].shift(periods=1)
        dataset = pd.concat([dataset, time_series], axis=1, sort=False)
        return dataset

    def plot_history(self,history):
        axs = plt.subplot()
        #error
        axs.plot(history.history["loss"], label="train error")
        axs.plot(history.history["val_loss"], label="validation error")
        axs.set_ylabel("Error")
        axs.legend(loc="upper right")
        axs.set_title("Error eval")
        plt.show()

    # proses ann
    def processANN(self, X_train_scaled, X_test_scaled, targetTrainX_scaled, numOfParameterInput, selectedTarget0_And_optimizer1, numberOfHidLayer, output1_Activation, numOfHidNeuron, actHidLayer, epoch, view):
        model = Sequential()
        #initializer = self.createRandom() #bias + weight random
        initializer = keras.initializers.Constant(0.039)

        #susun arsitektur yang diinputkan
        for i in range(numberOfHidLayer):
            if (i==0):
                # input layer dan hidden layer pertama (gabungan)
                if actHidLayer[i] == "None":
                    model.add(Dense(numOfHidNeuron[i], input_dim=numOfParameterInput, kernel_initializer=initializer))
                else:
                    model.add(Dense(numOfHidNeuron[i], activation=actHidLayer[i], input_dim=numOfParameterInput, kernel_initializer=initializer))
            else:
                # hidden layer lanjutan
                if actHidLayer[i] == "None":
                    model.add(Dense(numOfHidNeuron[i], kernel_initializer=initializer))
                else:
                    model.add(Dense(numOfHidNeuron[i], activation=actHidLayer[i], kernel_initializer=initializer))

        #susun output layer sesuai input
        if output1_Activation == "None":
            model.add(Dense(1, kernel_initializer=initializer))
        else:
            model.add(Dense(1, activation=output1_Activation, kernel_initializer=initializer))

        model.compile(loss='mean_squared_error', optimizer=selectedTarget0_And_optimizer1[1], metrics=['accuracy'])


        start_time = time.time() #ambil waktu sebelum training

        #proses training
        history = model.fit(X_train_scaled, targetTrainX_scaled, validation_split=0.2, epochs=epoch, batch_size=self.batch, verbose=0, shuffle=False, callbacks=[CustomCallback(view, epoch)])

        end_time = time.time() #ambil waktu setelah training

        #proses testing
        trainPredict = model.predict(X_train_scaled) #hasil ann training (skala [0,1])
        testPredict = model.predict(X_test_scaled) #hasil ann dari data testing (skala [0,1])

        self.plot_history(history)
        #print(model.layers[0].get_weights()[0])
        #print(model.summary())

        return trainPredict, testPredict, history, model, end_time - start_time

    def predictingOnly(self,dataTest,model):
        testPredict = model.predict(dataTest)
        return(testPredict)

    def dataframeToNumpy(self, dataset) :
        return(dataset.to_numpy())

    def dataSplitTrainTestDaily(self, dataset):
        # data test merupakan dataset 1 tahun terakhir
        #print(dataset.tail(1).index[0].year)
        if int(dataset.tail(1).index[0].year) % 4 == 0:
            jmlHari = 366
        else :
            jmlHari = 365


        #jmlHari = 1460

        trainX = dataset.drop(dataset.tail(jmlHari).index[:], axis=0, inplace=False)
        testX = dataset.tail(jmlHari)
        splitedDataset = [trainX, testX]
        return (splitedDataset)

    def dataSplitTrainTestMonthly(self, dataset):
        #data test merupakan dataset 1 tahun terakhir
        #print(dataset)
        trainX = dataset.drop(dataset.tail(12).index[:], axis=0, inplace=False)
        testX = dataset.tail(12)
        splitedDataset = [trainX, testX]
        return(splitedDataset)

    def splitDataTarget(self, data, targetColumn):
        inputDatas = data.drop(targetColumn, axis=1, inplace = False)
        #print(inputDatas)
        target = data[targetColumn]
        return (inputDatas, target)

    def resetModel(self, model):
        session = K.get_session()
        for layer in model.layers:
            if isinstance(layer, Dense):
                old = layer.get_weights()
                layer.W.initializer.run(session=session)
                layer.b.initializer.run(session=session)
                #print(np.array_equal(old, layer.get_weights()), " after initializer run")
            else:
                print(layer, "not reinitialized")
        #print(model.summary())

    def printModel(self, model):
        print(model.layers)
        print()
        print(model.summary())