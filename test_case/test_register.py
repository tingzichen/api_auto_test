# -*-coding:utf-8-*-
# author：陈婷
# Project：注册接口测试用例


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
case_data = do_excel.get_case('register')
logger = MyLog()  #创建日志信息的实例

@ddt  # 装饰测试类
class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil()

    def setUp(self):
        logger.info('======================开始测试===========================')
        # MobilePhone = Conf().get_option_str('basic', 'normal_user')
        # 从数据库获取以138开头的最大的电话号码
        sql = "SELECT MobilePhone FROM `future`.`member` WHERE MobilePhone LIKE '138%' ORDER BY `MobilePhone` DESC LIMIT 1"
        self.user_data = mysql.fetch_one(sql)
        setattr(Context, 'register_user',int(self.user_data['MobilePhone'])+1)


    def tearDown(self):
        logger.info('======================结束测试===========================')

    @data(*case_data)
    def test_register(self, case):
        logger.info('=====case_id={}======用例title={}====='.format(case.case_id,case.title))
        case_data = case.params
        pattern = "\$\{.+?\}"
        data = Pattern().pattern(case_data, pattern)
        logger.info('测试data数据：{}'.format(data))
        cookies = Context.cookies
        res = Request(case.http_method, case.url, eval(data), cookies=cookies)  # 创建Request实例，发送接口请求
        actual = json.dumps(res.get_json(), ensure_ascii=False)  # json数据里面含有中文，写入表单时，需要设置编码格式
        try:
            self.assertEqual(str(case.expected), res.get_json()['code'])  # 判断期望结果与实际结果
            result = 'PASS'
        except AssertionError as a:
            result = 'False'
            logger.error('断言报错啦！，错误原因：{}'.format(a))
            raise a
        finally:
            logger.error('测试结果是：{}'.format(result))
            do_excel.write_return('register', case.case_id, actual, result)  # 将测试结果写入excel
            #  如果注册成功，用注册的手机号码去用户表里面查，能查到则正常，查不到则不正常
            try:
                if res.get_json()['msg'] == '注册成功': # 这里如果用code=10001,需要再判断一次登录成功的用例
                    expecte_mobilePhone = eval(data)['mobilephone']  # 注册手机号码
                    logger.error("注册手机号码：{}".format(expecte_mobilePhone))
                    sql = "SELECT MobilePhone FROM `future`.`member` WHERE MobilePhone={}".format(expecte_mobilePhone)
                    actual_mobilePhone = mysql.fetch_one(sql)['MobilePhone']  # 查询数据库里的手机号码
                    self.assertEqual(str(expecte_mobilePhone),actual_mobilePhone) # 比较期望值与实际值
                elif res.get_json()['code'] != '10001' and res.get_json()['msg'] != '手机号不能为空':
                    expecte_mobilePhone = eval(data)['mobilephone']  # 注册手机号码
                    logger.error("注册手机号码：{}".format(expecte_mobilePhone))
                    sql = "SELECT MobilePhone FROM `future`.`member` WHERE MobilePhone='{}'".format(expecte_mobilePhone)
                    actual_mobilePhone = mysql.fetch_one(sql)['MobilePhone']  # 查询数据库里的手机号码
                    print('actual_mobilePhone',actual_mobilePhone)
                    self.assertEqual(expecte_mobilePhone, actual_mobilePhone)  # 比较期望值与实际值

            except AssertionError as a:
                logger.error('数据库手机号不等于注册手机号，错误原因:{}'.format(a))


    @classmethod
    def tearDownClass(cls):
        mysql.mysql.close()

if __name__ == '__main__':
    pass
