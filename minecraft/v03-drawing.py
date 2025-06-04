"""
# 扫雷游戏 v3 - 绘图基础版本

## 版本特点
- 添加图像加载和处理功能
- 实现基本的游戏界面绘制
- 完善游戏循环和事件处理

## 关键概念说明

### 1. Pygame图像处理
- **图像加载**：
  - 使用`pygame.image.load()`加载图像
  - 支持多种图像格式（GIF、PNG等）
  - 可以批量加载多个图像
- **图像绘制**：
  - 使用`screen.blit()`在屏幕上绘制图像
  - 可以指定绘制位置
  - 支持图像缩放和旋转

### 2. 文件路径处理
- **路径操作**：
  - 使用`os.path`模块处理文件路径
  - `os.path.dirname()`获取目录路径
  - `os.path.join()`连接路径
- **资源管理**：
  - 组织游戏资源文件
  - 批量加载图像资源
  - 管理图像对象

### 3. 游戏界面
- **界面绘制**：
  - 清除屏幕背景
  - 绘制游戏元素
  - 更新显示
- **私有方法**：
  - 使用下划线前缀（`_`）
  - 封装内部实现细节
  - 提供清晰的接口

## 学习要点
- 图像资源的加载和管理
- 文件路径的处理方法
- 游戏界面的绘制技术
- 面向对象编程的实践
"""

#!/bin/env python

# 导入必要的库
# os: 提供与操作系统交互的功能
# pygame: 用于创建游戏的Python库
import os
import pygame



# --- 学习内容 ---
# 1. Pygame初始化
#    - 使用pygame.init()初始化所有Pygame模块
#    - 设置游戏窗口标题和大小
#    - 创建游戏主循环和退出机制

# 2. 图像加载和处理
#    - 使用os.path处理文件路径
#    - 批量加载多个图像文件
#    - 使用pygame.image.load()加载图像
#    - 使用screen.blit()在屏幕上绘制图像

# 3. 游戏循环
#    - 实现基本的游戏主循环
#    - 处理退出事件
#    - 使用screen.fill()清除屏幕
#    - 使用pygame.display.flip()更新显示

# 4. 面向对象编程
#    - 创建MineCraft类封装游戏逻辑
#    - 实现初始化和运行方法
#    - 使用私有方法（_draw）处理内部逻辑

# --- 实践练习 ---
# 1. 完善游戏初始界面的绘制
#    - 创建初始界面：_create_board
#    - 绘制界面



# --- Game class ---
class MineCraft():
    """
    扫雷游戏类：管理游戏的主要逻辑和界面绘制
    """
    def __init__(self, name='MineCraft'):
        """
        初始化方法：创建游戏窗口和加载图像资源
        参数：
            name: 游戏窗口标题
        """
        # Initialize Pygame
        pygame.init()
        # Set up the game title
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode((600, 600))
        self.running = True
        script_dir = os.path.dirname(__file__)
        images = [os.path.join(script_dir, 'img', f'{num}.gif') for num in range(0, 14)]
        print(f'images path list: {images}')
        # load the images
        self.images = [pygame.image.load(img) for img in images]
        print(f'images object list: {self.images}')

    def run(self):
        """
        运行方法：实现游戏主循环
        """
        while self.running:
            # --- Stop loop if cmd+q ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # --- Draw Game Elements ---
            self._draw()
        # end while loop

        # --- Exit Game ---
        pygame.quit()

    def _create_board(self):
        """
        创建游戏初始界面
        TODO：实现游戏板的创建逻辑
        """
        # TODO：创建游戏初始界面
        pass


    def _draw(self):
        """
        绘制方法：在屏幕上绘制游戏元素
        """
        self.screen.fill((255,255,255)) # Fill background
        # draw image at coords (0,0)
        self.screen.blit(self.images[9], (0,0))
        # TODO: 绘制初始界面


        pygame.display.flip()


# --- global function ---
def main():
    """
    主函数：创建游戏实例并运行游戏
    """
    game = MineCraft('Hugo MineCraft')
    game.run()



if __name__ == "__main__":
    main()
