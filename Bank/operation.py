import os
import pickle
import random
from .card import Card
from .user import User


class Operation(object):
    # 初始化操作

    dic_func = {1: 'register', 2: 'query', 3: 'save_money', 7: 'lock', 8: 'unlock', 0: 'save'}

    def __init__(self):
        # 程序进行操作时加载两套存储数据（用函数分离写法）
        # 第一套：卡号：用户对象
        self.load_user()

        # 第二套：身份证：卡号
        self.load_user_id()

    def load_user(self):
        # 判断文件是否存在,存在时候就拿数据,否则初始化空字典
        if os.path.exists("user.txt"):
            with open("user.txt", 'rb')as rf:
                self.user_dict = pickle.load(rf)
        else:
            self.user_dict = {}
        print(self.user_dict)

    def load_user_id(self):
        if os.path.exists("user_id.text"):
            with open("user_id.txt", "rb")as rf:
                self.user_id_dict = pickle.load(rf)
        else:
            self.user_id_dict = {}
        print(self.user_id_dict)

    # 保存退出操作
    def save(self):
        with open("user.txt", mode="wb") as fp:
            pickle.dump(self.user_dict, fp)

        with open("userid.txt", mode="wb") as fp:
            pickle.dump(self.user_id_dict, fp)

    # 开户操作
    def register(self):
        name = input("请输入您的姓名:")
        user_id = input("请输入您的身份证号:")
        phone = input("请输入您的手机号:")
        # 获取卡密码
        password = self.get_cwd()
        # 获取卡号
        card_id = self.get_cardid()

        # 余额默认10块
        money = 10

        # 创建一张新卡
        card = Card(card_id, password, money)
        # 创建一个用户
        user = User(name, user_id, phone, card)

        # 存储数据
        # 存储 (卡号:用户对象)
        # self.user_dict[card.card_id]=user
        self.user_dict[card_id] = user
        # 存储（身份证：卡号）
        # self.user_id_dict[user.user_id]=card_id
        self.user_id_dict[user_id] = card_id

        # 给出提示
        print("恭喜{}开卡成功,您的卡号为:{},卡内余额{}元".format(name, card_id, money))

    # 获取密码
    def get_cwd(self):
        while True:
            pwd1 = input("请输入您的密码:")
            pwd2 = input("请确认您的密码:")
            if pwd1 == pwd2:
                return pwd1  # 返回给上面的password
            else:
                print("两次密码不一致,请重新输入")

    # 获取卡号
    def get_cardid(self):
        card_id = ""
        for i in range(6):
            card_id += str(random.randrange(0, 10))
        if card_id not in self.user_dict:
            return card_id

    #  查询操作
    def query(self):  # 查询
        # 先获取到一张卡
        # 获取卡信息
        card = self.get_card_info()
        # card 要么返回False  要么返回真实对象
        if not card:
            print("对不起,你的卡不存在")
        else:
            # 判断卡是否锁定
            if card.is_lock:  # islock=True
                print("对不起,您的卡被锁了")
            else:
                # 检查卡密码
                if self.check_cwd(card):
                    print("你的卡内余额是{}元".format(card.money))

    # 获取卡信息
    def get_card_info(self):
        card_id = input("请输入您的卡号")
        if card_id not in self.user_dict:
            print("您的卡不存在")
        else:  # 获取用户对象
            # 通过: 卡号：用户对象 取到对象
            user = self.user_dict[card_id]
            # 拿到 封装在用户类中的卡对象
            return user.card

    # 检查卡密码
    def check_cwd(self, card):
        count = 1
        while count < 4:
            pwd = input("请输入您的密码")
            if pwd == card.password:
                return True
            else:
                # 剩余次数 = 总次数-已经循环的次数
                print("密码错误,您还剩下%d次机会" % (3 - count))
                # 等于三次，直接锁卡
                if count == 3:
                    card.is_lock = True
                    print("抱歉,因为密码错了三次,你的卡被锁了")

            count += 1

    # 存钱操作
    def save_money(self):
        card = self.get_card_info()
        if not card:
            print("抱歉，你的卡不存在！")
        else:
            # 获取用户对象
            user = self.user_dict[card.card_id]  # 卡号：用户对象 表
            print("您的卡用户名:%s" % (user.name))
            key_sure = input("确认存款请按 1 ,任意按键回上一层!")
            if key_sure == "1":
                str_money = input("请输入您的存款金额:")
                if str_money.isdecimal():
                    money = int(str_money)
                    # 充值
                    card.money += money
                    print("成功存入%s元" % (money))
                else:
                    print("你输入的金额有误！")

    # 锁卡操作
    def lock(self):
        card = self.get_card_info()
        if not card:
            print("抱歉,您的卡不存在")
        else:
            num = input("1.使用密码冻结  2.使用身份证冻结")
            if num == "1":
                if self.check_cwd(card):
                    card.is_lock = True
                    print("======锁卡成功======")
            elif num == "2":
                user_id = input("请输入您的身份证号:")
                user = self.user_dict[card.card_id]
                if user_id == user.user_id:
                    card.is_lock = True
                    print("======锁卡成功======")
                else:
                    print("======锁卡失败======")

    # 解卡操作
    def unlock(self):
        card = self.get_card_info()
        if not card:
            print("抱歉,您的卡不存在")
        else:
            while True:
                user_id = input("请输入您的身份证号:")
                user = self.user_dict[card.card_id]
                if user_id != user.user_id:
                    print('您输入的身份证有误，请重新输入！')
                    break
                else:
                    if self.check_cwd(card):
                        card.is_lock = False
                        print("======解卡成功======")
                        return
