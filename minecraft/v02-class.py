"""
# 扫雷游戏 v2 - 类基础版本

## 版本特点
- 引入面向对象编程概念
- 实现基本的游戏循环
- 添加游戏退出机制

## 关键概念说明

### 1. 面向对象编程
- **类（Class）**：
  - 使用`class`关键字定义
  - 用于封装数据和方法
  - 可以创建多个实例
- **对象（Object）**：
  - 类的实例
  - 包含具体的数据
  - 可以调用类的方法
- **方法（Method）**：
  - 使用`def`关键字定义
  - 第一个参数是`self`
  - 可以访问类的属性

### 2. 游戏循环
- **初始化**：
  - 使用`pygame.init()`初始化
  - 设置窗口标题和大小
  - 创建游戏窗口
- **主循环**：
  - 处理游戏事件
  - 更新游戏状态
  - 绘制游戏画面
- **退出机制**：
  - 处理退出事件
  - 清理游戏资源

### 3. 代码组织
- **类的结构**：
  - `__init__`方法：初始化
  - `run`方法：游戏主循环
  - 成员变量：存储游戏状态
- **资源管理**：
  - 初始化Pygame
  - 创建游戏窗口
  - 清理资源

## 学习要点
- 面向对象编程基础
- 游戏循环的实现
- 事件处理机制
- 资源管理方法
"""

#!/bin/env python

# 导入必要的库
# pygame: 用于创建游戏的Python库
import pygame


# --- Game class ---
class MineCraft():
    """
    扫雷游戏类：管理游戏的主要逻辑
    """
    def __init__(self, name='MineCraft'):
        """
        初始化方法：创建游戏窗口和设置基本属性
        参数：
            name: 游戏窗口标题
        """
        # Initialize Pygame
        pygame.init()
        # Set up the game title
        pygame.display.set_caption(name)
        # 类的成员变量
        self.screen = pygame.display.set_mode((600, 600))  # 创建600x600的游戏窗口
        self.running = True  # 控制游戏循环的标志

    def run(self):
        """
        运行方法：实现游戏主循环
        """
        while self.running:
            # 处理游戏事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 如果点击窗口关闭按钮
                    self.running = False  # 设置退出标志
            self.screen.fill((255,255,255))  # 用白色填充背景
            pygame.display.flip()  # 更新显示
        # --- Exit Game ---
        pygame.quit()  # 清理Pygame资源

# --- global function ---
def main():
    """
    主函数：创建游戏实例并运行游戏
    """
    # 创建类的实例
    game = MineCraft('Hugo MineCraft')
    # 调用成员函数
    game.run()

# Python的特殊语法：当这个文件被直接运行时（而不是被导入时）
# __name__ 变量的值会是 '__main__'
if __name__ == "__main__":
    main()
