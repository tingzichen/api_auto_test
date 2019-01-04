#-*-coding:utf-8-*-

'''
1：结合1207上课讲的日志知识，以及配置文件知识点编写一个属于自己的可控制的日志类，要求如下：
1）日志输出的渠道 可以通过配置文件指定输出到指定文件或者是指定渠道
2）通过配置文件 可以指定输出日志的格式 formatter
3）通过配置文件 可以指定我们日志收集器收集日志的级别 以及 输出渠道输出日志的级别
4）把这个日志类 结合我们test_http_requst这个测试类来做
print的信息用 info级别日志信息来代替
异常信息用error级别的日志信息来代替
'''
import logging
import time
from api_auto_test.common.project_path import *

def get_current_day(): # 获取当前日期
    return time.strftime('%Y%m%d',time.localtime(time.time()))

# 通过获取当前日期，将每次执行时获取到的日志存放在当天日志文件下面
def get_log_dir(): # 获取当天的日志存放目录
    log_dir = os.path.join(logs_path,get_current_day())
    if not os.path.isdir(log_dir): # 判断是否存在
        os.makedirs(log_dir)  # 不存在就创建一个文件
    return log_dir  # 存在就直接返回

class MyLog:
    def mylog(self,msg,Level):
        logger=logging.getLogger('Ting')
        logger.setLevel('DEBUG') #日志收集的级别debug级别以上
        formatter01 = '%(asctime)s-%(levelname)s-%(filename)s--%(name)s日志信息: %(message)s'  # 日志输出的格式
        formatter=logging.Formatter(formatter01)

        # 文件日志
        # 输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel('DEBUG')  # 输出ERROR以上的
        ch.setFormatter(formatter)  # 输出指定格式formatter的日志
        logger.addHandler(ch)
        # 将info日志 输出到文件日志
        info_handler = logging.FileHandler(get_log_dir()+'\info_log.log',mode='a+', encoding='utf-8')
        info_handler.setLevel('INFO')
        info_handler.setFormatter(formatter)
        logger.addHandler(info_handler)
        # 将error日志 输出到文件日志
        error_handler = logging.FileHandler(get_log_dir()+'\error_log.log',mode='a+', encoding='utf-8')
        error_handler.setLevel('ERROR')
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

        #调用方式的级别判断
        if Level =='DEBUG':
            logger.debug(msg)
        elif Level == 'INFO':
            logger.info(msg)
        elif Level == 'WARNING':
            logger.warning(msg)
        elif Level == 'ERROR':
            logger.error(msg)
        elif Level == 'CRITICAL':
            logger.critical(msg)
        logger.removeHandler(ch)  # 执行完后，移除控制台上日志
        logger.removeHandler(info_handler)  # 执行完后，移除info_handler
        logger.removeHandler(error_handler)  # 执行完后，移除error_handler



    #不同的级别调用不同的方法：
    def debug(self,msg):
        self.mylog(msg,'DEBUG')
    def info(self,msg):
        self.mylog(msg,'INFO')
    def warning(self,msg):
        self.mylog(msg,'WARNING')
    def error(self,msg):
        self.mylog(msg,'ERROR')
    def critical(self, msg):
        self.mylog(msg,'CRITICAL')

if __name__ == '__main__':
    logger=MyLog().error('这是一条error日志')
    print('======1========')
    logger = MyLog().info('这是一条info日志')
    print('=====2=========')

    logger = MyLog().debug('这是一条debug日志')
    print('=======3=======')
    logger = MyLog().error('这是一4条error日志')
    print('========4======')

