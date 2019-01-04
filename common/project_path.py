
#这里存放文件的绝对路径
import os

#获取当前项目的地址
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(dir_path)

#获取test_case目录文件地址
test_case_path= os.path.join(dir_path,'test_case')
#这是excel文件地址
testCase_path=os.path.join(dir_path,'test_datas','testCase.xlsx')
# print(testCase_path)

#这里是配置文件地址
conf_path = os.path.join(dir_path,'configs')

#这里是配置文件总开关地址
global_conf_path = os.path.join(dir_path,'configs','global.conf')
# print(global_conf_path)

#这里是测试环境的配置文件地址
test_conf_path = os.path.join(dir_path,'configs','test.conf')
# print(test_conf_path)

#这里是测试环境的配置文件地址
online_conf_path = os.path.join(dir_path,'configs','online.conf')
# print(online_conf_path)

#report的地址
report_path = os.path.join(dir_path,'reports')
# print(report_path)

#日志目录的地址
logs_path = os.path.join(dir_path,'logs')
# info日志文件地址
info_log= os.path.join(logs_path,'info_logs')
#error日志文件地址
error_log= os.path.join(logs_path,'error_logs')