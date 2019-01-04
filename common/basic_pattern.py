# 这里做正则匹配和反射操作

import re
from api_auto_test.common.config import Conf
config = Conf()
normal_user = config.get_option_str('basic', 'normal_user')
pwd = config.get_option_str('basic', 'pwd')
user_id = config.get_option_str('basic', 'user_id')
class Pattern:
    def pattern(self,data,pattern):
        res = re.findall(pattern, data)
        for i in range(0,len(res)):
            if 'normal_user' in res[i]:
                setattr(Context, 'normal_user', normal_user)
                data = data.replace(res[i], normal_user)
            elif 'pwd'in res[i]:
                setattr(Context, 'pwd', pwd)
                data = data.replace(res[i], pwd)
            elif 'user_id' in res[i]:
                setattr(Context, 'user_id', user_id)
                data = data.replace(res[i], user_id)
            elif 'register_user' in res[i]:
                data = data.replace(res[i], str(Context.register_user))
            elif 'user_id'in res[i]:
                data = data.replace(res[i], str(Context.user_id))
            elif 'NotFull_loanId' in res[i]:
                data = data.replace(res[i], str(Context.NotFull_loanId))
            elif 'NoneLoanId' in res[i]:
                data = data.replace(res[i], str(Context.NoneLoanId))
            elif 'CannotInvest_loanId' in res[i]:
                data = data.replace(res[i], str(Context.CannotInvest_loanId))
            elif 'Full_loanId' in res[i]:
                data = data.replace(res[i], str(Context.Full_loanId))
            elif 'NotFull_amount' in res[i]:
                data = data.replace(res[i], str(int(int(Context.LeaveAmount)/100)*200))
        return data

 #  测试上下文
class Context:
    register_user = None  # 从数据库读取137开头的手机号码+1
    normal_user = None
    user_id = None
    pwd = None
    cookies = None
    LeaveAmount = None

    # 投标时用：
    NotFull_loanId = None  # 没有投满的标  从数据库取Status=4 状态：“竞标中”
    NoneLoanId = None  # 不存在的标   从数据库取最大的标id+1
    CannotInvest_loanId = None  # 不在竞标状态的标  从数据库取Status != 4
    Full_loanId = None  # 已满标  从数据库取FullTime != null  满标时间不为空

    NotFull_amount = None  # 余额不足


if __name__ == '__main__':
    pattern = "\$\{.+?\}"
    # data = '{"memberId":${user_id},"password":${pwd},"loanId":${NotFull_loanId},"amount":"200"}'
    data = '{"mobilephone":${user_id},"amount":"int(${LeaveAmount}/100)*200"}'
    Pattern().pattern(data,pattern)
    print(data)
