# -*-coding:utf-8-*-
# author：陈婷
# Project：审核项目接口测试用例


import json
import unittest
from ddt import ddt, data

from api_auto_test.common import project_path
from api_auto_test.common.do_excel import DoExcel
from api_auto_test.common.http_requests import Request
from api_auto_test.common.my_log import MyLog
from api_auto_test.common.mysql_util import MysqlUtil
from api_auto_test.common.basic_pattern import *

# 获取测试数据
do_excel = DoExcel(project_path.testCase_path)
case_data = do_excel.get_case('audit')
logger = MyLog()  #创建日志信息的实例

@ddt  # 装饰测试类
class TestAudit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil()
        # auditLoan_id = None   # 审核中
        # two_auditLoan_id = None   # 二审中
        # three_auditLoan_id = None  # 三审中
        # compete_loan_id = None  # 竞标中

    def setUp(self):
        logger.info('======================开始测试===========================')
        sql = {
            'auditLoan_id': "SELECT Id FROM `future`.`loan` WHERE STATUS=1 ORDER BY id DESC LIMIT 1",
            'two_auditLoan_id': "SELECT Id FROM `future`.`loan` WHERE STATUS=2 ORDER BY id DESC LIMIT 1",
            'three_auditLoan_id': "SELECT Id FROM `future`.`loan` WHERE STATUS=3 ORDER BY id DESC LIMIT 1",
            'compete_loan_id': "SELECT Id FROM `future`.`loan` WHERE STATUS=4 ORDER BY id DESC LIMIT 1", }
        for i in sql.keys():
            res = mysql.fetch_one(sql[i])
            setattr(Context,i,res['Id'])

    def tearDown(self):
        logger.info('======================结束测试===========================')

    @data(*case_data)
    def test_audit(self, case):
        logger.info('=====case_id={}======用例title={}====='.format(case.case_id,case.title))
        case_data = case.params
        pattern = "\$\{.+?\}"
        data = Pattern().pattern(case_data, pattern)
        logger.info('测试data数据：{}'.format(data))
        if case.case_id != 1:
            sql = "SELECT id,Status FROM `future`.`loan` WHERE Id ={}".format(eval(data)['id'])
            logger.info('测试前data数据里标{}的状态为{}'.format(eval(data)['id'],mysql.fetch_one(sql)['Status']))
        cookies = Context.cookies
        res = Request(case.http_method, case.url, eval(data), cookies=cookies)  # 创建Request实例，发送接口请求
        actual = json.dumps(res.get_json(), ensure_ascii=False)  # json数据里面含有中文，写入表单时，需要设置编码格式
        logger.info('json数据：{}'.format(res.get_json()))
        if res.get_cookies():
            setattr(Context,'cookies',res.get_cookies())
        try:
            self.assertEqual(str(case.expected), res.get_json()['code'])  # 判断期望结果与实际结果
            result = 'PASS'
        except AssertionError as a:
            result = 'False'
            logger.error('断言报错啦！，错误原因：{}'.format(a))
            raise a
        finally:
            logger.error('测试结果是：{}'.format(result))
            do_excel.write_return('audit', case.case_id, actual, result)  # 将测试结果写入excel

            #  如果项目审核成功，标状态data中的status”
            try:
                if res.get_json()['code'] == '1001' and case.case_id != 1:
                    # 审核成功，根据标id，查询标的状态
                    # sql = "SELECT STATUS FROM `future`.`loan` WHERE Id ={}".format(eval(data)['id'])
                    actual_status = mysql.fetch_one(sql)['Status']  # 查询数据库里的 标的状态
                    self.assertEqual(eval(data)['status'] ,actual_status) # 比较用例里的状态和数据库的状态
            except AssertionError as a:
                logger.error('错误原因:{}'.format(a))


    @classmethod
    def tearDownClass(cls):
        mysql.mysql.close()

if __name__ == '__main__':
    pass