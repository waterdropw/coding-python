"""
# 贪吃蛇游戏 v2 - 移动控制版本

## 版本特点
- 添加了蛇的移动控制功能
- 实现了基本的碰撞检测（墙壁碰撞）
- 使用方向键控制蛇的移动方向

## 关键概念说明

### 1. 移动控制
- **方向控制**：使用方向键（↑↓←→）控制蛇的移动方向
- **方向向量**：使用 [x, y] 坐标表示移动方向
  - [1, 0] 表示向右移动
  - [-1, 0] 表示向左移动
  - [0, 1] 表示向下移动
  - [0, -1] 表示向上移动
- **防止反向移动**：蛇不能直接向相反方向移动

### 2. 碰撞检测
- **墙壁碰撞**：检测蛇头是否碰到游戏边界
- **边界条件**：
  - x < 0 或 x >= GRID_WIDTH
  - y < 0 或 y >= GRID_HEIGHT

### 3. 蛇身更新
- **头部更新**：根据移动方向计算新的头部位置
- **身体移动**：在头部添加新位置，删除尾部位置
- **列表操作**：
  - `insert(0, new_head)` 在列表开头添加新头部
  - `pop()` 删除列表末尾的尾部

## 游戏控制
- 方向键：控制蛇的移动方向
- ESC键：退出游戏
- 窗口关闭按钮：退出游戏

## 注意事项
- 蛇不能直接向相反方向移动
- 撞墙会导致游戏结束
"""

# 导入必要的库
# pygame: 用于创建游戏的Python库
# sys: 提供与Python解释器和运行环境相关的变量和函数
import pygame
import sys

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
pygame.display.set_caption('Snake Game v2 - Movement Control')

# 设置游戏时钟
# Clock对象用于控制游戏的帧率
clock = pygame.time.Clock()

def main():
    """
    主函数：实现蛇的移动控制和基本的碰撞检测
    """
    # 初始化蛇的位置和方向
    # 使用列表存储蛇身体的每个部分的位置
    # 每个位置是一个包含[x, y]坐标的列表
    snake_pos = [[GRID_WIDTH//2, GRID_HEIGHT//2]]
    # 方向向量：[x, y]表示移动方向
    snake_direction = [1, 0]  # 初始向右移动
    
    # 初始化食物位置
    food_pos = [GRID_WIDTH//4, GRID_HEIGHT//4]
    
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
        
        # 将新头部添加到蛇身列表的开头
        # insert(0, new_head) 在列表开头插入新元素
        snake_pos.insert(0, new_head)
        # 删除尾部
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