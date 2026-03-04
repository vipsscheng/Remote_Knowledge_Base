#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识版本控制工具
用于跟踪知识库条目的变更历史和版本管理
"""

import os
import sys
import argparse
import json
import shutil
import subprocess
from datetime import datetime

class VersionControl:
    def __init__(self, knowledge_base_dir):
        self.knowledge_base_dir = knowledge_base_dir
        self.repo_dir = os.path.join(knowledge_base_dir, '.version_control')
        self.history_dir = os.path.join(self.repo_dir, 'history')
        self.current_version = '1.0.0'
        
        # 初始化版本控制目录
        self._init_repo()
    
    def _init_repo(self):
        """初始化版本控制仓库"""
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)
            os.makedirs(self.history_dir)
            
            # 创建初始版本信息
            initial_version = {
                'version': '1.0.0',
                'timestamp': datetime.now().isoformat(),
                'author': 'AI Agent Core Skill',
                'message': 'Initial version'
            }
            
            with open(os.path.join(self.repo_dir, 'version.json'), 'w', encoding='utf-8') as f:
                json.dump(initial_version, f, indent=2, ensure_ascii=False)
            
            # 创建版本历史文件
            with open(os.path.join(self.repo_dir, 'history.json'), 'w', encoding='utf-8') as f:
                json.dump([initial_version], f, indent=2, ensure_ascii=False)
            
            print("Initialized version control repository")
        else:
            # 加载当前版本
            with open(os.path.join(self.repo_dir, 'version.json'), 'r', encoding='utf-8') as f:
                version_info = json.load(f)
                self.current_version = version_info['version']
            
            print(f"Loaded version control repository (current version: {self.current_version})")
    
    def commit(self, message, author='AI Agent Core Skill'):
        """提交变更"""
        # 计算新版本号
        new_version = self._increment_version(self.current_version)
        
        # 创建版本快照
        snapshot_dir = os.path.join(self.history_dir, new_version)
        if not os.path.exists(snapshot_dir):
            os.makedirs(snapshot_dir)
        
        # 复制知识库内容到快照
        for root, dirs, files in os.walk(self.knowledge_base_dir):
            # 跳过版本控制目录
            if '.version_control' in root:
                continue
            
            # 创建目标目录
            rel_path = os.path.relpath(root, self.knowledge_base_dir)
            target_dir = os.path.join(snapshot_dir, rel_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # 复制文件
            for file in files:
                if file.endswith('.md'):
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(target_dir, file)
                    shutil.copy2(src_file, dst_file)
        
        # 创建版本信息
        version_info = {
            'version': new_version,
            'timestamp': datetime.now().isoformat(),
            'author': author,
            'message': message
        }
        
        # 更新版本信息
        with open(os.path.join(self.repo_dir, 'version.json'), 'w', encoding='utf-8') as f:
            json.dump(version_info, f, indent=2, ensure_ascii=False)
        
        # 更新版本历史
        with open(os.path.join(self.repo_dir, 'history.json'), 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        history.append(version_info)
        
        with open(os.path.join(self.repo_dir, 'history.json'), 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        # 更新当前版本
        self.current_version = new_version
        
        print(f"Committed changes as version {new_version}")
        print(f"Message: {message}")
        return new_version
    
    def log(self):
        """查看版本历史"""
        with open(os.path.join(self.repo_dir, 'history.json'), 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        print("Version history:")
        print("-" * 60)
        
        for version in reversed(history):
            print(f"Version: {version['version']}")
            print(f"Date: {version['timestamp']}")
            print(f"Author: {version['author']}")
            print(f"Message: {version['message']}")
            print()
    
    def checkout(self, version):
        """切换到指定版本"""
        # 检查版本是否存在
        snapshot_dir = os.path.join(self.history_dir, version)
        if not os.path.exists(snapshot_dir):
            print(f"Error: Version {version} not found")
            return False
        
        # 备份当前状态
        backup_dir = os.path.join(self.repo_dir, 'backup')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 清理备份目录
        for file in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        
        # 备份当前文件
        for root, dirs, files in os.walk(self.knowledge_base_dir):
            # 跳过版本控制目录
            if '.version_control' in root:
                continue
            
            # 创建备份目录
            rel_path = os.path.relpath(root, self.knowledge_base_dir)
            target_dir = os.path.join(backup_dir, rel_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # 复制文件
            for file in files:
                if file.endswith('.md'):
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(target_dir, file)
                    shutil.copy2(src_file, dst_file)
        
        # 恢复指定版本
        for root, dirs, files in os.walk(snapshot_dir):
            rel_path = os.path.relpath(root, snapshot_dir)
            target_dir = os.path.join(self.knowledge_base_dir, rel_path)
            
            # 确保目标目录存在
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # 复制文件
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)
        
        # 更新当前版本信息
        with open(os.path.join(self.repo_dir, 'history.json'), 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        version_info = next((v for v in history if v['version'] == version), None)
        if version_info:
            with open(os.path.join(self.repo_dir, 'version.json'), 'w', encoding='utf-8') as f:
                json.dump(version_info, f, indent=2, ensure_ascii=False)
            
            self.current_version = version
            print(f"Checked out version {version}")
            print(f"Message: {version_info['message']}")
            return True
        else:
            print(f"Error: Version {version} not found in history")
            return False
    
    def diff(self, version1, version2):
        """比较两个版本的差异"""
        # 检查版本是否存在
        snapshot_dir1 = os.path.join(self.history_dir, version1)
        snapshot_dir2 = os.path.join(self.history_dir, version2)
        
        if not os.path.exists(snapshot_dir1):
            print(f"Error: Version {version1} not found")
            return False
        
        if not os.path.exists(snapshot_dir2):
            print(f"Error: Version {version2} not found")
            return False
        
        # 使用diff命令比较
        try:
            result = subprocess.run(
                ['diff', '-r', snapshot_dir1, snapshot_dir2],
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                print(f"Differences between version {version1} and {version2}:")
                print(result.stdout)
            else:
                print(f"No differences between version {version1} and {version2}")
            
            return True
        except Exception as e:
            print(f"Error comparing versions: {e}")
            return False
    
    def status(self):
        """查看当前状态"""
        # 加载当前版本
        with open(os.path.join(self.repo_dir, 'version.json'), 'r', encoding='utf-8') as f:
            version_info = json.load(f)
        
        print("Current status:")
        print("-" * 60)
        print(f"Current version: {version_info['version']}")
        print(f"Last updated: {version_info['timestamp']}")
        print(f"Author: {version_info['author']}")
        print(f"Message: {version_info['message']}")
        
        # 检查是否有未提交的变更
        changes = self._detect_changes()
        if changes:
            print("\nUncommitted changes:")
            for change in changes:
                print(f"- {change}")
        else:
            print("\nNo uncommitted changes")
    
    def _detect_changes(self):
        """检测未提交的变更"""
        changes = []
        
        # 检查当前版本的快照
        current_snapshot = os.path.join(self.history_dir, self.current_version)
        if not os.path.exists(current_snapshot):
            return changes
        
        # 比较文件
        for root, dirs, files in os.walk(self.knowledge_base_dir):
            # 跳过版本控制目录
            if '.version_control' in root:
                continue
            
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.knowledge_base_dir)
                    snapshot_file = os.path.join(current_snapshot, rel_path)
                    
                    if not os.path.exists(snapshot_file):
                        changes.append(f"Added: {rel_path}")
                    else:
                        # 比较文件内容
                        with open(file_path, 'r', encoding='utf-8') as f1:
                            content1 = f1.read()
                        with open(snapshot_file, 'r', encoding='utf-8') as f2:
                            content2 = f2.read()
                        
                        if content1 != content2:
                            changes.append(f"Modified: {rel_path}")
        
        # 检查删除的文件
        for root, dirs, files in os.walk(current_snapshot):
            for file in files:
                if file.endswith('.md'):
                    rel_path = os.path.relpath(os.path.join(root, file), current_snapshot)
                    current_file = os.path.join(self.knowledge_base_dir, rel_path)
                    if not os.path.exists(current_file):
                        changes.append(f"Deleted: {rel_path}")
        
        return changes
    
    def _increment_version(self, version):
        """递增版本号"""
        parts = version.split('.')
        if len(parts) != 3:
            return '1.0.0'
        
        major, minor, patch = map(int, parts)
        patch += 1
        
        if patch >= 10:
            patch = 0
            minor += 1
            
            if minor >= 10:
                minor = 0
                major += 1
        
        return f"{major}.{minor}.{patch}"

def main():
    # 获取当前用户目录
    import os
    user_home = os.path.expanduser('~')
    default_knowledge_base = os.path.join(user_home, '技能文件夹', '知识库')
    
    parser = argparse.ArgumentParser(description='Knowledge Version Control')
    parser.add_argument('--knowledge-base', default=default_knowledge_base, help='Knowledge base directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Commit
    commit_parser = subparsers.add_parser('commit', help='Commit changes')
    commit_parser.add_argument('message', help='Commit message')
    commit_parser.add_argument('--author', default='AI Agent Core Skill', help='Author')
    
    # Log
    log_parser = subparsers.add_parser('log', help='View version history')
    
    # Checkout
    checkout_parser = subparsers.add_parser('checkout', help='Checkout a version')
    checkout_parser.add_argument('version', help='Version to checkout')
    
    # Diff
    diff_parser = subparsers.add_parser('diff', help='Compare versions')
    diff_parser.add_argument('version1', help='First version')
    diff_parser.add_argument('version2', help='Second version')
    
    # Status
    status_parser = subparsers.add_parser('status', help='View current status')
    
    args = parser.parse_args()
    
    vc = VersionControl(args.knowledge_base)
    
    if args.command == 'commit':
        vc.commit(args.message, args.author)
    
    elif args.command == 'log':
        vc.log()
    
    elif args.command == 'checkout':
        vc.checkout(args.version)
    
    elif args.command == 'diff':
        vc.diff(args.version1, args.version2)
    
    elif args.command == 'status':
        vc.status()

if __name__ == "__main__":
    main()
