"""
# 扫雷游戏 v1 - Python基础版本

## 版本特点
- 展示Python程序的基本要素
- 演示全局变量和局部变量的使用
- 说明模块和可执行文件的区别

## 关键概念说明

### 1. Python程序基本要素
- **关键字**：
  - `def`: 用于定义函数
  - `if`: 用于条件判断
  - `#!`: 用于指定解释器路径
- **函数**：使用def关键字定义的可重用代码块
- **变量**：
  - 全局变量：在整个模块中都可以访问
  - 局部变量：只在定义它的函数内部可见

### 2. 模块和可执行文件
- **模块**：可以被其他Python程序导入的代码文件
- **可执行文件**：可以直接运行的Python程序
- **`__name__`变量**：
  - 当文件作为主程序运行时，值为`"__main__"`
  - 当文件被导入时，值为模块名

### 3. 代码结构
- **导入语句**：使用`import`导入需要的模块
- **全局变量**：在模块级别定义的变量
- **函数定义**：使用`def`关键字定义函数
- **主程序入口**：使用`if __name__ == "__main__"`判断

## 学习要点
- Python程序的基本结构
- 变量的作用域
- 模块化编程的概念
- 代码的可重用性
"""

#!/bin/env python

# 导入必要的库
# pygame: 用于创建游戏的Python库
import pygame

#####################################################
# 学习内容：
# 1. python 程序的基本要素
#   - 关键字：def, if, #!
#   - 函数
#   - 变量：全局、局部
# 2. 区分模块和可执行文件
#####################################################


# 全局变量 user_name 在整个模块中都可以访问
# 全局变量在模块级别定义，可以被模块中的所有函数访问
user_name = 'Hugo'

# --- global function ---
def main():
    """
    主函数：演示局部变量的使用
    """
    # 局部变量 greetings 只在 main 函数内部可见
    # 局部变量在函数内部定义，只能在函数内部访问
    greetings = 'Hello, I am '
    print('############################')
    print(greetings + user_name)


# 这行代码的作用是检查当前脚本是否作为主程序运行。
# 如果脚本被直接运行，`__name__` 变量的值将是 `"__main__"`，此时 `main()` 函数会被调用。
# 如果脚本被导入到其他模块中，`__name__` 变量的值将是模块的名称，此时 `main()` 函数不会被调用。
if __name__ == "__main__":
    main()
    # print(greetings)  # 这行代码会报错，因为 greetings 是局部变量，在 main 函数外部不可见

# 总结：
# 1. 全局变量 user_name 在整个模块中都可以访问。
# 2. 局部变量 greetings 只在 main 函数内部可见。
# 3. 使用 if __name__ == "__main__": 来区分模块和可执行文件。
# 4. 代码结构清晰，便于理解 Python 程序的基本要素。
