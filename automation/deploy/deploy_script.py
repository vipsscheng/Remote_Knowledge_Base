#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署脚本
用于自动部署项目和管理版本
"""

import os
import sys
import subprocess
import argparse
import json
import shutil
from datetime import datetime

class DeployScript:
    def __init__(self):
        self.deploy_results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def create_deployment_package(self, source_dir, output_dir):
        """创建部署包"""
        print(f"Creating deployment package from {source_dir}...")
        
        try:
            # 确保输出目录存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 计算版本号
            version = self._get_version()
            package_name = f"deployment_{version}_{self.timestamp}"
            package_path = os.path.join(output_dir, package_name)
            
            # 创建部署包目录
            os.makedirs(package_path)
            
            # 复制文件
            self._copy_files(source_dir, package_path)
            
            # 创建版本信息文件
            version_info = {
                'version': version,
                'timestamp': self.timestamp,
                'source_directory': source_dir,
                'files': self._list_files(package_path)
            }
            
            with open(os.path.join(package_path, 'version_info.json'), 'w', encoding='utf-8') as f:
                json.dump(version_info, f, indent=2, ensure_ascii=False)
            
            # 创建压缩包
            archive_path = shutil.make_archive(package_path, 'zip', package_path)
            
            # 清理临时目录
            shutil.rmtree(package_path)
            
            self.deploy_results['package'] = {
                'status': 'success',
                'package_name': package_name,
                'archive_path': archive_path,
                'version': version,
                'file_count': len(version_info['files'])
            }
            
            print(f"Deployment package created: {archive_path}")
            
        except Exception as e:
            self.deploy_results['package'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error creating deployment package: {e}")
    
    def deploy_to_local(self, package_path, target_dir):
        """部署到本地目录"""
        print(f"Deploying to local directory {target_dir}...")
        
        try:
            # 确保目标目录存在
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # 解压部署包
            shutil.unpack_archive(package_path, target_dir)
            
            # 记录部署信息
            self.deploy_results['local_deployment'] = {
                'status': 'success',
                'target_directory': target_dir,
                'package_path': package_path,
                'timestamp': self.timestamp
            }
            
            print(f"Successfully deployed to {target_dir}")
            
        except Exception as e:
            self.deploy_results['local_deployment'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error deploying to local directory: {e}")
    
    def run_post_deployment_tests(self, deployment_dir):
        """运行部署后测试"""
        print(f"Running post-deployment tests in {deployment_dir}...")
        
        try:
            # 检查关键文件是否存在
            required_files = ['README.md', 'version_info.json']
            missing_files = []
            
            for file in required_files:
                file_path = os.path.join(deployment_dir, file)
                if not os.path.exists(file_path):
                    missing_files.append(file)
            
            # 运行基本测试
            test_results = {
                'missing_files': missing_files,
                'directory_exists': os.path.exists(deployment_dir),
                'file_count': len([f for f in os.listdir(deployment_dir) if os.path.isfile(os.path.join(deployment_dir, f))])
            }
            
            self.deploy_results['post_deployment_tests'] = {
                'status': 'success' if not missing_files else 'warning',
                'results': test_results
            }
            
            print("Post-deployment tests completed")
            
        except Exception as e:
            self.deploy_results['post_deployment_tests'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error running post-deployment tests: {e}")
    
    def rollback_deployment(self, deployment_dir, backup_dir):
        """回滚部署"""
        print(f"Rolling back deployment in {deployment_dir}...")
        
        try:
            # 确保备份目录存在
            if not os.path.exists(backup_dir):
                print("Backup directory not found, cannot rollback")
                self.deploy_results['rollback'] = {
                    'status': 'error',
                    'error': 'Backup directory not found'
                }
                return
            
            # 清理当前部署
            if os.path.exists(deployment_dir):
                shutil.rmtree(deployment_dir)
            
            # 从备份恢复
            shutil.copytree(backup_dir, deployment_dir)
            
            self.deploy_results['rollback'] = {
                'status': 'success',
                'deployment_dir': deployment_dir,
                'backup_dir': backup_dir
            }
            
            print(f"Successfully rolled back to backup from {backup_dir}")
            
        except Exception as e:
            self.deploy_results['rollback'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error rolling back deployment: {e}")
    
    def create_backup(self, source_dir, backup_dir):
        """创建备份"""
        print(f"Creating backup of {source_dir}...")
        
        try:
            # 确保备份目录存在
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # 创建备份子目录
            backup_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            backup_path = os.path.join(backup_dir, f'backup_{backup_timestamp}')
            
            # 复制文件
            shutil.copytree(source_dir, backup_path)
            
            self.deploy_results['backup'] = {
                'status': 'success',
                'backup_path': backup_path,
                'timestamp': backup_timestamp
            }
            
            print(f"Backup created: {backup_path}")
            
        except Exception as e:
            self.deploy_results['backup'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error creating backup: {e}")
    
    def generate_deploy_report(self, output_dir):
        """生成部署报告"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成JSON报告
        report_file = os.path.join(output_dir, f'deploy_report_{self.timestamp}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.deploy_results, f, indent=2, ensure_ascii=False)
        
        # 生成文本报告
        text_report_file = os.path.join(output_dir, f'deploy_report_{self.timestamp}.txt')
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(f"Deployment Report - {self.timestamp}\n")
            f.write("=" * 60 + "\n")
            
            for step, results in self.deploy_results.items():
                f.write(f"\n{step.upper()} STEP\n")
                f.write("-" * 40 + "\n")
                
                if 'status' in results:
                    f.write(f"Status: {results['status']}\n")
                
                for key, value in results.items():
                    if key != 'status' and key != 'output' and key != 'error':
                        f.write(f"{key}: {value}\n")
                
                if 'output' in results:
                    f.write("\nOutput:\n")
                    f.write(results['output'] + "\n")
                
                if 'error' in results:
                    f.write("\nError:\n")
                    f.write(results['error'] + "\n")
        
        print(f"Deployment report generated: {report_file}")
        print(f"Text report generated: {text_report_file}")
    
    def _get_version(self):
        """获取版本号"""
        # 从版本文件读取版本号
        version_file = os.path.join(os.getcwd(), 'VERSION')
        if os.path.exists(version_file):
            with open(version_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return '1.0.0'
    
    def _copy_files(self, source_dir, target_dir):
        """复制文件"""
        for root, dirs, files in os.walk(source_dir):
            # 跳过不需要的目录
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'node_modules']]
            
            # 创建目标目录
            rel_path = os.path.relpath(root, source_dir)
            target_path = os.path.join(target_dir, rel_path)
            if rel_path != '.':
                os.makedirs(target_path, exist_ok=True)
            
            # 复制文件
            for file in files:
                # 跳过不需要的文件
                if file.endswith(('.pyc', '.swp', '.tmp')):
                    continue
                
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_path, file)
                shutil.copy2(src_file, dst_file)
    
    def _list_files(self, directory):
        """列出目录中的所有文件"""
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), directory)
                files.append(rel_path)
        return files

