"""
# 贪吃蛇游戏 v1 - 基础显示版本

## 关键概念说明

### 1. Python基础语法
- **导入语句**：使用 `import` 关键字导入需要的库
- **变量定义**：使用赋值运算符 `=` 定义变量
- **整除运算符**：`//` 返回除法运算的整数部分
- **条件语句**：使用 `if/elif/else` 进行条件判断
- **循环语句**：使用 `while` 和 `for` 进行循环
- **函数定义**：使用 `def` 关键字定义函数
- **特殊变量**：`__name__` 用于判断文件是否被直接运行

### 2. Pygame库核心概念
- **初始化**：`pygame.init()` 初始化所有Pygame模块
- **颜色系统**：使用RGB格式 (红, 绿, 蓝)，每个分量范围0-255
- **显示窗口**：使用 `set_mode()` 创建游戏窗口
- **事件系统**：处理用户输入和系统事件
- **绘图系统**：使用各种绘图函数在屏幕上绘制图形
- **游戏循环**：控制游戏的主要流程
- **帧率控制**：使用 `Clock` 对象控制游戏速度

### 3. 数据结构
- **列表（List）**：用于存储蛇身体的位置坐标
- **坐标系统**：使用二维坐标 [x, y] 表示位置
- **矩形对象**：使用 `Rect` 类表示游戏中的矩形区域

### 4. 游戏开发概念
- **游戏循环**：持续运行的主循环，处理输入、更新状态、渲染画面
- **事件处理**：响应用户输入和系统事件
- **屏幕刷新**：使用 `flip()` 更新显示
- **碰撞检测**：通过坐标系统检测物体间的碰撞

## 游戏控制
- 按 ESC 键退出游戏
- 点击窗口关闭按钮退出游戏
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
pygame.display.set_caption('Snake Game v1 - Basic Display')

# 设置游戏时钟
# Clock对象用于控制游戏的帧率
clock = pygame.time.Clock()

def main():
    """
    主函数：实现基本的游戏循环和显示功能
    """
    # 初始化蛇的位置（静态显示）
    # 使用列表存储蛇身体的每个部分的位置
    # 每个位置是一个包含[x, y]坐标的列表
    snake_pos = [[GRID_WIDTH//2, GRID_HEIGHT//2]]
    
    # 初始化食物位置（静态显示）
    # 食物位置用[x, y]坐标表示
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