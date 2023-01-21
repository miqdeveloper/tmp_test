from iqoptionapi.stable_api import IQ_Option
import json



 #MODE: "PRACTICE"/"REAL"

class buy_digital_action():
	def __init__(self):
		#global duract
		#duract = 1
		with open("config/dates_config.json", "r") as file:
			self.read = json.loads(file.read())
			self.email = self.read['email']
			self.passwd = self.read['senha']
			self.account = self.read['account']
			file.close()


		with open('config/martin.json', 'r') as self.mart:
			self.js_ = self.mart.read()
			self.read_m = json.loads(self.js_)
			self.martingale = self.read_m['mart']
			#self.loss = self.read_m['loss']
			#SOma o loss para limitar o martingale
			#self.lose_soma = self.read_m['lose']
			#print(type(self.martingale))
			self.mart.close()

	def write(self, self_win):
		self.read_m["mart"] = self_win
		print(self.read_m)
		with open("config/martin.json", "w") as self.file:
			js_ = json.dump(self.read_m, self.file)
			return js_

	def call_buy_dig(self ,active, money, acti, duract):
		try:		
			self.iq = IQ_Option(self.email, self.passwd)
			self.status, self.ranson = self.iq.connect()
			if not self.status:
				print("Erro na conexão...")
				print("Tentando novamente...")
			if self.status:
				print("--> Realisando compra...")
				self.iq.change_balance(self.account)
				try:
					if self.martingale[0] == "-":
						self.money = float(self.martingale[1:]) * 2.3
						money = self.money
					else:
						pass
					self.iq_buy, self.id_buy = self.iq.buy_digital_spot(str(active), (money), str(acti), duract)
					self.status = self.iq_buy
					if self.status:
						while True:
							self.chack, self.win = self.iq.check_win_digital_v2(self.id_buy)
							if self.chack:
								break
						self.win = ('%0.2f' %self.win)
						print(self.win)
						if self.win[0] == '-':
							self.write(self.win)							
							print("Perdeu -->", self.win)							
						else:
							self.write(self.win)
							print("Ganhou -->", self.win)
				except Exception as error:
					print("Erro na compra...", error)
		except Exception as error:
			print("Error --> ", error)