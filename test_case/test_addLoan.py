# -*-coding:utf-8-*-
# author：陈婷
# Project：加标测试用例


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
case_data = do_excel.get_case('addLoan')
logger = MyLog()  #创建日志信息的实例

@ddt  # 装饰测试类
class TestAddLoan(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil()

    def setUp(self):
        logger.info('======================开始测试===========================')
        # MobilePhone = Conf().get_option_str('basic', 'normal_user')
        # user_id = Conf().get_option_str('basic', 'user_id')
        # pwd = Conf().get_option_str('basic', 'pwd')
        # setattr(Context, 'normal_user', MobilePhone)

    def tearDown(self):
        logger.info('======================结束测试===========================')

    @data(*case_data)
    def test_addLoan(self, case):
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
            do_excel.write_return('addLoan', case.case_id, actual, result)  # 将测试结果写入excel

            #  如果加标成功，loan表里面会增加一个标，标id从json里面获取，状态应为“审核中”
            try:
                if res.get_json()['msg'] == '加标成功':
                    # 加标成功，获取标id
                    sql = "SELECT Id ,`Title`, FROM `future`.`loan` WHERE `MemberID` = 1111405  ORDER BY `CreateTime` DESC LIMIT 1".format(user_id)
                    actual_title = mysql.fetch_one(sql)['Title']  # 查询数据库里的 标id 是否存在


                    # 需要重新检查，断言会报错
                    self.assertEqual(eval(data)['title'] ,actual_title) # 比较期望值与实际值
            except AssertionError as a:
                logger.error('错误原因:{}'.format(a))


    @classmethod
    def tearDownClass(cls):
        mysql.mysql.close()

if __name__ == '__main__':

    pass