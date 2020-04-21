import time


class View(object):
    @staticmethod
    def login():
        while True:
            name = input("请输入管理员账户:")
            pwd = input("请输入管理员密码:")
            if name == "admin" and pwd == "111":
                # 打印欢迎界面
                View.login_view()
                # 延迟一秒刷新界面
                time.sleep(1)
                # 打印操作界面
                View.operation_view()
                # 账号密码正确返回True
                return True
            else:
                print("管理员账号或密码不正确")

    @staticmethod
    def login_view():
        print("*******************************************")
        print("*                                         *")
        print("*                                         *")
        print("*         Welcome To OldBoy Bank          *")
        print("*                                         *")
        print("*                                         *")
        print("*******************************************")

    @staticmethod
    def operation_view():
        print("*******************************************")
        print("*           开户(1)    查询(2)             *")
        print("*           存钱(3)    取钱(4)             *")
        print("*           转账(5)    改密(6)             *")
        print("*           锁卡(7)    解卡(8)             *")
        print("*           补卡(9)    退出(0)             *")
        print("*******************************************")
