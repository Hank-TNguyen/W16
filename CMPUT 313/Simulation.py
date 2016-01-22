import random 
import math 
import statistics
import csv

class Simulation:
	
	def __init__(self): 
		# M (character): Indicates the error model used:  I for independent, B for Burst
		self.M = input().lower()
		
		# A (integer): You can assume the feedback time is 50 bit time units.
		self.A = int(input())

		# K (integer):  The number of blocks. 
		# You should at least explore the range of values of K =0, 1, 2,10,40,100,400,1000.  
		# Note that your K should be chosen such that F is a multiple of K.
		self.K = int(input())

		# F (integer)   The size of the frame in number of bits.   You can assume this is 4000 bits. 
		self.F = int(input())

		# e (floating)  The probability that a bit is in error.  
		# You will vary this for e = 0.0001, 0.0003, 0.0005, 0.0007,  0.001.
		self.e = float(input())

		# B burst length.  0 for the independent model.  
		# For the burst model, set this to 50 and 500 bit times.
		# N non-burst length.  0 for the independent model.  
		# For the burst model, set this to 5000 and 1000 bit times.
		self.N = int(input())
		self.B = int(input())

		# R (integer)   The length of the simulation in bit time units.   
		# You must run this long enough to obtain stable results (for reasonable error rates).  
		# This should be run on the order of 5,000,000 bit time units.
		self.R = int(input())

		# T  t1 t2 t3 ... tT (integer)   The number of trials, followed by seeds for the trials.  
		# For this simulation, you can set T to 5.
		self.T = input()
		self.T = self.T.split(' ')
		self.process_arguments()

	def process_arguments(self):
		
		if self.K:

			self.HSBC = 1
			# r bits for HSBC
			r = math.ceil(math.log2(self.F/self.K))
			if (math.pow(2,r) < self.F/self.K + r + 1): 
				r += 1
			self.r = r 

			# calculate block and frame size accordingly 
			self.block_size = int(self.F / self.K + self.r)
			self.frame_size = int(self.block_size * self.K)
		else: 
			# HSBC is not in use
			self.HSBC = 0
			self.block_size = 0
			self.frame_size = self.F

		# initialize runtime
		self.run_time = 0

		# error rate in burst mode 
		# e' = e * (N + B) / B
		if self.M == 'b':
			self.e_burst = self.e * (self.N + self.B) / self.B

		print("\nSIMULATION STARTS\n")
		print(self.M)
		print(self.A)
		print(self.K)
		print(self.F)
		print(self.e)
		print(self.N)
		print(self.B)
		print(self.R)
		print(self.T)

		# print(self.block_size)
		# print(self.frame_size)

	def run(self): 

		sum_t_frame, sum_r_frame = list(), list()
		if self.M == 'b':
			# run in burst mode
			for i in range(int(self.T[0])):
				random.seed(int(self.T[i+1]))
				t_frame, r_frame = self.run_burst(self.HSBC)

				# reset run_time for next trial
				self.run_time = 0 
				sum_t_frame.append(t_frame)
				sum_r_frame.append(r_frame)
				
		else: 
			# run in independent mode 
			# print('run ' + str(self.T) + ' trials') 
			for i in range(int(self.T[0])):
				random.seed(int(self.T[i+1]))
				t_frame, r_frame = self.run_independent(self.HSBC)

				# reset run_time for next trial
				self.run_time = 0 
				sum_t_frame.append(t_frame)
				sum_r_frame.append(r_frame)

		a, b, c, d, e, f = self.process_result(sum_t_frame,sum_r_frame)
		self.print_result(a, b, c, d, e, f)
		
		self.writeResults('output_data.csv', [self.M, self.N, self.B, self.K, self.e , a,b,c,d,e,f])

	def process_result(self, t_frame, r_frame):
		print(t_frame, r_frame) 
		
		try:
			stat_const = float(2.776)

			res2 = [] # frame transmission 
			res3 = [] # throughput 
			for i in range(int(self.T[0])):
				# frame transmission
				res2.append(t_frame[i]/r_frame[i])
				res3.append(self.F * r_frame[i] / self.R)

			# print(res2, res3)

			avg_res2 = statistics.mean(res2)
			sd2 = statistics.stdev(res2)
			dif2 = sd2/math.sqrt(int(self.T[0]))*stat_const
			upper_bound2 = avg_res2 + dif2 
			lower_bound2 = avg_res2 - dif2 

			avg_res3 = statistics.mean(res3)
			sd3 = statistics.stdev(res3)
			dif3 = sd3/math.sqrt(int(self.T[0]))*stat_const
			upper_bound3 = avg_res3 + dif3
			lower_bound3 = avg_res3 - dif3 

		except ZeroDivisionError: 
			return float("inf"), float("inf"), float("inf"), 0, 0, 0

		return avg_res2, lower_bound2, upper_bound2, avg_res3, lower_bound3, upper_bound3 
		
	def print_result(self, a,b,c,d,e,f):
		print("\nRESULTS\n")
		print("Frame transmission")
		print(a,b,c)
		print("Throughput")
		print(d,e,f)
		print("\nSIMULATION ENDS\n\n")
		return 			

	def run_independent(self, HSBC):
		total_frame = 0
		received_frame = 0 
		
		while self.R > self.run_time: 
			# print(self.R, self.run_time)
			# time taken to send one frame
			self.send_frame()
			self.acknowledgement() 
			total_frame += 1 

			# receiver processing message
			send_fail = 0 
			if self.K:
				for i in range(self.K): 
					errors = self.bit_error_in_message(self.block_size, self.e)
					if errors > HSBC:

						send_fail = 1
						break
			else: 
				for i in range(self.frame_size): 
					errors = self.bit_error(self.e)
					if errors:		
						send_fail = 1 
						break 

			if not send_fail:
				
				received_frame += 1 

		# self.print_result(total_frame, received_frame)
		return total_frame, received_frame
	
	def run_burst(self, HSBC):
		total_frame = 0 
		received_frame = 0 

		while self.R > self.run_time: 
			# print(self.R, self.run_time)
			# keep track of cur_time to determine burst period
			cur_time = self.run_time 

			# time taken to send one frame
			self.send_frame()
			self.acknowledgement() 
			total_frame += 1 			
			
			# processing a frame
			send_fail = 0
			if self.K: 
				for i in range(self.K):
					# use HSBC upon each block  
					errors = 0 
					for j in range(self.block_size):
						# processing a bit
						cur_time += 1
						if self.in_burst(cur_time):
							be = self.bit_error(self.e_burst)
							if be: errors += 1 
						if errors > HSBC:
							send_fail = 1 
							break			
			else: 
				for j in range(self.frame_size): 
					# no correction is in used 
					cur_time += 1
					b = self.in_burst(cur_time)

					if b:
						be = self.bit_error(self.e_burst)
						send_fail = 1 
			# decision on incrementing frame successfully transmitted 
			if send_fail == 1: 
				continue
			else: 
				received_frame += 1
		# print(total_frame, received_frame)
		return total_frame, received_frame

	def send_frame(self): 
		# increase run time
		self.run_time += self.frame_size
		return 

	def acknowledgement(self):
		# increase run time
		self.run_time += self.A
		return

	def bit_error(self, e): 
		r = random.random()
		# print(r)
		if r <= e: 
			# print(r)
			return 1
		else: 
			return 0

	def in_burst(self, cur_time): 
		# assume starts with non_burst period
		time_block = self.N + self.B
		time_in_block = cur_time%time_block 
		if time_in_block > self.N: 
			# print('burst')
			return True 
		else: 
			# print('non_burst')
			return False   

	def bit_error_in_message(self, message_size, e): 
		errors = 0		
		for i in range(message_size): 
			errors += self.bit_error(e)
		
		# return number of errors in the message
		return errors

	def writeResults(self, Filename, data): 

		with open(Filename, 'a+') as f:
			fieldnames = ['M', 'N', 'B', 'K', 'e', 'Frame transmission', 'Upper bound Ft', 'Lower Bound Ft', 'Throughput', 'Upper Bound Tp', 'Lower Bound Tp']
			writer = csv.DictWriter(f, fieldnames = fieldnames)

			# writer.writeheader()
			to_write = {}
			for i in range(len(fieldnames)): 
				to_write[fieldnames[i]] = data[i] 
			
			writer.writerow(to_write)

		return 