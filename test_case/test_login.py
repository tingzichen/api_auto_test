
# 设计测试用例，利用unittest框架
# 思路：先从excel读取数据，把读取到的数据用http_requests模块发送请求，进行断言，将结果写会excel文件
# 用ddt的目的是：如果不加ddt，相当于用一条用例执行了表单里的所有数据，这样会影响测试结果，
# 利用ddt，可以实现一条用例执行一条数据的目的
import unittest
import json
from ddt import ddt, data
from api_auto_test.common.do_excel import DoExcel
from api_auto_test.common import project_path
from api_auto_test.common.http_requests import Request
# 获取测试数据
do_excel = DoExcel(project_path.testCase_path)
case_data = do_excel.get_case('login')

@ddt  # 装饰测试类
class TestLogin(unittest.TestCase):
    def setUp(self):
        print('开始测试')

    def tearDown(self):
        print('清除数据')
        print('==================我是分割线=========================')

    @data(*case_data)  # 这里将case_data脱了一层外套，变成了一个个的对象；如果这里不加*号，在test_login函数里面用for来遍历，那还是一条用例执行了多条数据，会影响测试结果
    def test_login(self, case):  # case用来接收case_data脱了一层外套后的一个对象
        print('测试用例的title为:{}，case_id={}'.format(case.title,case.case_id))
        data = eval(case.params)
        res = Request(case.http_method, case.url, data, cookies=None)  # 创建Request实例，发送接口请求
        actual = json.dumps(res.get_json(), ensure_ascii=False)  # json数据里面含有中文，写入表单时，需要设置编码格式
        if str(case.expected) == res.get_json()['code']:
            result = 'PASS'
        else:
            print(case.expected, res.get_json())
            result = 'False'
        try:
            self.assertEqual(str(case.expected), res.get_json()['code'])  # 判断期望结果与实际结果
        except AssertionError as a:
            print('断言报错啦！，错误原因：',a)
            raise a
        print('测试结果是：',result)

        do_excel.write_return('login', case.case_id, actual, result)  # 将测试结果写入excel





