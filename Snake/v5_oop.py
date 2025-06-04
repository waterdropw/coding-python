"""
# 贪吃蛇游戏 v5 - 面向对象版本

## 版本特点
- 使用面向对象编程重构游戏
- 将游戏逻辑分解为多个类
- 提高了代码的可维护性和可扩展性
- 实现了更清晰的代码结构

## 关键概念说明

### 1. 面向对象编程
- **类（Class）**：将相关的数据和方法组织在一起
- **对象（Object）**：类的实例，包含具体的数据
- **封装**：将数据和方法封装在类中
- **继承**：可以基于现有类创建新类（本版本未使用）

### 2. 游戏类结构
- **Snake类**：
  - 管理蛇的位置和移动
  - 处理碰撞检测
  - 控制蛇的生长
  - 绘制蛇的外观
- **Food类**：
  - 管理食物的位置
  - 生成新的食物
  - 绘制食物的外观
- **Game类**：
  - 管理游戏主循环
  - 处理用户输入
  - 控制游戏状态
  - 协调各个组件

### 3. 类的方法
- **初始化方法**：`__init__` 设置初始状态
- **实例方法**：操作对象的具体行为
- **私有方法**：内部使用的辅助方法
- **公共接口**：供其他类调用的方法

### 4. 代码组织
- **模块化**：将功能分解为独立的类
- **职责分离**：每个类负责特定的功能
- **接口设计**：定义清晰的类间交互方式
- **状态管理**：通过类属性管理游戏状态

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

## 面向对象设计优势
- 代码更容易维护和扩展
- 逻辑更清晰，结构更合理
- 便于添加新功能
- 提高代码重用性
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

class Snake:
    """
    蛇类：管理蛇的所有属性和行为
    """
    def __init__(self):
        """
        初始化方法：创建蛇的初始状态
        """
        self.reset()
    
    def reset(self):
        """
        重置方法：将蛇恢复到初始状态
        """
        # 初始化蛇的位置和方向
        self.positions = [[GRID_WIDTH//2, GRID_HEIGHT//2]]
        self.direction = [1, 0]  # 初始向右移动
    
    def move(self):
        """
        移动方法：根据当前方向移动蛇
        返回：
            新的头部位置 [x, y]
        """
        # 计算新的头部位置
        new_head = [
            self.positions[0][0] + self.direction[0],
            self.positions[0][1] + self.direction[1]
        ]
        # 将新头部添加到蛇身列表的开头
        self.positions.insert(0, new_head)
        return new_head
    
    def grow(self):
        """
        生长方法：让蛇变长（不删除尾部）
        """
        pass  # 不删除尾部即可实现增长
    
    def check_collision(self, new_head):
        """
        碰撞检测方法：检查是否发生碰撞
        参数：
            new_head: 新的头部位置 [x, y]
        返回：
            True: 发生碰撞
            False: 未发生碰撞
        """
        # 检查是否撞墙
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return True
        # 检查是否撞到自己
        if new_head in self.positions:
            return True
        return False
    
    def draw(self, screen):
        """
        绘制方法：在屏幕上绘制蛇
        参数：
            screen: Pygame屏幕对象
        """
        # 遍历蛇身体的每个部分并绘制
        for pos in self.positions:
            rect = pygame.Rect(
                pos[0] * GRID_SIZE,
                pos[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, GREEN, rect)

class Food:
    """
    食物类：管理食物的属性和行为
    """
    def __init__(self):
        """
        初始化方法：创建食物的初始状态
        """
        self.position = [0, 0]
        self.generate()
    
    def generate(self, snake_positions=None):
        """
        生成方法：生成新的食物位置
        参数：
            snake_positions: 蛇身体的位置列表，用于避免食物生成在蛇身上
        """
        if snake_positions is None:
            snake_positions = []
        while True:
            # 生成随机位置
            self.position = [
                random.randint(0, GRID_WIDTH-1),
                random.randint(0, GRID_HEIGHT-1)
            ]
            # 确保食物不会生成在蛇身上
            if self.position not in snake_positions:
                break
    
    def draw(self, screen):
        """
        绘制方法：在屏幕上绘制食物
        参数：
            screen: Pygame屏幕对象
        """
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(screen, RED, rect)

class Game:
    """
    游戏类：管理整个游戏的运行
    """
    def __init__(self):
        """
        初始化方法：创建游戏窗口和初始化游戏状态
        """
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game v5 - OOP')
        
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        
        # 初始化字体
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        
        # 创建游戏对象
        self.snake = Snake()
        self.food = Food()
        
        # 初始化游戏状态
        self.score = 0
        self.paused = False
    
    def draw_text(self, text, font, color, x, y):
        """
        文本绘制方法：在屏幕上绘制文本
        参数：
            text: 要显示的文本
            font: 字体对象
            color: 文本颜色
            x, y: 文本中心位置
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def show_start_screen(self):
        """
        开始界面方法：显示游戏开始界面
        """
        while True:
            self.screen.fill(BLACK)
            self.draw_text("Snake Game", self.title_font, GREEN, WINDOW_WIDTH//2, WINDOW_HEIGHT//3)
            self.draw_text("Press SPACE to Start", self.font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            self.draw_text("Press ESC to Quit", self.font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def show_game_over_screen(self):
        """
        结束界面方法：显示游戏结束界面
        返回：
            True: 重新开始游戏
            False: 退出游戏
        """
        while True:
            self.screen.fill(BLACK)
            self.draw_text("Game Over", self.title_font, RED, WINDOW_WIDTH//2, WINDOW_HEIGHT//3)
            self.draw_text(f"Score: {self.score}", self.font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            self.draw_text("Press SPACE to Restart", self.font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3)
            self.draw_text("Press ESC to Quit", self.font, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT*3//4)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
    
    def handle_events(self):
        """
        事件处理方法：处理游戏事件
        """
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
                    self.paused = not self.paused
                # 只有在非暂停状态下才处理方向键
                elif not self.paused:
                    if event.key == pygame.K_UP and self.snake.direction != [0, 1]:
                        self.snake.direction = [0, -1]
                    elif event.key == pygame.K_DOWN and self.snake.direction != [0, -1]:
                        self.snake.direction = [0, 1]
                    elif event.key == pygame.K_LEFT and self.snake.direction != [1, 0]:
                        self.snake.direction = [-1, 0]
                    elif event.key == pygame.K_RIGHT and self.snake.direction != [-1, 0]:
                        self.snake.direction = [1, 0]
    
    def update(self):
        """
        更新方法：更新游戏状态
        返回：
            True: 游戏继续
            False: 游戏结束
        """
        if not self.paused:
            # 移动蛇并获取新的头部位置
            new_head = self.snake.move()
            
            # 检查碰撞
            if self.snake.check_collision(new_head):
                return False
            
            # 检查是否吃到食物
            if new_head == self.food.position:
                self.score += 10
                self.food.generate(self.snake.positions)
            else:
                self.snake.positions.pop()
            
            return True
        return True
    
    def draw(self):
        """
        绘制方法：绘制游戏画面
        """
        # 清空屏幕
        self.screen.fill(BLACK)
        
        # 绘制食物和蛇
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        
        # 显示分数
        self.draw_text(f'Score: {self.score}', self.font, WHITE, 70, 20)
        
        # 如果游戏暂停，显示暂停文字
        if self.paused:
            self.draw_text("PAUSED", self.title_font, BLUE, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        
        # 更新显示
        pygame.display.flip()
    
    def run(self):
        """
        运行方法：运行游戏主循环
        """
        while True:
            # 显示开始界面
            self.show_start_screen()
            
            # 重置游戏状态
            self.snake.reset()
            self.food.generate()
            self.score = 0
            self.paused = False
            
            # 游戏主循环
            running = True
            while running:
                self.handle_events()
                running = self.update()
                self.draw()
                self.clock.tick(10)
            
            # 显示游戏结束界面
            if not self.show_game_over_screen():
                break

# Python的特殊语法：当这个文件被直接运行时（而不是被导入时）
# __name__ 变量的值会是 '__main__'
if __name__ == '__main__':
    # 创建游戏对象并运行游戏
    game = Game()
    game.run() 