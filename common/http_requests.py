
import json

import requests

from api_auto_test.common import project_path
from api_auto_test.common.do_excel import *

class Request:
    def __init__(self,http_method,url,params,cookies):
        if http_method.upper() == 'GET':
            self.res = requests.get(url=url,params=params,cookies=cookies)

        elif http_method.upper() == 'POST':
            self.res = requests.post(url=url,data=params,cookies=cookies)

        else:
            print('你的{}请求方式错啦！'.format(http_method))


    def get_json(self):
        return  self.res.json()

    def get_header(self):
        return  self.res.headers

    def get_text(self):
        return self.res.text

    def get_status_code(self):
        return self.res.status_code

    def get_cookies(self):
        return self.res.cookies


if __name__ == '__main__':
    # 获取所有表单名，遍历表单名
    do_excel = DoExcel(project_path.testCase_path)
    sheetnames = do_excel.sheet_namme()
    for sheetname in sheetnames: # 遍历表单名
        case_data = do_excel.get_case( sheetname) # 获取测试数据对象列表
        for case in case_data: # 遍历数据列表里的对象
            data=eval(case.params)
            res = Request(case.http_method,case.url,data,cookies=None) # 创建Request实例，发送接口请求
            actual=json.dumps(res.get_json(),ensure_ascii=False) # json数据里面含有中文，写入表单时，需要设置编码格式
            if str(case.expected) == res.get_json()['code']: # 判断期望结果与实际结果
                result='PASS'
            else:
                result ='False'
            do_excel.write_return(sheetname,case.case_id,actual,result) # 将测试结果写入excel


