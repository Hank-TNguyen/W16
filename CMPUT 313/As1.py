import random 

class Simulation:8

	def __init__(self): 
		# M (character): Indicates the error model used:  I for independent, B for Burst
		self.M = input("M\n").lower()

		# A (integer): You can assume the feedback time is 50 bit time units.
		self.A = int(input("A\n"))


		# K (integer):  The number of blocks. 
		# You should at least explore the range of values of K =0, 1, 2,10,40,100,400,1000.  
		# Note that your K should be chosen such that F is a multiple of K.
		self.K = int(input("K\n"))

		# F (integer)   The size of the frame in number of bits.   You can assume this is 4000 bits. 
		self.F = int(input("F\n"))

		# e (floating)  The probability that a bit is in error.  
		# You will vary this for e = 0.0001, 0.0003, 0.0005, 0.0007,  0.001.
		self.e = float(input("e\n"))

		# B burst length.  0 for the independent model.  
		# For the burst model, set this to 50 and 500 bit times.
		self.B = input("B\n")

		# N non-burst length.  0 for the independent model.  
		# For the burst model, set this to 5000 and 1000 bit times.
		if not (self.M == 'i'): 
			self.N = int(input("N\n"))
		else: 
			self.N = 0

		# R (integer)   The length of the simulation in bit time units.   
		# You must run this long enough to obtain stable results (for reasonable error rates).  
		# This should be run on the order of 5,000,000 bit time units.
		self.R = int(input("R\n"))

		# T  t1 t2 t3 ... tT (integer)   The number of trials, followed by seeds for the trials.  
		# For this simulation, you can set T to 5.
		self.T = input("T\n")
		self.T = self.T.split(' ')

	def run(self): 
		if self.M = 'b':
			for i in range(int(T[0]):
				self.run_burst(int(i+1))
				# run in burst mode
		else: 
			for i in range(int(T[0])):
				self.run_independent(int(i+1))
				# run in independent mode 

	def run_independent(self, seed):
		pass 

	def run_burst(self, seed):
		pass 