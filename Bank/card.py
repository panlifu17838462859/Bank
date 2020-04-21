class Card(object):
    def __init__(self, card_id, password, money):
        self.card_id = card_id
        self.password = password
        self.money = money
        # 默认新开的卡都不锁
        self.is_lock = False
