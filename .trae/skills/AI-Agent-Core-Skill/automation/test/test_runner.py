#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行器
用于自动运行测试和验证代码质量
"""

import os
import sys
import subprocess
import argparse
import json
from datetime import datetime

class TestRunner:
    def __init__(self):
        self.test_results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def run_python_tests(self, test_dir):
        """运行Python测试"""
        print(f"Running Python tests in {test_dir}...")
        
        try:
            # 使用pytest运行测试
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', test_dir, '-v', '--tb=short'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            # 解析测试结果
            output = result.stdout
            error = result.stderr
            
            # 提取测试统计信息
            test_count = 0
            passed_count = 0
            failed_count = 0
            
            for line in output.split('\n'):
                if 'test_' in line and ('PASSED' in line or 'FAILED' in line):
                    test_count += 1
                    if 'PASSED' in line:
                        passed_count += 1
                    else:
                        failed_count += 1
            
            self.test_results['python'] = {
                'status': 'success' if result.returncode == 0 else 'failed',
                'returncode': result.returncode,
                'output': output,
                'error': error,
                'test_count': test_count,
                'passed_count': passed_count,
                'failed_count': failed_count
            }
            
            print(f"Python tests completed: {passed_count} passed, {failed_count} failed")
            
        except Exception as e:
            self.test_results['python'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error running Python tests: {e}")
    
    def run_c_tests(self, test_dir):
        """运行C语言测试"""
        print(f"Running C tests in {test_dir}...")
        
        try:
            # 编译测试文件
            test_files = []
            for root, dirs, files in os.walk(test_dir):
                for file in files:
                    if file.endswith('.c'):
                        test_files.append(os.path.join(root, file))
            
            if not test_files:
                print("No C test files found")
                self.test_results['c'] = {
                    'status': 'skipped',
                    'message': 'No C test files found'
                }
                return
            
            # 编译并运行每个测试文件
            test_count = 0
            passed_count = 0
            failed_count = 0
            output = ""
            
            for test_file in test_files:
                test_count += 1
                test_name = os.path.splitext(os.path.basename(test_file))[0]
                executable = f"{test_name}_test.exe"
                
                # 编译
                compile_result = subprocess.run(
                    ['gcc', test_file, '-o', executable],
                    capture_output=True,
                    text=True
                )
                
                if compile_result.returncode != 0:
                    failed_count += 1
                    output += f"\n{test_file}: COMPILE FAILED\n{compile_result.stderr}"
                    continue
                
                # 运行
                run_result = subprocess.run(
                    [executable],
                    capture_output=True,
                    text=True
                )
                
                if run_result.returncode == 0:
                    passed_count += 1
                    output += f"\n{test_file}: PASSED\n{run_result.stdout}"
                else:
                    failed_count += 1
                    output += f"\n{test_file}: FAILED\n{run_result.stdout}\n{run_result.stderr}"
                
                # 清理可执行文件
                if os.path.exists(executable):
                    os.remove(executable)
            
            self.test_results['c'] = {
                'status': 'success' if failed_count == 0 else 'failed',
                'test_count': test_count,
                'passed_count': passed_count,
                'failed_count': failed_count,
                'output': output
            }
            
            print(f"C tests completed: {passed_count} passed, {failed_count} failed")
            
        except Exception as e:
            self.test_results['c'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error running C tests: {e}")
    
    def run_code_quality_checks(self, source_dir):
        """运行代码质量检查"""
        print(f"Running code quality checks in {source_dir}...")
        
        try:
            # 检查Python代码质量
            python_files = []
            c_files = []
            
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
                    elif file.endswith('.c') or file.endswith('.h'):
                        c_files.append(os.path.join(root, file))
            
            quality_results = {}
            
            # 检查Python代码
            if python_files:
                # 检查语法错误
                syntax_errors = []
                for py_file in python_files:
                    result = subprocess.run(
                        [sys.executable, '-m', 'py_compile', py_file],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        syntax_errors.append(f"{py_file}: {result.stderr}")
                
                quality_results['python'] = {
                    'file_count': len(python_files),
                    'syntax_errors': syntax_errors
                }
            
            # 检查C代码
            if c_files:
                # 检查语法错误
                syntax_errors = []
                for c_file in c_files:
                    result = subprocess.run(
                        ['gcc', '-fsyntax-only', c_file],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        syntax_errors.append(f"{c_file}: {result.stderr}")
                
                quality_results['c'] = {
                    'file_count': len(c_files),
                    'syntax_errors': syntax_errors
                }
            
            self.test_results['code_quality'] = quality_results
            print("Code quality checks completed")
            
        except Exception as e:
            self.test_results['code_quality'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error running code quality checks: {e}")
    
    def generate_report(self, output_dir):
        """生成测试报告"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成JSON报告
        report_file = os.path.join(output_dir, f'test_report_{self.timestamp}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        # 生成文本报告
        text_report_file = os.path.join(output_dir, f'test_report_{self.timestamp}.txt')
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(f"Test Report - {self.timestamp}\n")
            f.write("=" * 60 + "\n")
            
            for test_type, results in self.test_results.items():
                f.write(f"\n{test_type.upper()} TESTS\n")
                f.write("-" * 40 + "\n")
                
                if 'status' in results:
                    f.write(f"Status: {results['status']}\n")
                
                if 'test_count' in results:
                    f.write(f"Total tests: {results['test_count']}\n")
                    f.write(f"Passed: {results.get('passed_count', 0)}\n")
                    f.write(f"Failed: {results.get('failed_count', 0)}\n")
                
                if 'output' in results:
                    f.write("\nOutput:\n")
                    f.write(results['output'] + "\n")
                
                if 'error' in results:
                    f.write("\nError:\n")
                    f.write(results['error'] + "\n")
        
        print(f"Test report generated: {report_file}")
        print(f"Text report generated: {text_report_file}")

def main():
    parser = argparse.ArgumentParser(description='Test Runner')
    parser.add_argument('--python-tests', help='Python test directory')
    parser.add_argument('--c-tests', help='C test directory')
    parser.add_argument('--code-quality', help='Source code directory for quality checks')
    parser.add_argument('--output', default='test_reports', help='Output directory for reports')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.python_tests:
        runner.run_python_tests(args.python_tests)
    
    if args.c_tests:
        runner.run_c_tests(args.c_tests)
    
    if args.code_quality:
        runner.run_code_quality_checks(args.code_quality)
    
    runner.generate_report(args.output)

if __name__ == "__main__":
    main()
