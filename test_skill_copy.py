#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试技能复制脚本
用于手动复制技能到Trae国际版和国内版目录
"""

import os
import shutil

# 技能信息
skill_name = 'AI-Agent-Core-Skill'
skill_source = os.path.join(os.path.dirname(__file__), '.trae', 'skills', skill_name)

# Trae国际版目录
trae_dir = os.path.join(os.path.expanduser('~'), '.trae')
skills_dir = os.path.join(trae_dir, 'skills')
skill_target_intl = os.path.join(skills_dir, skill_name)

# Trae国内版目录
trae_cn_dir = os.path.join(os.path.expanduser('~'), '.trae-cn')
skills_cn_dir = os.path.join(trae_cn_dir, 'skills')
skill_target_cn = os.path.join(skills_cn_dir, skill_name)

print("Testing skill copy functionality...")
print(f"Skill source: {skill_source}")
print(f"Skill source exists: {os.path.exists(skill_source)}")

# 确保目标目录存在
print("\nEnsuring target directories exist...")
for directory in [skills_dir, skills_cn_dir]:
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directory {directory}: {e}")
    else:
        print(f"Directory already exists: {directory}")

# 复制技能到国际版
try:
    if os.path.exists(skill_source):
        if os.path.exists(skill_target_intl):
            shutil.rmtree(skill_target_intl)
        shutil.copytree(skill_source, skill_target_intl)
        print(f"\nCopied skill to Trae International: {skill_target_intl}")
    else:
        print("\nSkill source not found!")
except Exception as e:
    print(f"\nError copying to Trae International: {e}")

# 复制技能到国内版
try:
    if os.path.exists(skill_source):
        if os.path.exists(skill_target_cn):
            shutil.rmtree(skill_target_cn)
        shutil.copytree(skill_source, skill_target_cn)
        print(f"\nCopied skill to Trae CN: {skill_target_cn}")
    else:
        print("\nSkill source not found!")
except Exception as e:
    print(f"\nError copying to Trae CN: {e}")

print("\nTest completed!")