def main():
    parser = argparse.ArgumentParser(description='Deployment Script')
    parser.add_argument('--create-package', help='Source directory to create deployment package')
    parser.add_argument('--deploy-local', nargs=2, help='Deployment package and target directory')
    parser.add_argument('--run-tests', help='Directory to run post-deployment tests')
    parser.add_argument('--rollback', nargs=2, help='Deployment directory and backup directory')
    parser.add_argument('--create-backup', nargs=2, help='Source directory and backup directory')
    parser.add_argument('--output', default='deploy_reports', help='Output directory for reports')
    
    args = parser.parse_args()
    
    deployer = DeployScript()
    
    if args.create_package:
        deployer.create_deployment_package(args.create_package, args.output)
    
    if args.deploy_local:
        package_path, target_dir = args.deploy_local
        deployer.deploy_to_local(package_path, target_dir)
    
    if args.run_tests:
        deployer.run_post_deployment_tests(args.run_tests)
    
    if args.rollback:
        deployment_dir, backup_dir = args.rollback
        deployer.rollback_deployment(deployment_dir, backup_dir)
    
    if args.create_backup:
        source_dir, backup_dir = args.create_backup
        deployer.create_backup(source_dir, backup_dir)
    
    deployer.generate_deploy_report(args.output)

if __name__ == "__main__":
    main()
