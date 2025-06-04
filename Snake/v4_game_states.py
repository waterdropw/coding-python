"""
# 贪吃蛇游戏 v4 - 游戏状态版本

## 版本特点
- 添加了游戏状态管理（开始、暂停、结束）
- 实现了完整的游戏界面系统
- 增加了暂停功能
- 添加了游戏重启功能

## 关键概念说明

### 1. 游戏状态管理
- **开始界面**：显示游戏标题和开始提示
- **游戏界面**：显示游戏主体和分数
- **暂停状态**：可以暂停和继续游戏
- **结束界面**：显示最终分数和重新开始选项

### 2. 界面系统
- **文本渲染**：
  - 使用不同大小的字体（标题和普通文本）
  - 文本居中显示
  - 多行文本布局
- **界面切换**：
  - 开始界面 → 游戏界面
  - 游戏界面 → 暂停状态
  - 游戏界面 → 结束界面
  - 结束界面 → 重新开始或退出

### 3. 游戏控制
- **暂停功能**：
  - 空格键切换暂停状态
  - 暂停时显示暂停提示
  - 暂停时停止蛇的移动
- **重新开始**：
  - 游戏结束后可以选择重新开始
  - 重新开始会重置所有游戏状态

### 4. 状态转换
- **开始游戏**：按空格键从开始界面进入游戏
- **暂停游戏**：按空格键切换暂停状态
- **结束游戏**：
  - 撞墙或撞到自己时进入结束界面
  - 可以选择重新开始或退出游戏

## 游戏控制
- 方向键：控制蛇的移动方向
- 空格键：开始游戏/暂停游戏/重新开始
- ESC键：退出游戏
- 窗口关闭按钮：退出游戏

## 游戏规则
- 每吃到一个食物得10分
- 撞墙或撞到自己身体游戏结束
- 可以随时暂停游戏
- 游戏结束后可以选择重新开始
"""

# 导入必要的库
# pygame: 用于创建游戏的Python库
# sys: 提供与Python解释器和运行环境相关的变量和函数
# random: 用于生成随机数
import pygame
import sys
import random

# 初始化 Pygame
# pygame.init() 初始化所有Pygame模块，在使用Pygame功能前必须调用
pygame.init()

# 定义颜色常量
# 在Pygame中，颜色使用RGB格式表示：(红, 绿, 蓝)
# 每个颜色分量的取值范围是0-255
BLACK = (0, 0, 0)      # 黑色：所有颜色分量都是0
WHITE = (255, 255, 255) # 白色：所有颜色分量都是255
RED = (255, 0, 0)      # 红色：只有红色分量是255
GREEN = (0, 255, 0)    # 绿色：只有绿色分量是255
BLUE = (0, 0, 255)     # 蓝色：只有蓝色分量是255

# 游戏设置
# 定义游戏窗口和网格的大小
WINDOW_WIDTH = 800     # 窗口宽度（像素）
WINDOW_HEIGHT = 600    # 窗口高度（像素）
GRID_SIZE = 20        # 每个网格的大小（像素）
# // 是整除运算符，返回商的整数部分
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE   # 计算网格的宽度数量
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE # 计算网格的高度数量

# 创建游戏窗口
# set_mode() 创建一个新的显示窗口，参数是窗口的尺寸（宽度，高度）
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# 设置窗口标题
pygame.display.set_caption('Snake Game v4 - Game States')

# 设置游戏时钟
# Clock对象用于控制游戏的帧率
clock = pygame.time.Clock()

# 初始化字体
# pygame.font.init() 初始化字体系统
pygame.font.init()
# 创建字体对象，None表示使用默认字体，36是字体大小
font = pygame.font.Font(None, 36)
# 创建标题字体对象，72是字体大小
title_font = pygame.font.Font(None, 72)

def generate_food(snake_pos):
    """
    生成新的食物，确保不会生成在蛇身上
    参数：
        snake_pos: 蛇身体的位置列表
    返回：
        新的食物位置 [x, y]
    """
    while True:
        # random.randint(a, b) 生成a到b之间的随机整数（包含a和b）
        food_pos = [
            random.randint(0, GRID_WIDTH-1),  # 随机x坐标
            random.randint(0, GRID_HEIGHT-1)  # 随机y坐标
        ]
        # 确保食物不会生成在蛇身上
        if food_pos not in snake_pos:
            return food_pos

