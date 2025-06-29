
from deck import *
from tile import *
from score import *
from actions import *


# 初始化pygame
pygame.init()

# 设置屏幕尺寸
screen = pygame.display.set_mode((1000, 600))  # 扩大屏幕宽度，容纳更多的牌
pygame.display.set_caption("麻将游戏")

# 创建牌堆
deck = create_deck()

# 玩家手牌
hand = [deck.pop() for _ in range(13)]

# 玩家操作变量
player_action = None
waiting_for_card_selection = False  # 等待玩家选择出牌
selected_card_index = -1  # 存储玩家选择的出牌索引
user_input = ""
input_active = False  # 是否处于输入状态


# 初始化积分
score = 0
button1_image = pygame.image.load("images/Button1.jpg")
button1_image = pygame.transform.scale(button1_image, (1000, 600))  # 调整按钮图片大小

cheat_mode = 0

# 游戏主循环
while True:
    screen.fill((0, 128, 0))  # 背景色绿色
    
    # 绘制玩家的手牌
    draw_tiles(screen, hand, 50, 400)
    
    # 绘制按钮
    draw_button(screen, "Draw", 50, 50, 100, 40)
    draw_button(screen, "Discard", 200, 50, 100, 40)
    draw_button(screen, "Hu", 350, 50, 100, 40)
    draw_button(screen, "Sort", 500, 50, 100, 40)
    draw_button(screen, "Exit", 650, 50, 100, 40)
    

    # 绘制备用按钮
    draw_button(screen, "Third Eye", 50, 500, 100, 40)

    draw_button(screen, "Cheat", 200, 500, 100, 40)
    draw_button(screen, "Search", 350, 500, 100, 40)
    draw_button(screen, "Button4", 500, 500, 100, 40)
    
    # 绘制提示信息
    font = pygame.font.SysFont(None, 40)
    if player_action:
        action_text = font.render(player_action, True, (255, 255, 255))
        screen.blit(action_text, (50, 150))

    # 绘制牌堆剩余数量
    remaining_deck_text = f"Remaining Deck: {len(deck)}"
    remaining_deck = font.render(remaining_deck_text, True, (255, 255, 255))
    screen.blit(remaining_deck, (50, 200))

    # 绘制玩家手牌数量
    hand_count_text = f"Hand Count: {len(hand)}"
    hand_count = font.render(hand_count_text, True, (255, 255, 255))
    screen.blit(hand_count, (50, 250))

    # 绘制积分
    score_text = f"Score: {score}"
    score_display = font.render(score_text, True, (255, 255, 255))
    screen.blit(score_display, (800, 50))  # 显示在屏幕右侧

    # 如果正在输入，显示输入框内容
    if input_active:
        input_box = pygame.Rect(350, 450, 300, 40)  # 输入框位置和大小
        pygame.draw.rect(screen, (255, 255, 255), input_box)  # 输入框背景
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)  # 输入框边框
        input_text = font.render(user_input, True, (0, 0, 0))
        screen.blit(input_text, (input_box.x + 10, input_box.y + 5))


    # 事件监听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 鼠标点击
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                x, y = event.pos
                
                # 如果正在等待选择打出的牌
                if waiting_for_card_selection:
                    # 判断点击的牌
                    tile_index = (x - 50) // (50 + 10)
                    if 0 <= tile_index < len(hand):
                        selected_card_index = tile_index
                        selected_tile = hand[selected_card_index]
                        player_action = f"Discard {selected_tile.rank}{selected_tile.suit[0]}"
                        hand.pop(selected_card_index)  # 从手牌中移除这张牌
                        waiting_for_card_selection = False  # 结束选择牌的模式
                        print(f"Finish discarding: {selected_tile.rank}{selected_tile.suit[0]}")
                
                # 检查是否点击了“摸牌”按钮
                elif 50 <= x <= 150 and 50 <= y <= 90:
                    if len(deck) > 0:
                        hand.append(deck.pop())
                        player_action = f"Drawn {hand[-1].rank}{hand[-1].suit[0]}"
                    else:
                        player_action = "Empty deck, cannot draw"
                
                # 检查是否点击了“出牌”按钮
                elif 200 <= x <= 300 and 50 <= y <= 90:
                    if len(hand) == 0:
                        player_action = "No tiles to discard"
                        continue
                    waiting_for_card_selection = True  # 开始等待选择要打出的牌     
                    player_action = "Please select a tile to discard"
                
                # 检查是否点击了“胡牌”按钮
                elif 350 <= x <= 450 and 50 <= y <= 90:
                    hu_result = is_hu(hand)
                    if hu_result > 0:
                        player_action = "Congratulations! You Hu!"
                    else:
                        player_action = "Buff!"
                    score = score + hu_result + cheat_mode  # 更新积分
                    waiting_for_card_selection = True
                    
                
                # 检查是否点击了“理牌”按钮
                elif 500 <= x <= 600 and 50 <= y <= 90:
                    hand = sort_hand(hand)
                    player_action = "Sorted"

                elif 650 <= x <= 750 and 50 <= y <= 90:
                    pygame.quit()  # 退出游戏
                    sys.exit()  # 退出程序
                # 检查是否点击了备用按钮
                elif 50 <= x <= 150 and 500 <= y <= 540:
                    player_action = "Button1 clicked"
                    deck_screen = pygame.display.set_mode((1000, 600))
                    pygame.display.set_caption("麻将游戏")
                    screen.blit(button1_image, (1, 1))  # 显示备用按钮的图片
                    pygame.display.flip()
                    time.sleep(2)
                    show_deck_window(deck)
                elif 200 <= x <= 300 and 500 <= y <= 540:
                    cheat_mode = 10 - cheat_mode  # 切换作弊模式
                    if cheat_mode:
                        player_action = "Cheat Mode"
                    else:
                        player_action = "Normal Mode"
                    
                elif 350 <= x <= 450 and 500 <= y <= 540:
                    player_action = "Search for ..."
                    input_active = True
                    user_input = ""
                elif 500 <= x <= 600 and 500 <= y <= 540:
                    player_action = "Button4 clicked"
        # 键盘输入
        if input_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # 按下回车键
                input_active = False  # 停止输入模式
                # 解析输入内容
                if len(user_input) >= 2 and user_input[:-1].isdigit() and user_input[-1] in ['W', 'T', 'B']:
                    rank = int(user_input[:-1])  # 提取数字
                    suit = {'W': 'Wan', 'T': 'Tiao', 'B': 'Bing'}[user_input[-1]]  # 提取花色
                    remaining_count = sum(1 for tile in deck if tile.rank == rank and tile.suit == suit)
                    player_action = f"Remaining {user_input}: {remaining_count}"
                    if remaining_count > 0:
                        # 如果有剩余牌，显示剩余牌数量
                        pass
                else:
                    player_action = f"Remaining {user_input}: 0"  # 非法输入
            elif event.key == pygame.K_BACKSPACE:  # 按下退格键
                user_input = user_input[:-1]  # 删除最后一个字符
            else:
                user_input += event.unicode  # 添加输入字符


        
    pygame.display.flip()