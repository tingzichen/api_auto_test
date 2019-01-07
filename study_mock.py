# -*-coding:utf-8-*-
# author：陈婷
# Project：练习mock的使用

from unittest import mock
# from api_auto_test.common.http_requests import Request

# 这里是一个瞎编的微信充值接口
class WechatRecharge:

    @staticmethod
    def wechat_recharge(card_id,amount):
        # url = "http://ssdffsd.com"  # 假设这是一个微信提供的充值接口
        # res = Request('post',url,params={'card_id':card_id,'amount':amount},cookies=None)
        return res.get_status_code()  # 返回状态码


# 这里调用微信充值接口，检查是否充值成功
class Recharge:
    # 充值用户id： user_id
    # 充值卡号： card_id
    # 充值金额： amount
    @staticmethod
    def recharge(card_id,user_id,amount):
        try:
            res_code = WechatRecharge.wechat_recharge(card_id,amount)
        except TimeoutError:
            # 如果请求超时，就重新调用一次
            res_code = WechatRecharge.wechat_recharge(card_id, amount)

        if res_code == 200:  # 充值成功
            print("user_id={}的用户充值成功，充值金额为：{},用户余额增加".format(user_id,amount))
            return '充值成功'

        elif res_code != 200: # 充值失败
            print("user_id={}的用户充值失败，用户余额不变".format(user_id))
            return '充值失败'



if __name__ == '__main__':
    # res = Recharge.recharge(card_id=1,user_id=123,amount=500)
    res = WechatRecharge.wechat_recharge(card_id=1,amount=500)