def draw_text(text, font, color, x, y):
    """
    在屏幕上绘制文本
    参数：
        text: 要显示的文本
        font: 字体对象
        color: 文本颜色
        x, y: 文本中心位置
    """
    # render() 将文本转换为图像
    # 参数：文本内容, 抗锯齿, 颜色
    text_surface = font.render(text, True, color)
    # get_rect() 获取文本的矩形区域
    # center=(x, y) 设置矩形的中心点
    text_rect = text_surface.get_rect(center=(x, y))
    # blit() 在屏幕上绘制图像
    # 参数：要绘制的图像, 位置矩形
    screen.blit(text_surface, text_rect)

def show_start_screen():
    """
    显示开始界面
    使用 while True 循环等待用户输入
    """
    while True:
        # 清空屏幕
        screen.fill(BLACK)
        # 绘制游戏标题和提示文本
        draw_text("Snake Game", title_font, GREEN, WINDOW_WIDTH//2, WINDOW_HEIGHT//3)
        draw_text("Press SPACE to Start", font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        draw_text("Press ESC to Quit", font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3)
        
        # 更新显示
        pygame.display.flip()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 空格键开始游戏
                if event.key == pygame.K_SPACE:
                    return
                # ESC键退出游戏
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_game_over_screen(score):
    """
    显示游戏结束界面
    参数：
        score: 最终得分
    返回：
        True: 重新开始游戏
        False: 退出游戏
    """
    while True:
        # 清空屏幕
        screen.fill(BLACK)
        # 绘制游戏结束信息和分数
        draw_text("Game Over", title_font, RED, WINDOW_WIDTH//2, WINDOW_HEIGHT//3)
        draw_text(f"Score: {score}", font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        draw_text("Press SPACE to Restart", font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3)
        draw_text("Press ESC to Quit", font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT*3//4)
        
        # 更新显示
        pygame.display.flip()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 空格键重新开始游戏
                if event.key == pygame.K_SPACE:
                    return True
                # ESC键退出游戏
                elif event.key == pygame.K_ESCAPE:
                    return False

def main():
    """
    主函数：实现完整的游戏，包括状态管理
    """
    # 外层循环：处理游戏重启
    while True:
        # 显示开始界面
        show_start_screen()
        
        # 初始化游戏状态
        snake_pos = [[GRID_WIDTH//2, GRID_HEIGHT//2]]
        snake_direction = [1, 0]
        food_pos = generate_food(snake_pos)
        score = 0
        paused = False
        
        # 游戏主循环
        while True:
            # 处理游戏事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    # 空格键切换暂停状态
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    # 只有在非暂停状态下才处理方向键
                    elif not paused:
                        if event.key == pygame.K_UP and snake_direction != [0, 1]:
                            snake_direction = [0, -1]
                        elif event.key == pygame.K_DOWN and snake_direction != [0, -1]:
                            snake_direction = [0, 1]
                        elif event.key == pygame.K_LEFT and snake_direction != [1, 0]:
                            snake_direction = [-1, 0]
                        elif event.key == pygame.K_RIGHT and snake_direction != [-1, 0]:
                            snake_direction = [1, 0]
            
            # 只有在非暂停状态下才更新游戏状态
            if not paused:
                # 更新蛇的位置
                new_head = [
                    snake_pos[0][0] + snake_direction[0],
                    snake_pos[0][1] + snake_direction[1]
                ]
                
                # 检查是否撞墙
                if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                    break
                
                # 检查是否撞到自己
                if new_head in snake_pos:
                    break
                
                # 将新头部添加到蛇身列表的开头
                snake_pos.insert(0, new_head)
                
                # 检查是否吃到食物
                if new_head == food_pos:
                    score += 10
                    food_pos = generate_food(snake_pos)
                else:
                    snake_pos.pop()
            
            # 清空屏幕
            screen.fill(BLACK)
            
            # 绘制食物
            food_rect = pygame.Rect(
                food_pos[0] * GRID_SIZE,
                food_pos[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, RED, food_rect)
            
            # 绘制蛇
            for pos in snake_pos:
                snake_rect = pygame.Rect(
                    pos[0] * GRID_SIZE,
                    pos[1] * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE
                )
                pygame.draw.rect(screen, GREEN, snake_rect)
            
            # 显示分数
            draw_text(f'Score: {score}', font, WHITE, 70, 20)
            
            # 如果游戏暂停，显示暂停文字
            if paused:
                draw_text("PAUSED", title_font, BLUE, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            
            # 更新显示
            pygame.display.flip()
            
            # 控制游戏速度
            clock.tick(10)
        
        # 显示游戏结束界面
        if not show_game_over_screen(score):
            break

# Python的特殊语法：当这个文件被直接运行时（而不是被导入时）
# __name__ 变量的值会是 '__main__'
if __name__ == '__main__':
    main() 