from Simulation import Simulation 


try:
	for i in range(100):
		Test = Simulation()
		Test.run()
		# Test.in_burst(5000)
		# Test.in_burst(5001)
		# Test.in_burst(5049)
		# Test.in_burst(5050)
		# Test.in_burst(5051)
		input()

except EOFError: 
	pass 
