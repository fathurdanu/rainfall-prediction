# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:09:01 2019

@author: ASUS
"""
#import library
import numpy
#numpy.random.seed(1337)
import tensorflow as tf
#tf.set_random_seed(10)
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "3"

from numpy import std
from numpy import mean
import math
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from matplotlib import style
style.use("ggplot")


# dataset Curah Hujan, lama penyinaran rata-rata, kelembaban rata-rata, suhu rata-rata, dan kecepatan angin rata-rata
datasetX = pd.read_excel('D:\\rainfallData\dataANN17.xlsx', sep=',', header=0, index_col=False)
X = pd.DataFrame()
X['Tanggal'] = pd.to_datetime(datasetX['Tanggal'], format='%d-%m-%Y')
X['t-3'] = datasetX['t-3']
X['t-2'] = datasetX['t-2']
X['t-1'] = datasetX['t-1']
X['Suhu Rata-rata   (°C)'] = datasetX['Suhu Rata-rata   (°C)'].map('{:,.0f}'.format)
X['Kelembapan Rata-rata (%)'] = datasetX['Kelembapan Rata-rata (%)'].map('{:,.2f}'.format)
X['Lama Penyinaran Rata-rata (jam)'] = datasetX['Lama Penyinaran Rata-rata (jam)'].map('{:,.2f}'.format)
X['Kecepatan Angin Rata-rata (m/s)'] = datasetX['Kecepatan Angin Rata-rata (m/s)'].map('{:,.2f}'.format)
X.set_index(['Tanggal'], inplace=True)


#pembagian data training dan testing
train_size = int(len(X) * 0.69)
test_size = len(X) - train_size
trainX, testX = X[0:train_size], X[train_size:len(X)]
print(len(trainX), len(testX))

#dataset target
dataset = datasetX['target']
y = pd.DataFrame()
y['Target'] = dataset['t']
trainY, testY = dataset[0:train_size], dataset[train_size:len(dataset)]

#menghitung jumlah input dan output
X_input = X.shape[1]
y_output = y.shape[1]

#mengubah ke skala 0-1
scaler = MinMaxScaler(feature_range=(0, 1))
aktual = scaler.fit_transform(dataset)
all_real_data = scaler.fit_transform(X)
X_train_scaled = scaler.fit_transform(trainX)
X_test_scaled = scaler.fit_transform(testX)

#mengubah nilai nan ke menjani nol (0)
X_test_scaled = numpy.nan_to_num(X_test_scaled)

#mengubah ke skala 0-1
y_train_scaled = scaler.fit_transform(trainY)
y_test_scaled = scaler.fit_transform(testY)


#Arsitektur ANN 7-8-1
#Epoch 1000
model = Sequential()
model.add(Dense(X_input, input_dim=X_input))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adadelta')
history = model.fit(X_train_scaled, y_train_scaled, epochs=500, batch_size=2, verbose=2, shuffle=False)

# generate predictions for training
trainPredict = model.predict(X_train_scaled)
testPredict = model.predict(X_test_scaled)


#mengembalikan dari skala 0-1 ke skala normal
trainPredict_unscaled = scaler.inverse_transform(trainPredict)
testPredict_unscaled = scaler.inverse_transform(testPredict)

#penempatan data prediksi dari hasil training
trainPredictPlot = numpy.empty_like(datasetX)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[0:len(trainPredict), :] = trainPredict

#penempatan data prediksi dari hasil validasi/pengujian
testPredictPlot = numpy.empty_like(datasetX)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict):len(datasetX), :] = testPredict

#menyediakan keterangan tahun
bulanan = int(X.shape[0])
tm = []
for i in range(2008,2020):
    tm.append(i)
x_pos = range(6,X.shape[0],12)

#menampilkan grafik
plt.plot(aktual,'b')
plt.plot(trainPredictPlot,'g')
plt.plot(testPredictPlot,'r')
for i in range(1,bulanan):
    if i%12 == 0:
        plt.axvline(x=i,linestyle='dashed',color='grey')
plt.xticks(x_pos,tm)
plt.show()

#menggabungkan hasil data training dan data test ke dalam 1 variable (skala 0-1 maupun skala normal)
joined = numpy.concatenate((trainPredict, testPredict), axis=0).astype(numpy.float64)
joined_unscaled = numpy.concatenate((trainPredict_unscaled, testPredict_unscaled), axis=0).astype(numpy.float64)

#menduplikasi data hasil prediksi
prediksi = joined
prediksi_unscaled = joined_unscaled


#Penghitungan nilai error (MSE dan RMSE)
trainScore = model.evaluate(trainX, trainY, verbose=0)
print('Skala Normal')
print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
testScore = model.evaluate(testX, testY, verbose=0)
print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))
print('Skala 0-1')
trainScore = ((sum((X_train_scaled-trainPredict)**2))*1/train_size)[0]
print('Train Score: %.5f MSE (%.5f RMSE)' % (trainScore, math.sqrt(trainScore)))
testScore = ((sum((X_test_scaled-testPredict)**2))*1/test_size)[0]
print('Test Score: %.5f MSE (%.5f RMSE)' % (testScore, math.sqrt(testScore)))

#fungsi untuk mencari nilai a dan b pada regresi linier
def linearRegresion(data):
    #indeks[0] -> response variable -> x
	#indeks[1] -> predictor variable -> y
	x2=[]
	y2=[]
	xy=[]
	n = len(data[0])
	for x in data[0]:
		x2.append(x**2)
	for y in data[0]:
		y2.append(y**2)
	i=0;
	while(i<n):
		dump = data[0][i]*data[1][i]
		xy.append(dump)
		i+=1
	jmlhx = sum(data[0])
	jmlhy = sum(data[1])
	jmlhx2 = sum(x2)
	jmlhy2 = sum(y2)
	jmlhxy = sum(xy)
	a = ((jmlhy*jmlhx2)-(jmlhx*jmlhxy))/(n*jmlhx2-(jmlhx**2))
	b = ((n*jmlhxy)-(jmlhx*jmlhy))/(n*jmlhx2-(jmlhx**2))
	return(a,b)

#fungsi menampilkan nilai a dan b serta menampilkan grafik regresi linier
def gambarGrafik(dataProses):
	a,b = linearRegresion(dataProses)
	print("Nilai a : %.4f"%(a))
	print("Nilai b : %.4f"%(b))
	def f1(keanggotaan,a,b):
		hit = []
		for x in keanggotaan:
			y = b*x+a
			hit.append(y)
		return(hit)
	plt.scatter(dataProses[0],dataProses[1],label='data aktual',s=10)
	plt.plot(dataProses[0],f1(dataProses[0],a,b),c='k',label='hasil regresi',linewidth=0.5)
	plt.title("Hasil regresi Linear")
	plt.ylabel("y = b*x+a")
	plt.xlabel("Target")
	plt.legend()
	fig = plt.figure(1)
	fig.canvas.set_window_title("regresi linier")
	plt.show()

#pemanggilan fungsi untuk menampilkan grafik regresi linier
gambarGrafik([aktual,prediksi])

#mencari nilai error
pengurangan = abs(aktual-prediksi)
pengurangan_unscaled = abs(dataset.to_numpy()-prediksi_unscaled)

#deklarasi list
prediktor = []


aktual_unscaled = dataset['t'].to_numpy()
#menghilangkan nol pada nilai aktual supaya dapat berperan sebagai pembagi
for i in range(0,X.shape[0]):
    if aktual[i] == 0:
        aktual[i] = 1

for i in range(0,X.shape[0]):
    if aktual_unscaled[i] == 0:
        aktual_unscaled[i] = 1

#selisih nilai aktual dengan nilai prediksi (skala 0-1)
prediktor = ((pengurangan/aktual))*100
#selisih nilai aktual dengan nilai prediksi (skala normal)
prediktor_unscaled = numpy.transpose(numpy.transpose(pengurangan_unscaled)/aktual_unscaled)*100


#grafik prediktor (persentase selisih)
print('persen error = ', numpy.mean(prediktor_unscaled), '%')
plt.plot(prediktor_unscaled,'g')
plt.show()

#koefisien korelasi
coef_corelation = (sum(((aktual - mean(aktual)) * (joined - mean(joined)))))*1/(aktual.shape[0]-1)
coef_corelation = coef_corelation/(std(aktual)*std(joined))
print('koefisien korelasi = %.9f' % (coef_corelation[0]))
