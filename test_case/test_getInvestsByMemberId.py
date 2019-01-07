# -*-coding:utf-8-*-
# author：陈婷
# Project：获取用户投资记录测试用例

# 思路：根据配置文件里的用户id，获取到所有的投资记录，
# 检查获取到的data数据的数量，到数据库查用户的投资记录数量，比较是否一致
# 检查某个标的投资金额，与查询出来的数据里的投资金额是否一致


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
case_data = do_excel.get_case('getInvestsByMemberId')
logger = MyLog()  #创建日志信息的实例

@ddt  # 装饰测试类
class TestGetInvestsByMemberId(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil()

    def setUp(self):
        logger.info('======================开始测试===========================')
        user_id = config.get_option_str('basic', 'user_id')
        sql_01 = "SELECT COUNT(*) FROM `future`.`invest` WHERE `MemberID` = {} AND `IsValid`=1 ".format(user_id)
        sql_02 = "SELECT COUNT(*) ,SUM(`Amount`),LoanId  FROM `future`.`invest` " \
                 "WHERE `MemberID` = {} AND `IsValid`=1 " \
                 "AND LoanId=(SELECT LoanId FROM `future`.`invest` WHERE `MemberID` = {} " \
                 "ORDER BY `LoanId` LIMIT 1)".format(user_id,user_id)
        self.res_bibLoan = mysql.fetch_one(sql_01)
        self.res_bibLoan_amount = mysql.fetch_one(sql_02)


    def tearDown(self):
        logger.info('======================结束测试===========================')

    @data(*case_data)
    def test_getInvestsByMemberId(self, case):
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
            do_excel.write_return('getInvestsByMemberId', case.case_id, actual, result)  # 将测试结果写入excel

            #  如果获取投标流水成功，则json里面的data数量=数据库里的数量
            try:
                if res.get_json()['code'] == '10001' and case.case_id != 1:
                    json_data = res.get_json()['data']
                    # 检查json里面的data数量=数据库里的数量
                    logger.error('json数据里面的总投标次数为：{}，数据库里面投资的总次数为：{}'.format(len(json_data) ,self.res_bibLoan['COUNT(*)']))
                    self.assertEqual(len(json_data) ,self.res_bibLoan['COUNT(*)']) # 比较期望值与实际值

                    # 检查 json里面某一个标的投资次数和总金额
                    json_data_loadAmount = 0  # 投资指定标id的总金额
                    json_data_loadNum = 0  # 投资指定标id的总次数
                    for i in json_data:
                        if int(i["loanId"]) == self.res_bibLoan_amount['LoanId']:
                            json_data_loadAmount += float(i["amount"])
                            json_data_loadNum +=1
                    logger.error('json数据里面 投资标id={}的总次数：{}'.format(self.res_bibLoan_amount['LoanId'], json_data_loadNum))
                    logger.error('数据库里面，投资标id={}的总次数：{}'.format(self.res_bibLoan_amount['LoanId'],self.res_bibLoan_amount['COUNT(*)']))
                    self.assertEqual(json_data_loadNum, self.res_bibLoan_amount['COUNT(*)'])  # 比较投标的次数

                    logger.error('json数据里面，投资标id={}的总金额={}'.format(self.res_bibLoan_amount['LoanId'],json_data_loadAmount))
                    logger.error('数据库里面 投资标id={}的总金额={}'.format(self.res_bibLoan_amount['LoanId'],self.res_bibLoan_amount['SUM(`Amount`)']))
                    self.assertEqual(json_data_loadAmount, self.res_bibLoan_amount['SUM(`Amount`)'])  # 比较投标的总金额
            except AssertionError as a:
                logger.error('错误原因:{}'.format(a))


    @classmethod
    def tearDownClass(cls):
        mysql.mysql.close()

if __name__ == '__main__':
    pass