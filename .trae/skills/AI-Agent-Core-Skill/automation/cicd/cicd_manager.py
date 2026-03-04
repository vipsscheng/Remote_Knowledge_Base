#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI/CD管理器
用于实现CI/CD流程、自动化部署和工具管理
"""

import os
import sys
import subprocess
import argparse
import json
import platform
import shutil
from datetime import datetime

class CICDManager:
    def __init__(self):
        self.results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.system = platform.system()
    
    def detect_cli_tools(self):
        """检测系统安装的CLI工具"""
        print("Detecting CLI tools...")
        
        tools = {
            # 国际工具
            'code': {'name': 'Visual Studio Code', 'command': 'code', 'type': 'ide'},
            'git': {'name': 'Git', 'command': 'git', 'type': 'version_control'},
            'python': {'name': 'Python', 'command': 'python', 'type': 'interpreter'},
            'npm': {'name': 'npm', 'command': 'npm', 'type': 'package_manager'},
            'docker': {'name': 'Docker', 'command': 'docker', 'type': 'container'},
            'cmake': {'name': 'CMake', 'command': 'cmake', 'type': 'build'},
            'make': {'name': 'Make', 'command': 'make', 'type': 'build'},
            'gcc': {'name': 'GCC', 'command': 'gcc', 'type': 'compiler'},
            'g++': {'name': 'G++', 'command': 'g++', 'type': 'compiler'},
            'clang': {'name': 'Clang', 'command': 'clang', 'type': 'compiler'},
            'javac': {'name': 'Java Compiler', 'command': 'javac', 'type': 'compiler'},
            'node': {'name': 'Node.js', 'command': 'node', 'type': 'interpreter'},
            'pip': {'name': 'pip', 'command': 'pip', 'type': 'package_manager'},
            'yarn': {'name': 'Yarn', 'command': 'yarn', 'type': 'package_manager'},
            'helm': {'name': 'Helm', 'command': 'helm', 'type': 'deployment'},
            'kubectl': {'name': 'kubectl', 'command': 'kubectl', 'type': 'deployment'},
            'ansible': {'name': 'Ansible', 'command': 'ansible', 'type': 'deployment'},
            'terraform': {'name': 'Terraform', 'command': 'terraform', 'type': 'infrastructure'},
            # 国内工具
            'cnpm': {'name': 'cnpm', 'command': 'cnpm', 'type': 'package_manager'},
            'yarncn': {'name': 'Yarn China', 'command': 'yarncn', 'type': 'package_manager'},
            'tencentcloud': {'name': 'Tencent Cloud CLI', 'command': 'tencentcloud', 'type': 'cloud'},
            'aliyun': {'name': 'Alibaba Cloud CLI', 'command': 'aliyun', 'type': 'cloud'},
            'huaweicloud': {'name': 'Huawei Cloud CLI', 'command': 'huaweicloud', 'type': 'cloud'},
            'wenxin-cli': {'name': '文心一言 CLI', 'command': 'wenxin-cli', 'type': 'ai'},
            'xinghuo-cli': {'name': '讯飞星火 CLI', 'command': 'xinghuo-cli', 'type': 'ai'},
            'qwen-cli': {'name': '通义千问 CLI', 'command': 'qwen-cli', 'type': 'ai'},
            'doubao-cli': {'name': '豆包 CLI', 'command': 'doubao-cli', 'type': 'ai'}
        }
        
        detected_tools = []
        
        for tool_name, tool_info in tools.items():
            if self._is_tool_available(tool_info['command']):
                version = self._get_tool_version(tool_info['command'])
                tool_info['version'] = version
                tool_info['available'] = True
                detected_tools.append(tool_info)
                print(f"✓ {tool_info['name']} ({version})")
            else:
                tool_info['available'] = False
                print(f"✗ {tool_info['name']}")
        
        self.results['cli_tools'] = {
            'status': 'success',
            'detected': len(detected_tools),
            'total': len(tools),
            'tools': detected_tools
        }
        
        return detected_tools
    
    def register_ide_tools(self, tools):
        """注册IDE工具"""
        print("Registering IDE tools...")
        
        ide_tools = [tool for tool in tools if tool['type'] == 'ide']
        
        if ide_tools:
            print(f"Registered {len(ide_tools)} IDE tools:")
            for tool in ide_tools:
                print(f"- {tool['name']} ({tool['version']})")
        else:
            print("No IDE tools detected")
        
        self.results['ide_registration'] = {
            'status': 'success',
            'registered': len(ide_tools),
            'tools': ide_tools
        }
        
        return ide_tools
    
    def run_ci_pipeline(self, project_dir):
        """运行CI流水线"""
        print("Running CI pipeline...")
        
        ci_steps = [
            {'name': 'Build', 'command': self._get_build_command(project_dir)},
            {'name': 'Test', 'command': self._get_test_command(project_dir)},
            {'name': 'Analyze', 'command': self._get_analyze_command(project_dir)},
            {'name': 'Package', 'command': self._get_package_command(project_dir)}
        ]
        
        ci_results = []
        success = True
        
        for step in ci_steps:
            print(f"\nRunning {step['name']} step...")
            if step['command']:
                result = self._run_command(step['command'], cwd=project_dir)
                ci_results.append({
                    'name': step['name'],
                    'status': 'success' if result['returncode'] == 0 else 'failed',
                    'output': result['stdout'],
                    'error': result['stderr']
                })
                if result['returncode'] != 0:
                    success = False
                    print(f"{step['name']} step failed")
                    break
            else:
                ci_results.append({
                    'name': step['name'],
                    'status': 'skipped',
                    'output': 'No command specified',
                    'error': ''
                })
                print(f"{step['name']} step skipped")
        
        self.results['ci_pipeline'] = {
            'status': 'success' if success else 'failed',
            'steps': ci_results
        }
        
        return success
    
    def run_cd_pipeline(self, project_dir, target_env):
        """运行CD流水线"""
        print("Running CD pipeline...")
        
        # 导入部署脚本
        deploy_script_path = os.path.join(os.path.dirname(__file__), '..', 'deploy', 'deploy_script.py')
        
        # 创建部署包
        package_output = os.path.join(project_dir, 'deploy_reports')
        package_command = f"{sys.executable} {deploy_script_path} --create-package {project_dir} --output {package_output}"
        
        print("Creating deployment package...")
        package_result = self._run_command(package_command)
        
        if package_result['returncode'] != 0:
            self.results['cd_pipeline'] = {
                'status': 'failed',
                'error': 'Failed to create deployment package'
            }
            return False
        
        # 部署到目标环境
        target_dir = os.path.join(project_dir, f'deployments', target_env)
        backup_dir = os.path.join(project_dir, f'backups', target_env)
        
        # 创建备份
        backup_command = f"{sys.executable} {deploy_script_path} --create-backup {target_dir} --output {package_output}"
        print("Creating backup...")
        backup_result = self._run_command(backup_command)
        
        # 部署
        # 查找生成的部署包
        import glob
        package_files = glob.glob(os.path.join(package_output, 'deployment_*.zip'))
        if not package_files:
            self.results['cd_pipeline'] = {
                'status': 'failed',
                'error': 'No deployment package found'
            }
            return False
        
        package_path = sorted(package_files, key=os.path.getmtime, reverse=True)[0]
        deploy_command = f"{sys.executable} {deploy_script_path} --deploy-local {package_path} {target_dir} --output {package_output}"
        print(f"Deploying to {target_env} environment...")
        deploy_result = self._run_command(deploy_command)
        
        if deploy_result['returncode'] != 0:
            # 回滚
            rollback_command = f"{sys.executable} {deploy_script_path} --rollback {target_dir} {backup_dir} --output {package_output}"
            print("Deployment failed, rolling back...")
            self._run_command(rollback_command)
            
            self.results['cd_pipeline'] = {
                'status': 'failed',
                'error': 'Deployment failed and rolled back'
            }
            return False
        
        # 运行部署后测试
        test_command = f"{sys.executable} {deploy_script_path} --run-tests {target_dir} --output {package_output}"
        print("Running post-deployment tests...")
        test_result = self._run_command(test_command)
        
        self.results['cd_pipeline'] = {
            'status': 'success' if test_result['returncode'] == 0 else 'failed',
            'deployment_dir': target_dir,
            'package_path': package_path
        }
        
        return test_result['returncode'] == 0
    
    def generate_report(self, output_dir):
        """生成报告"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成JSON报告
        report_file = os.path.join(output_dir, f'cicd_report_{self.timestamp}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # 生成文本报告
        text_report_file = os.path.join(output_dir, f'cicd_report_{self.timestamp}.txt')
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(f"CI/CD Report - {self.timestamp}\n")
            f.write("=" * 80 + "\n")
            
            # 系统信息
            f.write("\nSYSTEM INFO\n")
            f.write("-" * 40 + "\n")
            f.write(f"System: {self.system}\n")
            f.write(f"Platform: {platform.platform()}\n")
            f.write(f"Python: {platform.python_version()}\n")
            
            # CLI工具
            if 'cli_tools' in self.results:
                f.write("\nCLI TOOLS\n")
                f.write("-" * 40 + "\n")
                f.write(f"Detected: {self.results['cli_tools']['detected']}/{self.results['cli_tools']['total']}\n")
                f.write("\nAvailable tools:\n")
                for tool in self.results['cli_tools']['tools']:
                    f.write(f"  - {tool['name']} ({tool['version']})\n")
            
            # IDE注册
            if 'ide_registration' in self.results:
                f.write("\nIDE REGISTRATION\n")
                f.write("-" * 40 + "\n")
                f.write(f"Registered: {self.results['ide_registration']['registered']}\n")
                for tool in self.results['ide_registration']['tools']:
                    f.write(f"  - {tool['name']} ({tool['version']})\n")
            
            # CI流水线
            if 'ci_pipeline' in self.results:
                f.write("\nCI PIPELINE\n")
                f.write("-" * 40 + "\n")
                f.write(f"Status: {self.results['ci_pipeline']['status']}\n")
                for step in self.results['ci_pipeline']['steps']:
                    f.write(f"  - {step['name']}: {step['status']}\n")
            
            # CD流水线
            if 'cd_pipeline' in self.results:
                f.write("\nCD PIPELINE\n")
                f.write("-" * 40 + "\n")
                f.write(f"Status: {self.results['cd_pipeline']['status']}\n")
                if 'deployment_dir' in self.results['cd_pipeline']:
                    f.write(f"Deployment directory: {self.results['cd_pipeline']['deployment_dir']}\n")
                if 'error' in self.results['cd_pipeline']:
                    f.write(f"Error: {self.results['cd_pipeline']['error']}\n")
        
        print(f"\nReport generated: {report_file}")
        print(f"Text report generated: {text_report_file}")
    
    def _is_tool_available(self, command):
        """检查工具是否可用"""
        try:
            if self.system == 'Windows':
                # Windows系统
                result = subprocess.run(['where', command], capture_output=True, text=True)
                return result.returncode == 0
            else:
                # Unix系统
                result = subprocess.run(['which', command], capture_output=True, text=True)
                return result.returncode == 0
        except:
            return False
    
    def _get_tool_version(self, command):
        """获取工具版本"""
        try:
            if command == 'code':
                result = subprocess.run([command, '--version'], capture_output=True, text=True)
                return result.stdout.strip().split('\n')[0]
            elif command in ['git', 'python', 'npm', 'docker', 'cmake', 'make', 'gcc', 'g++', 'clang', 'javac', 'node', 'pip', 'yarn', 'helm', 'kubectl', 'ansible', 'terraform']:
                result = subprocess.run([command, '--version'], capture_output=True, text=True)
                return result.stdout.strip().split('\n')[0]
            else:
                return 'Unknown'
        except:
            return 'Unknown'
    
    def _run_command(self, command, cwd=None):
        """运行命令"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except Exception as e:
            return {
                'returncode': 1,
                'stdout': '',
                'stderr': str(e)
            }
    
    def _get_build_command(self, project_dir):
        """获取构建命令"""
        if os.path.exists(os.path.join(project_dir, 'CMakeLists.txt')):
            return 'cmake . && cmake --build .'
        elif os.path.exists(os.path.join(project_dir, 'package.json')):
            return 'npm install && npm run build'
        elif os.path.exists(os.path.join(project_dir, 'setup.py')):
            return 'pip install -e .'
        elif os.path.exists(os.path.join(project_dir, 'Makefile')):
            return 'make'
        else:
            return None
    
    def _get_test_command(self, project_dir):
        """获取测试命令"""
        if os.path.exists(os.path.join(project_dir, 'package.json')):
            return 'npm test'
        elif os.path.exists(os.path.join(project_dir, 'setup.py')):
            return 'pytest'
        elif os.path.exists(os.path.join(project_dir, 'Makefile')):
            return 'make test'
        else:
            return None
    
    def _get_analyze_command(self, project_dir):
        """获取分析命令"""
        if os.path.exists(os.path.join(project_dir, 'package.json')):
            return 'npm run lint'
        elif os.path.exists(os.path.join(project_dir, 'setup.py')):
            return 'flake8 .'
        else:
            return None
    
    def _get_package_command(self, project_dir):
        """获取打包命令"""
        if os.path.exists(os.path.join(project_dir, 'package.json')):
            return 'npm run build'
        elif os.path.exists(os.path.join(project_dir, 'setup.py')):
            return 'python setup.py sdist bdist_wheel'
        else:
            return None

def main():
    parser = argparse.ArgumentParser(description='CI/CD Manager')
    parser.add_argument('--detect-tools', action='store_true', help='Detect CLI tools')
    parser.add_argument('--register-ide', action='store_true', help='Register IDE tools')
    parser.add_argument('--run-ci', help='Run CI pipeline on project directory')
    parser.add_argument('--run-cd', nargs=2, help='Run CD pipeline on project directory and target environment')
    parser.add_argument('--output', default='cicd_reports', help='Output directory for reports')
    parser.add_argument('--full', action='store_true', help='Run full CI/CD pipeline with tool detection')
    
    args = parser.parse_args()
    
    manager = CICDManager()
    
    if args.full:
        # 运行完整流程
        tools = manager.detect_cli_tools()
        manager.register_ide_tools(tools)
        if args.run_ci:
            success = manager.run_ci_pipeline(args.run_ci)
            if success and args.run_cd:
                project_dir, target_env = args.run_cd
                manager.run_cd_pipeline(project_dir, target_env)
    else:
        # 运行指定流程
        if args.detect_tools:
            manager.detect_cli_tools()
        
        if args.register_ide:
            tools = manager.detect_cli_tools()
            manager.register_ide_tools(tools)
        
        if args.run_ci:
            manager.run_ci_pipeline(args.run_ci)
        
        if args.run_cd:
            project_dir, target_env = args.run_cd
            manager.run_cd_pipeline(project_dir, target_env)
    
    # 生成报告
    manager.generate_report(args.output)

if __name__ == "__main__":
    main()