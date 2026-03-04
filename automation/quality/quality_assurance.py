#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量保障系统
用于降低人为错误，确保代码质量和系统可靠性
"""

import os
import sys
import argparse
import json
import subprocess
from datetime import datetime

class QualityAssuranceSystem:
    def __init__(self):
        self.qa_results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def run_quality_checks(self, source_dir, config_file=None):
        """运行质量检查"""
        print(f"Running quality checks on {source_dir}...")
        
        try:
            # 加载配置
            config = self._load_config(config_file)
            
            # 运行各项质量检查
            checks = config.get('checks', {
                'code_review': True,
                'tests': True,
                'static_analysis': True,
                'security_scan': True,
                'performance_test': False
            })
            
            # 运行代码审查
            if checks.get('code_review'):
                self._run_code_review(source_dir)
            
            # 运行测试
            if checks.get('tests'):
                self._run_tests(source_dir)
            
            # 运行静态分析
            if checks.get('static_analysis'):
                self._run_static_analysis(source_dir)
            
            # 运行安全扫描
            if checks.get('security_scan'):
                self._run_security_scan(source_dir)
            
            # 运行性能测试
            if checks.get('performance_test'):
                self._run_performance_test(source_dir)
            
            # 汇总结果
            self._summarize_results()
            
            print("\nQuality assurance checks completed")
            
        except Exception as e:
            self.qa_results['system'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error running quality checks: {e}")
    
    def _load_config(self, config_file):
        """加载配置文件"""
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _run_code_review(self, source_dir):
        """运行代码审查"""
        print("Running code review...")
        
        try:
            # 使用之前创建的代码审查工具
            code_review_script = os.path.join(os.path.dirname(__file__), '../code_review/code_reviewer.py')
            
            if os.path.exists(code_review_script):
                result = subprocess.run(
                    [sys.executable, code_review_script, source_dir, '--output', 'quality_reports'],
                    capture_output=True,
                    text=True
                )
                
                self.qa_results['code_review'] = {
                    'status': 'success' if result.returncode == 0 else 'failed',
                    'output': result.stdout,
                    'error': result.stderr
                }
            else:
                self.qa_results['code_review'] = {
                    'status': 'skipped',
                    'message': 'Code review script not found'
                }
            
        except Exception as e:
            self.qa_results['code_review'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _run_tests(self, source_dir):
        """运行测试"""
        print("Running tests...")
        
        try:
            # 使用之前创建的测试运行器
            test_runner_script = os.path.join(os.path.dirname(__file__), '../test/test_runner.py')
            
            if os.path.exists(test_runner_script):
                result = subprocess.run(
                    [sys.executable, test_runner_script, '--python-tests', source_dir, '--code-quality', source_dir, '--output', 'quality_reports'],
                    capture_output=True,
                    text=True
                )
                
                self.qa_results['tests'] = {
                    'status': 'success' if result.returncode == 0 else 'failed',
                    'output': result.stdout,
                    'error': result.stderr
                }
            else:
                self.qa_results['tests'] = {
                    'status': 'skipped',
                    'message': 'Test runner script not found'
                }
            
        except Exception as e:
            self.qa_results['tests'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _run_static_analysis(self, source_dir):
        """运行静态分析"""
        print("Running static analysis...")
        
        try:
            # 简单的静态分析实现
            issues = []
            
            # 检查文件权限
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path):
                        # 检查文件大小
                        file_size = os.path.getsize(file_path)
                        if file_size > 1024 * 1024:  # 大于1MB
                            issues.append({
                                'type': 'file_too_large',
                                'message': f'File {file_path} is too large ({file_size} bytes)',
                                'severity': 'warning'
                            })
            
            self.qa_results['static_analysis'] = {
                'status': 'success',
                'issues': issues
            }
            
        except Exception as e:
            self.qa_results['static_analysis'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _run_security_scan(self, source_dir):
        """运行安全扫描"""
        print("Running security scan...")
        
        try:
            # 简单的安全扫描实现
            security_issues = []
            
            # 检查敏感信息
            sensitive_patterns = [
                r'api[_\s-]?key',
                r'password',
                r'secret',
                r'token',
                r'credential',
                r'private[_\s-]?key'
            ]
            
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file.endswith(('.py', '.c', '.h', '.cpp', '.hpp', '.js', '.json', '.yaml', '.yml')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                                for pattern in sensitive_patterns:
                                    import re
                                    if re.search(pattern, content, re.IGNORECASE):
                                        security_issues.append({
                                            'type': 'potential_security_issue',
                                            'message': f'Potential sensitive information found in {file_path}',
                                            'severity': 'warning'
                                        })
                                        break
                        except:
                            pass
            
            self.qa_results['security_scan'] = {
                'status': 'success',
                'issues': security_issues
            }
            
        except Exception as e:
            self.qa_results['security_scan'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _run_performance_test(self, source_dir):
        """运行性能测试"""
        print("Running performance test...")
        
        try:
            # 简单的性能测试实现
            performance_results = []
            
            # 检查Python文件的执行时间
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file.endswith('.py') and not file.startswith('test_'):
                        file_path = os.path.join(root, file)
                        try:
                            import time
                            start_time = time.time()
                            
                            # 执行文件（如果是可执行的）
                            result = subprocess.run(
                                [sys.executable, file_path],
                                capture_output=True,
                                text=True,
                                timeout=10  # 10秒超时
                            )
                            
                            execution_time = time.time() - start_time
                            
                            if execution_time > 5:
                                performance_results.append({
                                    'type': 'performance_issue',
                                    'message': f'File {file_path} took too long to execute ({execution_time:.2f} seconds)',
                                    'severity': 'warning'
                                })
                                
                        except subprocess.TimeoutExpired:
                            performance_results.append({
                                'type': 'performance_issue',
                                'message': f'File {file_path} timed out after 10 seconds',
                                'severity': 'error'
                            })
                        except:
                            pass
            
            self.qa_results['performance_test'] = {
                'status': 'success',
                'results': performance_results
            }
            
        except Exception as e:
            self.qa_results['performance_test'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _summarize_results(self):
        """汇总结果"""
        summary = {
            'total_checks': len(self.qa_results),
            'passed_checks': 0,
            'failed_checks': 0,
            'skipped_checks': 0,
            'total_issues': 0
        }
        
        for check_name, check_result in self.qa_results.items():
            status = check_result.get('status')
            if status == 'success':
                summary['passed_checks'] += 1
                # 计算问题数量
                if 'issues' in check_result:
                    summary['total_issues'] += len(check_result['issues'])
                elif 'results' in check_result:
                    summary['total_issues'] += len(check_result['results'])
            elif status == 'failed':
                summary['failed_checks'] += 1
            elif status == 'skipped':
                summary['skipped_checks'] += 1
        
        self.qa_results['summary'] = summary
    
    def generate_qa_report(self, output_dir):
        """生成质量保障报告"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成JSON报告
        report_file = os.path.join(output_dir, f'quality_report_{self.timestamp}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.qa_results, f, indent=2, ensure_ascii=False)
        
        # 生成文本报告
        text_report_file = os.path.join(output_dir, f'quality_report_{self.timestamp}.txt')
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(f"Quality Assurance Report - {self.timestamp}\n")
            f.write("=" * 60 + "\n")
            
            if 'summary' in self.qa_results:
                summary = self.qa_results['summary']
                f.write("Summary:\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total checks: {summary.get('total_checks', 0)}\n")
                f.write(f"Passed checks: {summary.get('passed_checks', 0)}\n")
                f.write(f"Failed checks: {summary.get('failed_checks', 0)}\n")
                f.write(f"Skipped checks: {summary.get('skipped_checks', 0)}\n")
                f.write(f"Total issues found: {summary.get('total_issues', 0)}\n")
            
            f.write("\nDetailed Results:\n")
            f.write("-" * 40 + "\n")
            
            for check_name, check_result in self.qa_results.items():
                if check_name != 'summary':
                    f.write(f"\n{check_name.upper()}:\n")
                    f.write(f"Status: {check_result.get('status')}\n")
                    
                    if 'message' in check_result:
                        f.write(f"Message: {check_result['message']}\n")
                    
                    if 'issues' in check_result:
                        f.write(f"Issues found: {len(check_result['issues'])}\n")
                        for issue in check_result['issues']:
                            f.write(f"  [{issue.get('severity')}] {issue.get('message')} ({issue.get('type')})\n")
                    
                    if 'results' in check_result:
                        f.write(f"Results: {len(check_result['results'])}\n")
                        for result in check_result['results']:
                            f.write(f"  [{result.get('severity')}] {result.get('message')} ({result.get('type')})\n")
                    
                    if 'output' in check_result and check_result['output']:
                        f.write("Output:\n")
                        f.write(check_result['output'] + "\n")
                    
                    if 'error' in check_result and check_result['error']:
                        f.write("Error:\n")
                        f.write(check_result['error'] + "\n")
        
        print(f"Quality assurance report generated: {report_file}")
        print(f"Text report generated: {text_report_file}")
    
    def create_quality_config(self, output_file):
        """创建质量保障配置模板"""
        config = {
            "name": "Quality Assurance Configuration",
            "description": "Configuration for quality assurance checks",
            "checks": {
                "code_review": true,
                "tests": true,
                "static_analysis": true,
                "security_scan": true,
                "performance_test": false
            },
            "thresholds": {
                "max_file_size": 1048576,  # 1MB
                "max_execution_time": 5,  # 5 seconds
                "max_issues": 10
            },
            "exclude_patterns": [
                "__pycache__",
                "venv",
                "node_modules",
                ".git"
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"Quality assurance configuration created: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Quality Assurance System')
    parser.add_argument('source_dir', help='Source directory to check')
    parser.add_argument('--config', help='Configuration file')
    parser.add_argument('--create-config', help='Create a configuration template')
    parser.add_argument('--output', default='quality_reports', help='Output directory for reports')
    
    args = parser.parse_args()
    
    qa_system = QualityAssuranceSystem()
    
    if args.create_config:
        qa_system.create_quality_config(args.create_config)
    else:
        qa_system.run_quality_checks(args.source_dir, args.config)
        qa_system.generate_qa_report(args.output)

if __name__ == "__main__":
    main()
