# -*-coding:utf-8-*-
# author：陈婷
# Project： 执行测试用例

import unittest
from api_auto_test.common import project_path
import HTMLTestRunnerNew

# print(project_path.test_case_path)
# 自动查找test_case文件下面以test开头的文件
# print(project_path.test_case_path)
discover = unittest.defaultTestLoader.discover(project_path.test_case_path,pattern="test*.py",top_level_dir=None)

with open(project_path.report_path+'/test_report.html','wb') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title='测试报告', tester='ting')
    runner.run(discover)
