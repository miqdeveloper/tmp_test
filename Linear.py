from buy_digital import buy_digital_action
from multiprocess import Process 
import pandas as pd
import json
from joblib import dump, load
from time import strftime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import *
from sklearn.metrics import r2_score, mean_squared_error
import time, os
import numpy as np
#from buy import buy
from iqoptionapi.stable_api import IQ_Option
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from tensorflow import keras 
from keras.optimizers import Adam




class reg_linear():
	def __init__(self):
		#import start_bot
		 
		#self.contador = start_bot.main()	
		self.buy_d = buy_digital_action()

		with open("config/program_config.json", "r") as arch:
			self.j = json.loads(arch.read())
			self.ativo = str(self.j['ativo'])
			self.money = int(self.j['money'])
			self.time = int(self.j['time'])
			self.call = str(self.j['call'])
			self.put = str(self.j['put'])




	def calc_reg(self):
		#time.sleep(timer) # Resultado para cada 59 segundos. Altere se quiser
		try:
			df = pd.read_csv("iqdataset.csv", delimiter=';')
			timestamps = df['timestamp'].values
			kcloses = df['kclose'].values
			KCLOSE = kcloses[-1]
			print("Const KCLOSE:", KCLOSE)
			scaler = MinMaxScaler()
			kcloses = scaler.fit_transform(kcloses.reshape(-1, 1))
			# Divida os dados em conjuntos de treinamento e teste
			train, test = (train_test_split(kcloses, train_size=0.96))
			# Converta os conjuntos de treinamento e teste em arrays para serem usados pelo modelo
			train = np.array(train)
			test = np.array(test)
			train_target = np.array(train)
			# Crie o modelo LSTM
			
			model = Sequential()
			model.add(LSTM(210, input_shape=(train.shape[0], 1)))
			model.add(Dropout(0.4))
			model.add(Dense(15, activation='relu'))
			model.add(Dense(5, activation="softmax"))
			model.add(Dense(3))
			model.add(Dense(1))
			opt = Adam(learning_rate=(0.0001))
			model.compile(loss='mean_squared_error', optimizer=opt)
			model.fit(train, train_target, epochs=100, batch_size=1, verbose=2)
			# Faça previsões com o conjunto de teste
			predictions = model.predict(test)
			# Desfaça a normalização dos dados para obter os valores reais
			predictions = scaler.inverse_transform(predictions)
			score = np.sqrt(mean_squared_error(test[:, 0], predictions[:, 0]))
			#print( "%.3f," %predictions[-1])
			#print("%.3f" %test[-1])
			print("score: %.2f" %score)
			print("valor df kclose 0:", KCLOSE)
			print("valor previsto:", predictions[1])
			if(predictions[-1] > KCLOSE):
				Process(target=self.buy_d.call_buy_dig, args=(self.ativo, self.money, self.call, self.time)).start()
				return score, predictions[-1], "Up"
			elif(predictions[-1] < KCLOSE):
				Process(target=self.buy_d.call_buy_dig, args=(self.ativo, self.money, self.put, self.time)).start()
				return score, predictions[-1], "Down"

			os.remove("iqdataset.csv")
		except Exception as e:
			print("Error: %s" % str(e))
