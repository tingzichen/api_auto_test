import unittest
import HTMLTestRunnerNew
from api_auto_test.common import project_path

from api_auto_test.test_case import test_bidLoan

suite = unittest.TestSuite()
loder = unittest.TestLoader()
suite.addTest(loder.loadTestsFromModule(test_bidLoan))

# 执行测试用例，生成.html格式的测试报告
with open(project_path.report_path+'/test_bidLoan_report.html','wb+') as file:
    run = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title='投标的测试报告', tester='ting')
    run.run(suite)