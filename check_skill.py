#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查技能是否已经被Trae IDE识别
"""

import os
import sys
import json

print("Checking skill status...")
print("=" * 60)

# 检查用户技能目录
user_skill_dir = os.path.join(os.path.expanduser('~'), '.trae', 'skills', 'AI-Agent-Core-Skill')
print(f"User skill directory: {user_skill_dir}")
print(f"Skill directory exists: {os.path.exists(user_skill_dir)}")

# 检查技能配置文件
skill_json = os.path.join(user_skill_dir, 'skill.json')
print(f"\nChecking skill.json:")
if os.path.exists(skill_json):
    print("✓ skill.json exists")
    with open(skill_json, 'r', encoding='utf-8') as f:
        try:
            config = json.load(f)
            print(f"  Skill name: {config.get('name')}")
            print(f"  Version: {config.get('version')}")
            print(f"  Description: {config.get('description')}")
        except json.JSONDecodeError:
            print("✗ Invalid skill.json format")
else:
    print("✗ skill.json not found")

# 检查SKILL.md文件
skill_md = os.path.join(user_skill_dir, 'SKILL.md')
print(f"\nChecking SKILL.md:")
if os.path.exists(skill_md):
    print("✓ SKILL.md exists")
else:
    print("✗ SKILL.md not found")

# 检查核心文件
print(f"\nChecking core files:")
core_files = ['start_skill.bat', 'md_installer.py']
for file in core_files:
    file_path = os.path.join(user_skill_dir, file)
    if os.path.exists(file_path):
        print(f"✓ {file} exists")
    else:
        print(f"✗ {file} not found")

# 检查依赖目录
print(f"\nChecking dependency directories:")
dirs = ['automation', 'knowledge_base']
for dir_name in dirs:
    dir_path = os.path.join(user_skill_dir, dir_name)
    if os.path.exists(dir_path):
        print(f"✓ {dir_name} directory exists")
    else:
        print(f"✗ {dir_name} directory not found")

print("\n" + "=" * 60)
print("Skill check completed.")
print("\nTo make the skill available in Trae IDE:")
print("1. Restart Trae IDE to refresh the skill list")
print("2. Check if the skill appears in the skill management interface")
print("3. If not, try manually adding the skill directory in Trae IDE settings")
