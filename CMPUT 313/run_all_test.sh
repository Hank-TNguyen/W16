# run_all_test
echo "Running all tests"
python3 main.py < test_argument.in 
python3 main.py < test_B_1000_50.in 
python3 main.py < test_B_1000_500.in 
python3 main.py < test_B_5000_50.in 
python3 main.py < test_B_5000_500.in 
echo "Finished"