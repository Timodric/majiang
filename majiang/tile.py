# 创建麻将牌类
class MahjongTile:
    def __init__(self, suit, rank):
        self.suit = suit  # 花色 (万, 条, 筒)
        self.rank = rank  # 牌的数字 1-9
        self.image = None  # 后面会加载图像

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"{self.rank}{self.suit}"
