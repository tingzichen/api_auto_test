# -*-coding:utf-8-*-
# author：陈婷
# Project：日志操作

# 目的：
# 定义一个日志封装类
# 控制台输出所有debug级别以上的信息
# 按照当前日期定义两个file分别存放info 、 error信息
# 使用文件的方式，日志是一直追加的，需要做日志回滚，指定输出文件的大小，限制文件大小，清理旧日志


import logging
import time
import HTMLTestRunnerNew
from api_auto_test.common.project_path import *

# 创建一个日志收集器
logger = logging.getLogger('ting')

#定义日志收集器的级别，这里是最低级别
logger.setLevel('DEBUG')

def set_handler(levels):
    if levels == 'ERROR':  #判断如果是error就添加error信息到handler
        logger.addHandler(MyLog.error_handler)
    else:  # 其他添加到info_handler
        logger.addHandler(MyLog.info_handler)
    logger.addHandler(MyLog.ch)  # 全部输出到控制台
    logger.addHandler(MyLog.report_handler)  # 全部输出到report

def remove_handler(levels):
    if levels == 'ERROR':
        logger.removeHandler(MyLog.error_handler)
    else:
        logger.removeHandler(MyLog.info_handler)
    logger.removeHandler(MyLog.ch)
    logger.removeHandler(MyLog.report_handler)

def get_current_day(): # 获取当前日期
    return time.strftime('%y%m%d',time.localtime(time.time()))

def get_log_dir(): # 获取当天的日志存放目录
    log_dir = os.path.join(logs_path,get_current_day())
    if not os.path.isdir(log_dir): # 判断是否存在
        os.makedirs(log_dir)  # 不存在就创建一个文件
    return log_dir  # 存在就直接返回


class MyLog:
    # 设置输出日志格式
    formatter01 = '%(asctime)s-%(levelname)s-%(filename)s--%(name)s日志信息: %(message)s'  # 输出格式
    formatter = logging.Formatter(formatter01)

    # 指定输出渠道
    # 控制台输出
    ch = logging.StreamHandler() # 控制台输出
    ch.setLevel('DEBUG')
    ch.setFormatter(formatter)

    # info文件输出
    info_handler = logging.FileHandler(filename=info_log, encoding='utf-8')
    info_handler.setLevel('INFO')
    info_handler.setFormatter(formatter)

    # error日志文件输出
    error_handler = logging.FileHandler(filename=error_log,encoding='utf-8')
    error_handler.setLevel('ERROR')
    error_handler.setFormatter(formatter)

    # 报表日志输出
    report_handler = logging.StreamHandler(HTMLTestRunnerNew.stdout_redirector)
    report_handler.setLevel('INFO')
    report_handler.setFormatter(formatter)

    @staticmethod
    def debug(msg):
        set_handler('DEBUG')
        logger.debug(msg)
        remove_handler('DEBUG')

    @staticmethod
    def info(msg):
        set_handler('INFO')
        logger.info(msg)
        remove_handler('INFO')

    @staticmethod
    def error(msg):
        set_handler('ERROR')
        logger.error(msg) # 同时输出异常信息
        remove_handler('ERROR')

if __name__ == '__main__':
    a=2
    try:
        MyLog.error('00000000000000error!!!!!')
        pass
    except AssertionError as a:
        MyLog.error('error!!!!!')
        # MyLog.error('这是一条error信息001')
        # MyLog.error('这是一条error信息002')
        # MyLog.error('这是一条error信息003')
        # MyLog.error('这是一条error信息004')
    MyLog.info('这是info数据001')
    MyLog.info('这是info数据002')

    MyLog.debug('这是一组debug信息001')
    MyLog.debug('这是一组debug信息002')


