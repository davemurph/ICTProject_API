import unittest
from _tests.HTMLTestRunner import HTMLTestRunner
from _tests.testcases import TestCases



suite1 = unittest.TestLoader().loadTestsFromTestCase(TestCases)


all_tests = unittest.TestSuite([suite1])

# method to run test suite using unittest's TextTestRunner
'''unittest.TextTestRunner(verbosity=2).run(all_tests)'''

outfile = open('C:\Users\Daithi\Documents\ICTProject\TestResults\CurrWebServiceReport.html', 'w')
runner = HTMLTestRunner(stream = outfile,
						title = 'Currency Converter Web Service Testing',
						verbosity = 2,
						description = 'Currency Converter Web Service - Unit test results')

runner.run(all_tests)