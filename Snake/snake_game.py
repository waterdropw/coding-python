import pygame  # 导入pygame库，用于创建游戏
import random  # 导入random库，用于生成随机数
import sys    # 导入sys库，用于系统相关操作（如退出游戏）

# 初始化 Pygame
# 这一步是必须的，在使用pygame的任何功能之前都需要初始化
pygame.init()

# 定义游戏中使用的颜色
# 颜色使用RGB格式，每个值范围是0-255
BLACK = (0, 0, 0)      # 黑色，用于背景
WHITE = (255, 255, 255) # 白色，用于文字
RED = (255, 0, 0)      # 红色，用于食物
GREEN = (0, 255, 0)    # 绿色，用于蛇身

# 游戏基本设置
WINDOW_WIDTH = 800     # 游戏窗口宽度
WINDOW_HEIGHT = 600    # 游戏窗口高度
GRID_SIZE = 20         # 网格大小（蛇和食物的大小）
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE   # 计算网格宽度数量
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE # 计算网格高度数量

# 创建游戏窗口
# set_mode()函数创建一个指定大小的窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')  # 设置窗口标题

# 设置游戏时钟
# 用于控制游戏帧率，确保游戏速度一致
clock = pygame.time.Clock()

def main():
    # 初始化蛇的位置和方向
    # snake_pos是一个列表，存储蛇身体的每个部分的位置
    # 初始位置在屏幕中央
    snake_pos = [[GRID_WIDTH//2, GRID_HEIGHT//2]]
    # snake_direction表示蛇的移动方向
    # [1, 0]表示向右移动，[0, 1]表示向下，[-1, 0]表示向左，[0, -1]表示向上
    snake_direction = [1, 0]  # 初始向右移动
    
    # 生成第一个食物
    # random.randint()生成指定范围内的随机整数
    food_pos = [random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)]
    
    # TODO: 添加游戏分数变量
    # score = 0
    
    # 游戏主循环
    while True:
        # 处理游戏事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果点击窗口关闭按钮
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 如果按下键盘
                if event.key == pygame.K_ESCAPE:  # 如果按下ESC键
                    pygame.quit()
                    sys.exit()
                # TODO: 添加方向键控制
                # 使用pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
                # 更新snake_direction的值
        
        # TODO: 更新蛇的位置
        # 1. 根据snake_direction计算新的头部位置
        # 2. 将新位置添加到snake_pos列表的开头
        # 3. 如果吃到食物，不删除尾部；否则删除尾部
        
        # TODO: 添加碰撞检测
        # 1. 检查是否撞到墙壁
        # 2. 检查是否撞到自己
        # 3. 检查是否吃到食物
        
        # 清空屏幕
        screen.fill(BLACK)
        
        # 绘制食物
        food_rect = pygame.Rect(
            food_pos[0] * GRID_SIZE,  # 将网格坐标转换为像素坐标
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
        
        # TODO: 显示分数
        # 使用pygame.font模块创建文字
        
        # 更新显示
        # flip()函数将绘制的内容显示到屏幕上
        pygame.display.flip()
        
        # 控制游戏速度
        # tick(10)表示每秒运行10帧
        clock.tick(10)

if __name__ == '__main__':
    main() 