#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动自我进化系统
用于启动和管理自我进化系统的运行
"""

import sys
import os

# 添加自动化工具目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'automation'))

from evolution.self_evolution import SelfEvolutionSystem

def main():
    print("启动自我进化系统...")
    print("=" * 60)
    
    # 创建自我进化系统实例
    system = SelfEvolutionSystem()
    
    # 启动系统
    system.start()
    
    print("自我进化系统已在后台启动")
    print("系统正在监控和分析...")
    print("自我进化系统将自动运行，无需人工干预")
    print("=" * 60)
    
    # 保持脚本运行
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n正在停止自我进化系统...")
        system.stop()
        print("自我进化系统已停止")

if __name__ == "__main__":
    main()
