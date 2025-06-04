#!/bin/env python

# 导入必要的库
import pygame  # 用于创建游戏窗口和处理图形
import sys  # 用于系统操作，如退出程序
import random  # 用于生成随机数，放置地雷
import os  # 用于处理文件路径
from dataclasses import dataclass  # 用于创建数据类
from typing import Literal  # 用于类型提示

# 定义单元格类，用于表示游戏中的每个格子
@dataclass
class Cell:
    value: Literal['mine', 'dead', 'number', 'flag', 'unk']  # 单元格的值：地雷、死亡、数字、旗帜、未知
    state: Literal['covered', 'revealed', 'flagged']  # 单元格的状态：覆盖、揭示、标记


# 初始化Pygame
pygame.init()


# 定义屏幕尺寸
WIDTH, HEIGHT = 300, 300  # 游戏窗口的宽度和高度
CELL_SIZE = 30  # 每个单元格的大小

# 定义游戏板的行数和列数
ROWS = HEIGHT // CELL_SIZE  # 行数
COLS = WIDTH // CELL_SIZE  # 列数
NUM_MINES = 10  # 地雷的数量


# 设置游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 创建游戏窗口
pygame.display.set_caption("MineCraft")  # 设置窗口标题

# 获取当前脚本的目录
script_dir = os.path.dirname(__file__)
# 加载图像
images = [os.path.join(script_dir, 'img', f'{num}.gif') for num in range(0, 14)]
# 加载图像
images = [pygame.image.load(img) for img in images]
# 调整图像大小
images = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in images]
# 构建图像映射，方便使用
image_map = {
    'number_0': images[0],
    'number_1': images[1],
    'number_2': images[2],
    'number_3': images[3],
    'number_4': images[4],
    'number_5': images[5],
    'number_6': images[6],
    'number_7': images[7],
    'number_8': images[8],
    'covered': images[9],
    'flag': images[10],
    'mine': images[11],
    'unk': images[12],
    'dead': images[13],
}

# --- 游戏变量 ---
board = [[]]  # 全局变量，用于存储游戏板的状态
game_state = 'playing'  # 游戏状态：'playing'（游戏中）, 'won'（胜利）, 'lost'（失败）
total_non_mines = 0  # 存储非地雷单元格的总数

# --- 游戏函数 ---

def create_board():
    """创建并初始化游戏板。"""
    global board, total_non_mines
    board = [[Cell('number', 'covered') for _ in range(COLS)] for _ in range(ROWS)]  # 初始化游戏板
    total_cells = ROWS * COLS  # 计算总单元格数
    total_non_mines = total_cells - NUM_MINES  # 计算非地雷单元格数

    # 放置地雷
    mines_placed = 0
    while mines_placed < NUM_MINES:
        row = random.randint(0, ROWS - 1)  # 随机选择行
        col = random.randint(0, COLS - 1)  # 随机选择列
        if board[row][col].value != 'mine':  # 如果该单元格不是地雷
            board[row][col].value = 'mine'  # 放置地雷
            mines_placed += 1

    # 计算非地雷单元格周围的数字
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c].value != 'mine':  # 如果当前单元格不是地雷
                num_adjacent_mines = 0  # 初始化相邻地雷数
                for dr in [-1, 0, 1]:  # 遍历相邻的行
                    for dc in [-1, 0, 1]:  # 遍历相邻的列
                        if dr == 0 and dc == 0:  # 跳过当前单元格
                            continue
                        nr, nc = r + dr, c + dc  # 计算相邻单元格的位置
                        if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc].value == 'mine':  # 检查是否在地雷
                            num_adjacent_mines += 1  # 增加相邻地雷数
                board[r][c].value = f'number_{num_adjacent_mines}'  # 设置单元格的值

def draw_board(screen):
    """绘制当前游戏板的状态。"""
    for r in range(ROWS):
        for c in range(COLS):
            cell = board[r][c]  # 获取当前单元格
            x = c * CELL_SIZE  # 计算单元格的x坐标
            y = r * CELL_SIZE  # 计算单元格的y坐标
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)  # 创建单元格的矩形
            if cell.state == 'covered':  # 如果单元格被覆盖
                screen.blit(image_map['covered'], rect.topleft)  # 绘制覆盖图像
            elif cell.state == 'flagged':  # 如果单元格被标记
                if cell.value == 'flag':  # 如果单元格的值是旗帜
                    screen.blit(image_map['flag'], rect.topleft)  # 绘制旗帜图像
                elif cell.value == 'unk':  # 如果单元格的值是未知
                    screen.blit(image_map['unk'], rect.topleft)  # 绘制未知图像
                else:
                    print(f'Unknown Cell value for flagged state: {cell.value}')  # 打印错误信息
                    assert False  # 断言失败
            elif cell.state == 'revealed':  # 如果单元格被揭示
                screen.blit(image_map[cell.value], rect.topleft)  # 绘制揭示图像
            else:
                print(f'Unknown state: {cell.state}')  # 打印错误信息
                assert False  # 断言失败


