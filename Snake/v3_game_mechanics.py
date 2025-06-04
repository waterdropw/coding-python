"""
# 贪吃蛇游戏 v3 - 游戏机制版本

## 版本特点
- 添加了食物生成机制
- 实现了分数系统
- 增加了自身碰撞检测
- 添加了分数显示功能

## 关键概念说明

### 1. 食物系统
- **随机生成**：使用 `random` 模块生成随机位置
- **碰撞避免**：确保食物不会生成在蛇身上
- **食物获取**：吃到食物后蛇身变长，分数增加

### 2. 分数系统
- **分数计算**：每吃到一个食物得10分
- **分数显示**：使用 Pygame 字体系统显示分数
- **字体初始化**：
  - `pygame.font.init()` 初始化字体系统
  - `pygame.font.Font()` 创建字体对象
  - `render()` 将文本转换为图像

### 3. 碰撞检测
- **墙壁碰撞**：检测是否撞到游戏边界
- **自身碰撞**：检测是否撞到自己的身体
- **食物碰撞**：检测是否吃到食物

### 4. 蛇身管理
- **长度控制**：
  - 吃到食物：保留尾部，蛇身变长
  - 未吃到食物：删除尾部，保持长度不变
- **位置更新**：根据移动方向更新蛇身位置

## 游戏控制
- 方向键：控制蛇的移动方向
- ESC键：退出游戏
- 窗口关闭按钮：退出游戏

## 游戏规则
- 每吃到一个食物得10分
- 撞墙或撞到自己身体游戏结束
- 食物随机生成在空白位置
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
pygame.display.set_caption('Snake Game v3 - Game Mechanics')

# 设置游戏时钟
# Clock对象用于控制游戏的帧率
clock = pygame.time.Clock()

# 初始化字体
# pygame.font.init() 初始化字体系统
pygame.font.init()
# 创建字体对象，None表示使用默认字体，36是字体大小
font = pygame.font.Font(None, 36)

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

def main():
    """
    主函数：实现完整的游戏机制
    """
    # 初始化蛇的位置和方向
    # 使用列表存储蛇身体的每个部分的位置
    # 每个位置是一个包含[x, y]坐标的列表
    snake_pos = [[GRID_WIDTH//2, GRID_HEIGHT//2]]
    # 方向向量：[x, y]表示移动方向
    snake_direction = [1, 0]  # 初始向右移动
    
    # 初始化食物位置
    food_pos = generate_food(snake_pos)
    
    # 初始化分数
    score = 0
    
    # 游戏主循环
    # while True 创建一个无限循环，直到游戏退出
    while True:
        # 处理游戏事件
        # pygame.event.get() 获取所有待处理的事件
        for event in pygame.event.get():
            # pygame.QUIT 是窗口关闭事件
            if event.type == pygame.QUIT:
                pygame.quit()  # 退出Pygame
                sys.exit()     # 退出Python程序
            # pygame.KEYDOWN 是按键按下事件
            elif event.type == pygame.KEYDOWN:
                # pygame.K_ESCAPE 是ESC键
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # 处理方向键输入
                # 使用 and 运算符确保蛇不能直接向相反方向移动
                elif event.key == pygame.K_UP and snake_direction != [0, 1]:
                    snake_direction = [0, -1]  # 向上移动
                elif event.key == pygame.K_DOWN and snake_direction != [0, -1]:
                    snake_direction = [0, 1]   # 向下移动
                elif event.key == pygame.K_LEFT and snake_direction != [1, 0]:
                    snake_direction = [-1, 0]  # 向左移动
                elif event.key == pygame.K_RIGHT and snake_direction != [-1, 0]:
                    snake_direction = [1, 0]   # 向右移动
        
        # 更新蛇的位置
        # 计算新的头部位置：当前位置 + 移动方向
        new_head = [
            snake_pos[0][0] + snake_direction[0],  # x坐标
            snake_pos[0][1] + snake_direction[1]   # y坐标
        ]
        
        # 检查是否撞墙
        # 使用 or 运算符检查是否超出边界
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            pygame.quit()
            sys.exit()
        
        # 检查是否撞到自己
        # 使用 in 运算符检查新头部是否在蛇身列表中
        if new_head in snake_pos:
            pygame.quit()
            sys.exit()
        
        # 将新头部添加到蛇身列表的开头
        # insert(0, new_head) 在列表开头插入新元素
        snake_pos.insert(0, new_head)
        
        # 检查是否吃到食物
        # 使用 == 运算符比较两个列表是否相等
        if new_head == food_pos:
            # 增加分数
            score += 10
            # 生成新的食物
            food_pos = generate_food(snake_pos)
        else:
            # 如果没有吃到食物，删除尾部
            # pop() 删除并返回列表的最后一个元素
            snake_pos.pop()
        
        # 清空屏幕
        # fill() 用指定颜色填充整个屏幕
        screen.fill(BLACK)
        
        # 绘制食物
        # pygame.Rect() 创建一个矩形对象
        # 参数分别是：x坐标, y坐标, 宽度, 高度
        food_rect = pygame.Rect(
            food_pos[0] * GRID_SIZE,  # x坐标
            food_pos[1] * GRID_SIZE,  # y坐标
            GRID_SIZE,                # 宽度
            GRID_SIZE                 # 高度
        )
        # draw.rect() 在屏幕上绘制矩形
        # 参数：屏幕对象, 颜色, 矩形对象
        pygame.draw.rect(screen, RED, food_rect)
        
        # 绘制蛇
        # 遍历蛇身体的每个部分
        for pos in snake_pos:
            snake_rect = pygame.Rect(
                pos[0] * GRID_SIZE,
                pos[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, GREEN, snake_rect)
        
        # 显示分数
        # render() 将文本转换为图像
        # 参数：文本内容, 抗锯齿, 颜色
        score_text = font.render(f'Score: {score}', True, WHITE)
        # blit() 在屏幕上绘制图像
        # 参数：要绘制的图像, 位置坐标
        screen.blit(score_text, (10, 10))
        
        # 更新显示
        # flip() 更新整个显示窗口
        pygame.display.flip()
        
        # 控制游戏速度
        # tick() 控制游戏的帧率，参数是每秒的帧数
        clock.tick(10)

# Python的特殊语法：当这个文件被直接运行时（而不是被导入时）
# __name__ 变量的值会是 '__main__'
if __name__ == '__main__':
    main() 