# -*-coding:utf-8-*-
# author：陈婷
# Project：使用mock模拟充值接口的返回值

from unittest import mock
from mock import Mock,call
import unittest
from api_auto_test.study_mock import *

class Test_WechatRecharge(unittest.TestCase):

    def setUp(self):
        pass

    def test_wechatRecharge(self):

        #return_value，side_effect同时使用时，只会读取side_effect的值，side_effect需要是一个可扩展的数据类型：列表、元组。。。
        WechatRecharge.wechat_recharge = mock.Mock(return_value=300,side_effect=[TimeoutError,200])
        res_pay = Recharge.recharge(card_id=1, user_id=123, amount=500)
        try:
            self.assertEqual(res_pay,'充值成功')
        except AssertionError as a:
            print('断言报错啦',a)
        print('==========我是分割线===========')

        # 检查mock方法使用了正确的参数。
        WechatRecharge.wechat_recharge.assert_called_with(1,500)

        # 检查mock方法使用了正确的参数，且只被调用一次
        # WechatRecharge.wechat_recharge.assert_called_once_with(1, 500)

        # 检查mock方法至少被调用一次
        print('mock模拟对象是否被调用',WechatRecharge.wechat_recharge.called)

        # 检查mock方法被调用的次数
        print('mock模拟对象调用的次数',WechatRecharge.wechat_recharge.call_count)

        # 检查是否调用了mock方法
        print('mock模拟对象调用的次数', WechatRecharge.wechat_recharge.assert_any_call(1, 500))

        # 判断mock方法被多次调用
        # print('mock模拟对象被多次调用', WechatRecharge.wechat_recharge.assert_not_called)

        # 检查是否按照正确的顺序和正确的参数进行调用的
        WechatRecharge.wechat_recharge.assert_has_calls(calls=[call(1, 500), call(1, 500)])


    def tearDown(self):
        pass

