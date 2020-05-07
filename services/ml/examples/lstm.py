import numpy as np
import pandas as pd
import datetime as dt
import os
import sys

## using CPU
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from keras.models import Sequential
from keras.layers import LSTM, Dense
import keras.backend.tensorflow_backend as K

import os

def lstm_model(look_back):
	
	'''
	Building model structure

	first layer - lstm layer : input shape is (-1, look_back, 1) 
	it means (batch size, look_back, 1). 
	You should reshape your data into 3D tensor before inference. 
	second layer - lstm layer : stacked lstm 
	last layer - Dense layer : fully connected layer. 
	output is scaler.

	'''
	model = Sequential()
	model.add(LSTM(16, return_sequences=True, input_shape=(look_back, 1)))
	model.add(LSTM(8))
	model.add(Dense(1))   
	return model

def load_weight(model, sensor_type):
	
	'''
	Loading model weights

	be careful.
	before loading weights, you should builing model structure using lstm_model(look_back) method.

	'''
	weights_file= os.getcwd() + "/ml/weight/lstm_" + sensor_type + ".h5" 
	model.load_weights(weights_file)
	return model

def compute_anomaly_score(dataX, datay, look_back, sensor_type):

	'''
	1. predicting LSTM model
	

	2. calculating error (anomaly score)
		anomaly socre = | y_pred - y_true | / 200

	return anomaly score and y_pred
	'''
	dataX = np.array(dataX)
	dataX = dataX / 200.
	dataX = dataX.reshape(-1, look_back, 1)

	model = lstm_model(look_back)
	model = load_weight(model, sensor_type = sensor_type)   #######

	y_pred = model.predict(dataX, batch_size=128, verbose=0)
	y_pred = y_pred * 200

	anomaly_score = abs(y_pred - datay) * 10 ## multiple 200 : to scaling 0 ~ 100

	return anomaly_score, y_pred

if __name__ == '__main__':
	if len(sys.argv) == 26:
		sensor_type_ = str(sys.argv[1])
		dataX = [float(i) for i in sys.argv[2:]]

		### -999, -995, -991 missing value 처리 
		dataX = pd.DataFrame(dataX)
		dataX[dataX <= -990] = pd.np.nan
			
		if dataX.isnull().all().values == True :  ## all values are nan
			print("score : ", 100.0, " y_pred : ", pd.np.nan)
			print("completed!")
		else :
			dataX = dataX.interpolate()
			dataX = dataX.bfill() 
			dataX = dataX.ffill() 
			dataX = np.array(dataX)
			datay = dataX[-1]

			anomaly_score, y_pred = compute_anomaly_score(dataX, datay, look_back=24, sensor_type = sensor_type_)
			
			if anomaly_score[0][0] >  50 :  
				fail_flag = 1
			else : 
				fail_flag =0

			print("score : ", anomaly_score[0][0], " y_pred : ", y_pred[0][0], " fail_flag : ", fail_flag)
			print("completed!")
	else :
		print("Error! Number of argv is not 26. ")