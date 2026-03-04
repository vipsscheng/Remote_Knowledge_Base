#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试安装过程
用于检查安装脚本的各个步骤是否正常工作
"""

import os
import sys
import json

print("Testing installation process...")
print("=" * 60)

# 测试1: 检查当前目录
print(f"Current directory: {os.getcwd()}")

# 测试2: 检查标准工作流程.MD文件
md_file = os.path.join(os.path.dirname(__file__), '标准工作流程.MD')
print(f"MD file exists: {os.path.exists(md_file)}")

# 测试3: 检查用户目录
user_home = os.path.expanduser('~')
print(f"User home directory: {user_home}")
print(f"User home exists: {os.path.exists(user_home)}")

# 测试4: 尝试创建技能文件夹
skill_folder = os.path.join(user_home, '技能文件夹')
print(f"Skill folder path: {skill_folder}")

# 测试5: 尝试创建目录
print("\nAttempting to create directories...")
try:
    if not os.path.exists(skill_folder):
        os.makedirs(skill_folder)
        print(f"✓ Created skill folder: {skill_folder}")
    else:
        print(f"✓ Skill folder already exists: {skill_folder}")
    
except Exception as e:
    print(f"✗ Failed to create skill folder: {e}")

# 测试6: 检查权限
print("\nChecking permissions...")
try:
    test_file = os.path.join(skill_folder, 'test.txt')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    print("✓ Write permission granted")
except Exception as e:
    print(f"✗ Write permission denied: {e}")

print("=" * 60)
print("Test completed.")
