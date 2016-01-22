from Simulation import Simulation 
import csv

try:
	# with open('output_data.csv', 'a+') as f:
	# 	fieldnames = ['M', 'N', 'B', 'K', 'e', 'Frame transmission', 'Upper bound Ft', 'Lower Bound Ft', 'Throughput', 'Upper Bound Tp', 'Lower Bound Tp']
	# 	writer = csv.DictWriter(f, fieldnames = fieldnames)
	# 	writer.writeheader()
	for i in range(100):
		Test = Simulation()
		Test.run()
		input()

except EOFError: 
	pass 
