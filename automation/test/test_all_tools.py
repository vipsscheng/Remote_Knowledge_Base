#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本
用于测试和优化所有实施的功能
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class ToolTester:
    def __init__(self):
        self.test_results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def test_code_generator(self):
        """测试代码生成工具"""
        print("Testing code generator...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 测试Python代码生成
        try:
            # 使用绝对路径
            code_generator_path = os.path.join(os.path.dirname(__file__), '..', 'codegen', 'code_generator.py')
            print(f"Code generator path: {code_generator_path}")
            print(f"Script exists: {os.path.exists(code_generator_path)}")
            result = subprocess.run(
                [sys.executable, code_generator_path, 'python', 'test_python_code.py', '--description', 'Test Python code', '--function-name', 'test_function'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Python code generation',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Python code generation',
                'status': 'error',
                'error': str(e)
            })
        
        # 测试C代码生成
        try:
            # 使用绝对路径
            code_generator_path = os.path.join(os.path.dirname(__file__), '../codegen/code_generator.py')
            result = subprocess.run(
                [sys.executable, code_generator_path, 'c', 'test_c_code.c', '--description', 'Test C code', '--function-name', 'test_function'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'C code generation',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'C code generation',
                'status': 'error',
                'error': str(e)
            })
        
        # 检查生成的文件
        if os.path.exists('test_python_code.py'):
            os.remove('test_python_code.py')
        if os.path.exists('test_c_code.c'):
            os.remove('test_c_code.c')
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['code_generator'] = results
        return results
    
    def test_test_runner(self):
        """测试测试运行器"""
        print("Testing test runner...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 创建测试文件
        test_file = 'test_test_runner.py'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('''
def test_addition():
    assert 1 + 1 == 2

def test_subtraction():
    assert 5 - 3 == 2

if __name__ == "__main__":
    test_addition()
    test_subtraction()
    print("All tests passed!")
''')
        
        # 测试运行测试
        try:
            # 使用绝对路径
            test_runner_path = os.path.join(os.path.dirname(__file__), 'test_runner.py')
            result = subprocess.run(
                [sys.executable, test_runner_path, '--python-tests', '.', '--code-quality', '.'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Run tests',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Run tests',
                'status': 'error',
                'error': str(e)
            })
        
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['test_runner'] = results
        return results
    
    def test_deploy_script(self):
        """测试部署脚本"""
        print("Testing deploy script...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 创建测试目录
        test_dir = 'test_deploy_dir'
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, 'test_file.txt'), 'w', encoding='utf-8') as f:
            f.write('Test content')
        
        # 测试创建部署包
        try:
            # 使用绝对路径
            deploy_script_path = os.path.join(os.path.dirname(__file__), '../deploy/deploy_script.py')
            result = subprocess.run(
                [sys.executable, deploy_script_path, '--create-package', test_dir, '--output', 'test_deploy_reports'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Create deployment package',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Create deployment package',
                'status': 'error',
                'error': str(e)
            })
        
        # 清理测试目录
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        if os.path.exists('test_deploy_reports'):
            shutil.rmtree('test_deploy_reports')
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['deploy_script'] = results
        return results
    
    def test_workflow_automator(self):
        """测试工作流自动化工具"""
        print("Testing workflow automator...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 创建测试工作流文件
        workflow_file = 'test_workflow.json'
        with open(workflow_file, 'w', encoding='utf-8') as f:
            json.dump({
                "name": "Test Workflow",
                "description": "Test workflow",
                "steps": [
                    {
                        "name": "Test command",
                        "type": "command",
                        "command": "echo 'Hello, World!'"
                    }
                ]
            }, f, indent=2)
        
        # 测试运行工作流
        try:
            # 使用绝对路径
            workflow_automator_path = os.path.join(os.path.dirname(__file__), '../workflow/workflow_automator.py')
            result = subprocess.run(
                [sys.executable, workflow_automator_path, '--run', workflow_file, '--output', 'test_workflow_reports'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Run workflow',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Run workflow',
                'status': 'error',
                'error': str(e)
            })
        
        # 清理测试文件
        if os.path.exists(workflow_file):
            os.remove(workflow_file)
        if os.path.exists('test_workflow_reports'):
            import shutil
            shutil.rmtree('test_workflow_reports')
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['workflow_automator'] = results
        return results
    
    def test_code_reviewer(self):
        """测试代码审查工具"""
        print("Testing code reviewer...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 创建测试文件
        test_file = 'test_code_review.py'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('''
def test_function():
    x = 1
    y = 2
    return x + y
''')
        
        # 测试代码审查
        try:
            # 使用绝对路径
            code_reviewer_path = os.path.join(os.path.dirname(__file__), '../code_review/code_reviewer.py')
            result = subprocess.run(
                [sys.executable, code_reviewer_path, '.', '--output', 'test_code_review_reports'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Run code review',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Run code review',
                'status': 'error',
                'error': str(e)
            })
        
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists('test_code_review_reports'):
            import shutil
            shutil.rmtree('test_code_review_reports')
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['code_reviewer'] = results
        return results
    
    def test_quality_assurance(self):
        """测试质量保障系统"""
        print("Testing quality assurance system...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 创建测试文件
        test_file = 'test_quality.py'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('''
def test_function():
    return 42
''')
        
        # 测试质量检查
        try:
            # 使用绝对路径
            quality_assurance_path = os.path.join(os.path.dirname(__file__), '../quality/quality_assurance.py')
            result = subprocess.run(
                [sys.executable, quality_assurance_path, '.', '--output', 'test_quality_reports'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Run quality checks',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Run quality checks',
                'status': 'error',
                'error': str(e)
            })
        
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists('test_quality_reports'):
            import shutil
            shutil.rmtree('test_quality_reports')
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['quality_assurance'] = results
        return results
    
    def test_knowledge_manager(self):
        """测试知识库管理工具"""
        print("Testing knowledge manager...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 测试添加知识
        try:
            # 使用绝对路径
            knowledge_manager_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base/knowledge_manager.py')
            result = subprocess.run(
                [sys.executable, knowledge_manager_path, '--base-dir', os.path.join(os.path.expanduser('~'), '技能文件夹', '知识库'), 'add', 'core', 'Test Knowledge', '--content', 'This is a test knowledge item', '--tags', 'test', 'example'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Add knowledge',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Add knowledge',
                'status': 'error',
                'error': str(e)
            })
        
        # 测试列出知识
        try:
            # 使用绝对路径
            knowledge_manager_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base/knowledge_manager.py')
            result = subprocess.run(
                [sys.executable, knowledge_manager_path, '--base-dir', os.path.join(os.path.expanduser('~'), '技能文件夹', '知识库'), 'list'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'List knowledge',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'List knowledge',
                'status': 'error',
                'error': str(e)
            })
        
        # 测试搜索知识
        try:
            # 使用绝对路径
            knowledge_manager_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base/knowledge_manager.py')
            result = subprocess.run(
                [sys.executable, knowledge_manager_path, '--base-dir', os.path.join(os.path.expanduser('~'), '技能文件夹', '知识库'), 'search', 'test'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Search knowledge',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Search knowledge',
                'status': 'error',
                'error': str(e)
            })
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['knowledge_manager'] = results
        return results
    
    def test_version_control(self):
        """测试版本控制工具"""
        print("Testing version control...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 测试初始化版本控制
        try:
            # 使用绝对路径
            version_control_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base/version_control.py')
            result = subprocess.run(
                [sys.executable, version_control_path, '--knowledge-base', os.path.join(os.path.expanduser('~'), '技能文件夹', '知识库'), 'status'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Initialize version control',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Initialize version control',
                'status': 'error',
                'error': str(e)
            })
        
        # 测试提交变更
        try:
            # 使用绝对路径
            version_control_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base/version_control.py')
            result = subprocess.run(
                [sys.executable, version_control_path, '--knowledge-base', os.path.join(os.path.expanduser('~'), '技能文件夹', '知识库'), 'commit', 'Initial commit'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Commit changes',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Commit changes',
                'status': 'error',
                'error': str(e)
            })
        
        # 测试查看版本历史
        try:
            # 使用绝对路径
            version_control_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base/version_control.py')
            result = subprocess.run(
                [sys.executable, version_control_path, '--knowledge-base', os.path.join(os.path.expanduser('~'), '技能文件夹', '知识库'), 'log'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'View version history',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'View version history',
                'status': 'error',
                'error': str(e)
            })
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['version_control'] = results
        return results
    
    def test_model_monitor(self):
        """测试模型监控系统"""
        print("Testing model monitor...")
        results = {
            'status': 'success',
            'tests': []
        }
        
        # 测试监控模型
        try:
            # 使用绝对路径
            model_monitor_path = os.path.join(os.path.dirname(__file__), '../model/model_monitor.py')
            result = subprocess.run(
                [sys.executable, model_monitor_path, 'monitor'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Monitor models',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Monitor models',
                'status': 'error',
                'error': str(e)
            })
        
        # 测试列出模型
        try:
            # 使用绝对路径
            model_monitor_path = os.path.join(os.path.dirname(__file__), '../model/model_monitor.py')
            result = subprocess.run(
                [sys.executable, model_monitor_path, 'list'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'List models',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'List models',
                'status': 'error',
                'error': str(e)
            })
        
        # 测试获取适配策略
        try:
            # 使用绝对路径
            model_monitor_path = os.path.join(os.path.dirname(__file__), '../model/model_monitor.py')
            result = subprocess.run(
                [sys.executable, model_monitor_path, 'strategy', 'gpt-4'],
                capture_output=True,
                text=True
            )
            test_result = {
                'name': 'Get adaptation strategy',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr
            }
            results['tests'].append(test_result)
        except Exception as e:
            results['tests'].append({
                'name': 'Get adaptation strategy',
                'status': 'error',
                'error': str(e)
            })
        
        # 检查是否所有测试都通过
        if all(test['status'] == 'success' for test in results['tests']):
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
        
        self.test_results['model_monitor'] = results
        return results
    
    def run_all_tests(self):
        """运行所有测试"""
        print("Running all tests...")
        print("=" * 60)
        
        # 运行所有测试
        self.test_code_generator()
        self.test_test_runner()
        self.test_deploy_script()
        self.test_workflow_automator()
        self.test_code_reviewer()
        self.test_quality_assurance()
        self.test_knowledge_manager()
        self.test_version_control()
        self.test_model_monitor()
        
        # 生成测试报告
        self.generate_test_report()
    
    def generate_test_report(self):
        """生成测试报告"""
        # 计算总体结果
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        
        for tool, results in self.test_results.items():
            for test in results.get('tests', []):
                total_tests += 1
                if test['status'] == 'success':
                    passed_tests += 1
                elif test['status'] == 'failed':
                    failed_tests += 1
                else:
                    error_tests += 1
        
        # 生成报告
        report = {
            'timestamp': self.timestamp,
            'total_tools': len(self.test_results),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'error_tests': error_tests,
            'tools': self.test_results
        }
        
        # 保存报告
        output_dir = 'test_results'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        report_file = os.path.join(output_dir, f'test_report_{self.timestamp}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 生成文本报告
        text_report_file = os.path.join(output_dir, f'test_report_{self.timestamp}.txt')
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(f"Test Report - {self.timestamp}\n")
            f.write("=" * 60 + "\n")
            f.write(f"Total tools tested: {len(self.test_results)}\n")
            f.write(f"Total tests: {total_tests}\n")
            f.write(f"Passed: {passed_tests}\n")
            f.write(f"Failed: {failed_tests}\n")
            f.write(f"Errors: {error_tests}\n")
            f.write(f"Success rate: {passed_tests / total_tests * 100:.2f}%\n")
            
            f.write("\nDetailed Results:\n")
            f.write("-" * 60 + "\n")
            
            for tool, results in self.test_results.items():
                f.write(f"\n{tool.upper()}:\n")
                f.write(f"Status: {results['status']}\n")
                
                for test in results.get('tests', []):
                    f.write(f"  - {test['name']}: {test['status']}\n")
                    if test.get('error'):
                        f.write(f"    Error: {test['error']}\n")
        
        print(f"\nTest report generated: {report_file}")
        print(f"Text report generated: {text_report_file}")
        print(f"\nTotal tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Errors: {error_tests}")
        print(f"Success rate: {passed_tests / total_tests * 100:.2f}%")

def main():
    print("Starting test script...")
    tester = ToolTester()
    print("Running all tests...")
    tester.run_all_tests()
    print("Test script completed.")

if __name__ == "__main__":
    main()
