from tile import *
import pygame
import random
import sys
import time


# 理牌功能：按花色和数字排序手牌，且相同的牌放在一起
def sort_hand(hand):
    sorted_hand = sorted(hand, key=lambda x: (x.suit, x.rank))  # 按花色和数字排序
    return sorted_hand

# 绘制麻将牌
def draw_tiles(screen, tiles, x, y):
    tile_width = 50
    tile_height = 80
    for i, tile in enumerate(tiles):
        pygame.draw.rect(screen, (255, 255, 255), (x + i * (tile_width + 10), y, tile_width, tile_height))
        pygame.draw.rect(screen, (0, 0, 0), (x + i * (tile_width + 10), y, tile_width, tile_height), 2)
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"{tile.rank}{tile.suit[0]}", True, (0, 0, 0))
        screen.blit(text, (x + i * (tile_width + 10) + 5, y + 5))

# 绘制按钮
def draw_button(screen, text, x, y, width, height):
    font = pygame.font.SysFont(None, 30)
    pygame.draw.rect(screen, (0, 0, 255), (x, y, width, height))  # 按钮的背景
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 2)  # 按钮的边框
    button_text = font.render(text, True, (255, 255, 255))
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))

def show_deck_window(deck):
    """显示剩余牌堆的子界面"""
    # 创建一个新的窗口
    deck_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("剩余牌堆")

    running = True
    while running:
        deck_screen.fill((0, 0, 0))  # 设置背景为黑色

        # 绘制剩余牌堆
        font = pygame.font.SysFont(None, 30)
        x, y = 50, 50  # 起始位置
        for i, tile in enumerate(deck):
            tile_text = font.render(f"{tile.rank}{tile.suit[0]}", True, (255, 255, 255))
            deck_screen.blit(tile_text, (x, y))
            x += 100  # 每张牌右移
            if x > 700:  # 如果超出窗口宽度，换行
                x = 50
                y += 40

        tile_text = font.render("<-top", True, (255, 255, 255))
        deck_screen.blit(tile_text, (x, y))  # 显示剩余牌数
        # 监听事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # 关闭子窗口
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # 按下 ESC 键关闭子窗口

        pygame.display.flip()

    # 关闭子窗口后返回主窗口
    pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("麻将游戏")
