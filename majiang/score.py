from tile import *


# 判断两张牌是否相同
def equal(tile1, tile2):
    return tile1.suit == tile2.suit and tile1.rank == tile2.rank

# 判断是否胡牌
def is_pair(hand):
    if len(hand) == 2:
        return equal(hand[0], hand[1])
    return False

# 对于已排序的手牌，检查是否是刻子
def is_triplet(hand):
    if len(hand) == 3:
        return equal(hand[0], hand[1]) and equal(hand[1], hand[2])
    return False

# 对于已排序的手牌，检查是否是顺子
def is_sequence(hand):
    if len(hand) == 3:
        suits = {tile.suit for tile in hand}
        ranks = sorted(tile.rank for tile in hand)
        return len(suits) == 1 and ranks[2] - ranks[1] == 1 and ranks[1] - ranks[0] == 1
    return False

# 对于已确定将的手牌，检查剩余手牌是否为顺子、刻子组合
def is_triple_match(hand, is_triplet_existing=True):
    if len(hand) == 0:
        return True
    
    # 检查刻子
    if is_triplet_existing:
        for i in range(len(hand) - 2):
            if is_triplet(hand[i:i+3]):
                remaining_hand = hand[:i] + hand[i+3:]
                if is_triple_match(remaining_hand):
                    return True

    is_triplet_existing = False  # 不再检查刻子
    # 检查顺子
    # 对剩余手牌进行简并
    hand_single = []
    for card in hand:
        if not any(equal(card, existing) for existing in hand_single):
            hand_single.append(card)
            if len(hand_single) == 3:
                break
    
    remaining_hand = hand
    if is_sequence(hand_single):
        remaining_hand.remove(hand_single[0])
        remaining_hand.remove(hand_single[1])
        remaining_hand.remove(hand_single[2])
        return is_triple_match(remaining_hand, is_triplet_existing)
        
    return False

    

def is_hu(hand, is_main=True):
    # 如果手牌数不是14张，直接返回
    if len(hand) != 14:
        return -5
    
    