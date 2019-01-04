# -*-coding:utf-8-*-
# author：陈婷
# Project：提现接口测试用例

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
case_data = do_excel.get_case('withdraw')
logger = MyLog()  #创建日志信息的实例

@ddt  # 装饰测试类
class TestWithdraw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil()

    def setUp(self):
        logger.info('======================开始测试===========================')
        MobilePhone = Conf().get_option_str('basic', 'normal_user')
        setattr(Context, 'normal_user', MobilePhone)

        # 从数据库获取以137开头的最大的电话号码,创造一个不存在的会员
        sql = "SELECT MobilePhone FROM `future`.`member` WHERE MobilePhone LIKE '137%' ORDER BY `MobilePhone` DESC LIMIT 1"
        self.user_data = mysql.fetch_one(sql)
        setattr(Context, 'register_user',int(self.user_data['MobilePhone'])+1)

        # 从数据库获取用户余额
        self.sql = "SELECT id,`MobilePhone`,`LeaveAmount` FROM  future.`member` WHERE `MobilePhone` ={}".format(MobilePhone)
        self.user_data = mysql.fetch_one(self.sql)
        setattr(Context, 'LeaveAmount',self.user_data['LeaveAmount'])
        logger.info('账户余额={}'.format(Context.LeaveAmount))

    def tearDown(self):
        logger.info('======================结束测试===========================')

    @data(*case_data)
    def test_withdraw(self, case):
        logger.info('=====case_id={}======用例title={}====='.format(case.case_id,case.title))
        case_data = case.params
        pattern = "\$\{.+?\}"
        data = Pattern().pattern(case_data, pattern)
        logger.info('测试data数据：{}'.format(data))
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
            do_excel.write_return('withdraw', case.case_id, actual, result)  # 将测试结果写入excel

            #  如果提现成功，用户余额 = 原有余额 - 提现金额
            try:
                if res.get_json()['msg'] == '取现成功':
                    expecte_amount = float(Context.LeaveAmount) - float(eval(data)['amount'])  # 原有余额 - 提现金额
                    logger.error("提现金额：{}".format(eval(data)['amount']))
                    actual_amount = mysql.fetch_one(self.sql)['LeaveAmount']  # 查询数据库里的用户余额
                    self.assertEqual(float(expecte_amount),float(actual_amount)) # 比较期望值与实际值
                elif res.get_json()['code'] != '10001' and res.get_json()['msg'] != '手机号不能为空':
                    expecte_amount = Context.LeaveAmount # 原有余额 - 提现金额
                    logger.error("提现金额：{}".format(expecte_amount))
                    actual_amount = mysql.fetch_one(self.sql)['LeaveAmount']  # 查询数据库里的用户余额
                    self.assertEqual(float(expecte_amount), float(actual_amount))  # 比较期望值与实际值

            except AssertionError as a:
                logger.error('错误原因:{}'.format(a))


    @classmethod
    def tearDownClass(cls):
        mysql.mysql.close()

if __name__ == '__main__':
    pass