def handle_click(x, y, button):
    # 将像素坐标转换为游戏板坐标
    col = x // CELL_SIZE
    row = y // CELL_SIZE

    # 检查点击是否在游戏板边界内
    if 0 <= row < ROWS and 0 <= col < COLS:
        cell = board[row][col]  # 获取当前单元格

        # 左键点击（按钮1）揭示单元格
        if button == 1 and cell.state == 'covered':
            if cell.value == 'mine':  # 如果点击到地雷
                cell.value = 'dead'  # 设置单元格值为死亡
                cell.state = 'revealed'  # 揭示单元格
                global game_state
                game_state = 'lost'  # 设置游戏状态为失败
                print("Game Over! You hit a mine.")  # 简单通知
            elif cell.value == 'number_0':  # 如果是空单元格
                reveal_empty_cells(row, col)  # 揭示空单元格
                check_win_loss()  # 检查胜利或失败
            else:  # 如果是数字单元格
                cell.state = 'revealed'  # 揭示单元格

        # 右键点击（按钮3）标记单元格
        elif button == 3:
            if cell.state == 'covered':  # 如果单元格被覆盖
                cell.state = 'flagged'  # 标记单元格
                cell.value = 'flag'  # 设置单元格值为旗帜
            elif cell.state == 'flagged' and cell.value == 'flag':  # 如果单元格被标记为旗帜
                cell.value = 'unk'  # 设置单元格值为未知
            else:
                cell.state = 'covered'  # 覆盖单元格


def reveal_empty_cells(row, col):
    """递归揭示空单元格和相邻的数字单元格。"""
    # 检查边界和是否已经揭示或标记
    if not (0 <= row < ROWS and 0 <= col < COLS) or board[row][col].state != 'covered':
        return

    cell = board[row][col]  # 获取当前单元格
    cell.state = 'revealed'  # 揭示单元格

    # 如果是空单元格（number_0），递归揭示相邻单元格
    if cell.value == 'number_0':
        for dr in [-1, 0, 1]:  # 遍历相邻的行
            for dc in [-1, 0, 1]:  # 遍历相邻的列
                if dr == 0 and dc == 0:  # 跳过当前单元格
                    continue
                reveal_empty_cells(row + dr, col + dc)  # 递归揭示相邻单元格

def check_win_loss():
    """检查胜利或失败条件并更新游戏状态。"""
    global game_state
    if game_state == 'lost':  # 如果已经失败，无需检查胜利
        return

    revealed_non_mines = 0  # 初始化已揭示的非地雷单元格数
    for r in range(ROWS):
        for c in range(COLS):
            cell = board[r][c]  # 获取当前单元格
            if cell.state == 'revealed' and cell.value != 'mine':  # 如果单元格被揭示且不是地雷
                revealed_non_mines += 1  # 增加已揭示的非地雷单元格数

    if revealed_non_mines == total_non_mines:  # 如果所有非地雷单元格都被揭示
        game_state = 'won'  # 设置游戏状态为胜利
        print("Congratulations! You won!")  # 简单通知

# --- 主游戏循环 ---
def main():
    running = True  # 游戏运行标志
    create_board()  # 调用create_board初始化游戏板

    active_fingers = set()  # 用于跟踪活动的手指ID

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果事件类型是退出
                running = False  # 停止游戏循环
            
            if game_state == 'playing':  # 如果游戏状态是游戏中
                # 处理鼠标点击
                if event.type == pygame.MOUSEBUTTONDOWN:  # 如果事件类型是鼠标按下
                    x, y = event.pos  # 获取鼠标位置
                    handle_click(x, y, event.button)  # 处理点击

                # 处理触摸事件
                if event.type == pygame.FINGERDOWN:  # 如果事件类型是手指按下
                    active_fingers.add(event.finger_id)  # 添加活动手指ID
                    # 检查双指点击
                    if len(active_fingers) == 2:  # 如果有两个活动手指
                        x = int(event.x * WIDTH)  # 计算x坐标
                        y = int(event.y * HEIGHT)  # 计算y坐标
                        # 模拟右键点击（按钮3）
                        handle_click(x, y, 3)  # 处理点击
                    elif len(active_fingers) == 1:  # 如果只有一个活动手指
                        # 模拟左键点击
                        x = int(event.x * WIDTH)  # 计算x坐标
                        y = int(event.y * HEIGHT)  # 计算y坐标
                        handle_click(x, y, 1)  # 处理点击

                if event.type == pygame.FINGERUP:  # 如果事件类型是手指抬起
                    if event.finger_id in active_fingers:  # 如果手指ID在活动手指中
                        active_fingers.remove(event.finger_id)  # 移除活动手指ID

                # 我们也可以处理FINGERMOTION如果需要手势

        # --- 绘制 ---
        # screen.fill(WHITE)  # 填充背景
        draw_board(screen)  # 绘制游戏板
        
        # 显示游戏状态消息
        if game_state != 'playing':  # 如果游戏状态不是游戏中
            font = pygame.font.Font(None, 50)  # 创建字体
            message = "You Win!" if game_state == 'won' else "Game Over!"  # 设置消息
            text = font.render(message, True, (255, 0, 0))  # 渲染文本
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 获取文本矩形
            screen.blit(text, text_rect)  # 绘制文本

        # --- 更新显示 ---
        pygame.display.flip()  # 更新显示

    pygame.quit()  # 退出Pygame
    sys.exit()  # 退出程序

if __name__ == "__main__":
    main()  # 调用主函数
