import pygame
import random
import sys
import time
from tile import MahjongTile  # 导入麻将牌类
# 创建一个牌堆，每种牌有4张
def create_deck():
    suits = ['Wan', 'Tiao', 'Bing']
    deck = []
    for suit in suits:
        for rank in range(1, 10):  # 每种花色有1到9的数字
            for _ in range(4):  # 每张牌有4张
                deck.append(MahjongTile(suit, rank))
    random.shuffle(deck)  # 打乱牌堆
    save_deck(deck)  # 保存牌堆到文件
    return deck

# 保存牌堆到 deck.txt 文件
def save_deck(deck):
    with open("deck.txt", "w") as file:
        for tile in deck:
            file.write(f"{tile}\n")


def find_tile_positions(deck, rank, suit):
    """
    查询牌堆中某张牌的所有位置。
    :param deck: 牌堆列表
    :param rank: 牌的数字 (1-9)
    :param suit: 牌的花色 ('Wan', 'Tiao', 'Bing')
    :return: 包含所有匹配牌索引的列表
    """
    positions = [i for i, tile in enumerate(deck) if tile.rank == rank and tile.suit == suit]
    return positions

def deck_delete(deck, position):
    """
    从牌堆中删除指定位置的牌。
    :param deck: 牌堆列表
    :param position: 要删除的牌的位置索引
    :return: 删除后的牌堆
    """
    if 0 <= position < len(deck):
        del deck[position]
    return deck

def deck_add(deck, tile):
    """
    向牌堆中添加一张牌。
    :param deck: 牌堆列表
    :param tile: 要添加的麻将牌对象
    :return: 添加后的牌堆
    """
    deck.append(tile)
    return deck