from Bank.view import View
from Bank.operation import Operation


class Main():
    @staticmethod
    def run():
        if View.login():
            obj = Operation()
            while True:
                choice = input("请选选择需要办理的业务:")
                # 用反射来实现
                get_func = Operation.dic_func[int(choice)]
                var = getattr(obj, get_func)
                if get_func=='save':
                    var()
                    break
                else:
                    var()

                # 卡户
                if choice == "1":
                    obj.register()
                # 查询
                elif choice == "2":
                    obj.query()
                # 存钱
                elif choice == "3":
                    obj.save_money()
                elif choice == "4":
                    print(4)
                elif choice == "5":
                    print(5)
                elif choice == "6":
                    print(6)
                # 锁卡
                elif choice == "7":
                    obj.lock()
                # 解卡
                elif choice == "8":
                    obj.unlock()
                elif choice == "9":
                    print(9)
                # 退出保存
                elif choice == "0":
                    obj.save()
                    break


if __name__ == '__main__':
    Main.run()

