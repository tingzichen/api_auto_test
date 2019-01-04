# -*-coding:utf-8-*-
# author：陈婷
# Project：获取配置文件的option

import configparser
import os
from api_auto_test.common import project_path
class Conf:
    def __init__(self):
        #创建实例
        self.cf = configparser.ConfigParser()
        #打开配置文件
        filename = os.path.join(project_path.conf_path,'global.conf')  # 这里利用os路径拼接，获取配置文件名称
        self.cf.read(filenames=filename,encoding='utf-8')
        # print(cf.sections())
        # print(cf.getboolean('switch','on'))
        if self.cf.getboolean('switch','on') == True:
            online = project_path.online_conf_path  # 获取正式环境的配置文件名称
            self.cf.read(filenames=online, encoding='utf-8')
        else:
            test = project_path.test_conf_path  # 获取正式环境的配置文件名称
            self.cf.read(filenames=test, encoding='utf-8')

    def get_option_str(self,section,option):
        return self.cf.get(section=section,option=option)

    def get_option_int(self,section,option):
        return self.cf.getint(section=section,option=option)

    def get_option_bool(self,section,option):
        return self.cf.getboolean(section=section,option=option)

    def get_option_float(self,section,option):
        return self.cf.getfloat(section=section,option=option)

    def write_option(self,value):  # 将参数化的MobilePhone写入配置文件
        if self.cf.getboolean('switch','on') == True:  # 如果执行online配置文件，则修改online文件里的MobilePhone值
            online = project_path.online_conf_path  # 获取正式环境的配置文件名称
            self.cf.set('API', 'MobilePhone', value=value)  # 增加/修改一个新的MobilePhone键值对到新的Section中：
            self.cf.write(open(online,'w'))  # 要想把增/改完毕的Config写入配置文件进行本地保存，需要调用write()函数：
            # print(self.cf['API']['MobilePhone'])

        else:   # 如果执行test配置文件，则修改test文件里的MobilePhone值
            test = project_path.test_conf_path  # 获取正式环境的配置文件名称
            self.cf.set('API', 'MobilePhone', value=value)
            self.cf.write(open(test, 'w'))  # 这里的write（）函数是将新增/修改的option值进行保存
            # print(self.cf['API']['MobilePhone'])

if __name__ == '__main__':
    get_option = Conf().get_option_str('API','url_pre')
    print(get_option)
    Conf().write_option('32433')
    print(Conf().get_option_str('API','MobilePhone'))
