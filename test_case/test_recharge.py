
# 这是充值接口
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
case_data = do_excel.get_case('recharge')
logger = MyLog()  #创建日志信息的实例

@ddt  # 装饰测试类
class TestRecharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil()

    def setUp(self):
        logger.info('======================开始测试===========================')
        MobilePhone = Conf().get_option_str('basic', 'normal_user')
        self.sql = "SELECT id,`MobilePhone`,`LeaveAmount` FROM  future.`member` WHERE `MobilePhone` ={}".format(MobilePhone)
        self.user_data = mysql.fetch_one(self.sql)
        setattr(Context, 'LeaveAmount',self.user_data['LeaveAmount'])
        logger.info('账户余额={}'.format(Context.LeaveAmount))

    def tearDown(self):
        logger.info('======================结束测试===========================')

    @data(*case_data)
    def test_recharge(self, case):
        logger.info('============测试用例的title为： {}==============case_id={}'.format(case.title, case.case_id))
        case_data = case.params
        pattern = "\$\{.+?\}"
        data = Pattern().pattern(case_data, pattern)
        cookies = Context.cookies
        res = Request(case.http_method, case.url, eval(data), cookies=cookies)  # 创建Request实例，发送接口请求
        actual = json.dumps(res.get_json(), ensure_ascii=False)  # json数据里面含有中文，写入表单时，需要设置编码格式
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
            do_excel.write_return('recharge', case.case_id, actual, result)  # 将测试结果写入excel

            try:
                if res.get_json()['msg'] == '竞标成功': # 这里如果用code=10001,需要再判断一次登录成功的用例
                    data_amount = eval(data)['amount']  # 投标金额
                    expected_amount = float(Context.LeaveAmount) - float(data_amount)  # 期望金额 = 原余额-投资金额
                    logger.error("投标金额={}".format(data_amount))
                    actual_amount = float(mysql.fetch_one(self.sql)['LeaveAmount'])  # 实际余额 = 数据库里的余额
                    self.assertEqual(expected_amount,actual_amount) # 比较期望余额与实际余额
                elif res.get_json()['code'] != '10001':
                    expected_amount = float(Context.LeaveAmount)  # 如果投标失败，期望余额=投标前的余额
                    actual_amount = float(mysql.fetch_one(self.sql)['LeaveAmount'])
                    self.assertEqual(expected_amount, actual_amount)  # 比较期望余额与实际余额
            except AssertionError as a:
                logger.error('数据库账户余额不等于实际余额，错误原因:{}'.format(a))
                logger.error('数据库账户余额{}，实际余额应为{}'.format(actual_amount,expected_amount))

    @classmethod
    def tearDownClass(cls):
        mysql.mysql.close()

