# 操作数据库
import pymysql
from api_auto_test.common.config import Conf
'''
1、先建立数据库的连接，从配置文件里面读取连接数据库的数据
2、建立游标（游标相当于光标，光标是用在txt文件里面的，游标是用在数据库里的
3、编写sql语句
4、执行sql语句
5、将结果写回到配置文件
'''

class MysqlUtil:

    def __init__(self):
        # 建立连接,先从配置文件读取连接数据库的数据
        conf = Conf()
        host = conf.get_option_str('Mysql', 'host')
        port = conf.get_option_int('Mysql', 'port')  # 因为连接数据库时，传参post是一个整型，这里直接用int类型的接收
        user = conf.get_option_str('Mysql', 'user')
        pwd = conf.get_option_str('Mysql', 'pwd')
        try:
            self.mysql = pymysql.connect(host=host, user=user, password=pwd, port=port,
                                         cursorclass=pymysql.cursors.DictCursor)  # 建立数据库的连接
        except AssertionError as a:
            print('数据库连接失败，请检查配置文件里的数据库连接参数')
            raise a

    def fetch_one(self, sql):   # 这个方法的作用是：查询一条数据，并返回查询结果
        cursor = self.mysql.cursor()  # 建立游标
        cursor.execute(sql)  # 根据sql进行查询
        cursor.close()
        return  cursor.fetchone()  # 获取查询结果,fetchone只返回一条数据

    def fetch_all(self, sql):
        cursor = self.mysql.cursor()
        cursor.executemany(sql)
        cursor.close()
        return cursor.fetchall()

if __name__ == '__main__':
    # sql = 'SELECT MobilePhone FROM  future.`member` WHERE `MobilePhone` != "" ORDER BY `MobilePhone` DESC LIMIT 1;'   # sql里面的引号需要用双引号，否则要转义
    mysql = MysqlUtil()
    # returns= mysql.fetch_one(sql)  #得到一个结果，类型是字典
    # print(returns)

    # sql = {
    #     'auditLoan_id': "SELECT Id FROM `future`.`loan` WHERE STATUS=1 ORDER BY id DESC LIMIT 1",
    #     'two_auditLoan_id': "SELECT Id FROM `future`.`loan` WHERE STATUS=2 ORDER BY id DESC LIMIT 1",
    #     'three_auditLoan_id': "SELECT Id FROM `future`.`loan` WHERE STATUS=3 ORDER BY id DESC LIMIT 1",
    #     'compete_loan_id': "SELECT Id FROM `future`.`loan` WHERE STATUS=4 ORDER BY id DESC LIMIT 1",}
    # for i in sql.keys():
    #     res = mysql.fetch_one(sql[i])
    #     print("i的值：",i)
    #     print('res的值：',res)

    sql ="SELECT COUNT(*) ,SUM(`Amount`),LoanId  FROM `future`.`invest` WHERE `MemberID` = {} AND " \
         "`IsValid`=1 AND LoanId=(SELECT LoanId FROM `future`.`invest` WHERE `MemberID` = {} " \
         "ORDER BY `LoanId` LIMIT 1)".format(1111405,1111405)
    res = mysql.fetch_one(sql)
    print('res的值：', res)


