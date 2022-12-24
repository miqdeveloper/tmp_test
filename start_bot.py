 
#from threading import Thread
from iqcapture import IQ_capture
from time import strftime
from buy_digital import buy_digital_action

A = buy_digital_action()
class main():
	def __init__(self):
		self.x_ = 0
		self.limit = 1
	def main_st(self):
		try:
				#if self.x_ < self.limit:
				while strftime("%S") == '50':
					print("Round martin --> ", self.x_)
					self.iq_ = IQ_capture()
					self.iq_.IQconnect()
					self.x_+=1
						#REseta martingale
		except Exception as error:
			print("Start.main_st -->", error)


i = main()
for rols in range(10):
	A.write("0")
	print("execuçao -> ", rols)
	i.main_st()


