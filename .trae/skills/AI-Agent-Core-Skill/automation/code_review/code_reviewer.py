#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能代码审查工具
用于自动检测代码质量问题和提供改进建议
"""

import os
import sys
import argparse
import json
import re
from datetime import datetime

class CodeReviewer:
    def __init__(self):
        self.review_results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def review_code(self, source_dir):
        """审查代码"""
        print(f"Reviewing code in {source_dir}...")
        
        try:
            # 收集文件
            files_to_review = []
            for root, dirs, files in os.walk(source_dir):
                # 跳过不需要的目录
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'node_modules']]
                
                for file in files:
                    if file.endswith(('.py', '.c', '.h', '.cpp', '.hpp')):
                        files_to_review.append(os.path.join(root, file))
            
            # 审查每个文件
            file_results = []
            for file_path in files_to_review:
                print(f"Reviewing file: {file_path}")
                file_result = self._review_file(file_path)
                file_results.append(file_result)
            
            # 汇总结果
            total_issues = sum(len(f.get('issues', [])) for f in file_results)
            total_files = len(file_results)
            files_with_issues = len([f for f in file_results if len(f.get('issues', [])) > 0])
            
            self.review_results['review'] = {
                'status': 'success',
                'total_files': total_files,
                'files_with_issues': files_with_issues,
                'total_issues': total_issues,
                'files': file_results,
                'source_directory': source_dir
            }
            
            print(f"\nCode review completed: {total_issues} issues found in {files_with_issues} out of {total_files} files")
            
        except Exception as e:
            self.review_results['review'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error reviewing code: {e}")
    
    def _review_file(self, file_path):
        """审查单个文件"""
        file_ext = os.path.splitext(file_path)[1]
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # 根据文件类型进行审查
            if file_ext == '.py':
                issues.extend(self._review_python_file(file_path, lines))
            elif file_ext in ['.c', '.h']:
                issues.extend(self._review_c_file(file_path, lines))
            elif file_ext in ['.cpp', '.hpp']:
                issues.extend(self._review_cpp_file(file_path, lines))
            
            return {
                'file_path': file_path,
                'file_extension': file_ext,
                'line_count': len(lines),
                'issues': issues,
                'status': 'clean' if not issues else 'issues_found'
            }
            
        except Exception as e:
            return {
                'file_path': file_path,
                'file_extension': file_ext,
                'issues': [{
                    'severity': 'error',
                    'type': 'review_error',
                    'message': f'Error reviewing file: {str(e)}',
                    'line': 0
                }],
                'status': 'error'
            }
    
    def _review_python_file(self, file_path, lines):
        """审查Python文件"""
        issues = []
        
        # 检查缩进
        for i, line in enumerate(lines, 1):
            # 检查混合缩进（空格和制表符）
            if '\t' in line and ' ' in line[:len(line) - len(line.lstrip())]:
                issues.append({
                    'severity': 'warning',
                    'type': 'indentation',
                    'message': 'Mixed indentation (spaces and tabs)',
                    'line': i
                })
        
        # 检查未使用的导入
        import_lines = [i for i, line in enumerate(lines, 1) if line.strip().startswith('import ') or line.strip().startswith('from ')]
        used_imports = set()
        
        # 简单的导入使用检测
        for line in lines:
            # 提取可能的导入使用
            for imp in re.findall(r'\b([a-zA-Z0-9_]+)\.', line):
                used_imports.add(imp)
        
        for line_num in import_lines:
            line = lines[line_num - 1].strip()
            if line.startswith('import '):
                imp_name = line.split('import ')[1].split(' as ')[0].split('.')[0]
                if imp_name not in used_imports:
                    issues.append({
                        'severity': 'warning',
                        'type': 'unused_import',
                        'message': f'Unused import: {imp_name}',
                        'line': line_num
                    })
            elif line.startswith('from '):
                imp_name = line.split('from ')[1].split(' import ')[0]
                if imp_name.split('.')[0] not in used_imports:
                    issues.append({
                        'severity': 'warning',
                        'type': 'unused_import',
                        'message': f'Unused import: {imp_name}',
                        'line': line_num
                    })
        
        # 检查缺少文档字符串
        if not any('"""' in line or "''" in line for line in lines[:20]):
            issues.append({
                'severity': 'info',
                'type': 'missing_docstring',
                'message': 'Missing module docstring',
                'line': 1
            })
        
        # 检查长行
        for i, line in enumerate(lines, 1):
            if len(line) > 80:
                issues.append({
                    'severity': 'info',
                    'type': 'line_too_long',
                    'message': f'Line too long ({len(line)} characters)',
                    'line': i
                })
        
        return issues
    
    def _review_c_file(self, file_path, lines):
        """审查C文件"""
        issues = []
        
        # 检查缺少头文件保护
        if file_path.endswith('.h'):
            has_header_guard = False
            for line in lines[:20]:
                if '#ifndef' in line or '#pragma once' in line:
                    has_header_guard = True
                    break
            if not has_header_guard:
                issues.append({
                    'severity': 'warning',
                    'type': 'missing_header_guard',
                    'message': 'Missing header guard',
                    'line': 1
                })
        
        # 检查未使用的变量
        # 简单的未使用变量检测
        declared_vars = set()
        used_vars = set()
        
        for i, line in enumerate(lines, 1):
            # 检测变量声明
            var_decl = re.search(r'\b(?:int|char|float|double|void|struct|union|enum)\s+([a-zA-Z0-9_]+)\s*[=;]', line)
            if var_decl:
                declared_vars.add(var_decl.group(1))
            
            # 检测变量使用
            for var in declared_vars:
                if re.search(r'\b' + re.escape(var) + r'\b', line) and '=' not in line:
                    used_vars.add(var)
        
        for var in declared_vars - used_vars:
            issues.append({
                'severity': 'warning',
                'type': 'unused_variable',
                'message': f'Unused variable: {var}',
                'line': 0  # 无法准确确定行号
            })
        
        # 检查长函数
        brace_count = 0
        function_start = 0
        for i, line in enumerate(lines, 1):
            if re.search(r'\b(?:void|int|char|float|double)\s+[a-zA-Z0-9_]+\s*\([^)]*\)\s*\{', line):
                function_start = i
                brace_count = 1
            elif function_start > 0:
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    function_length = i - function_start + 1
                    if function_length > 50:
                        issues.append({
                            'severity': 'info',
                            'type': 'function_too_long',
                            'message': f'Function too long ({function_length} lines)',
                            'line': function_start
                        })
                    function_start = 0
        
        return issues
    
    def _review_cpp_file(self, file_path, lines):
        """审查C++文件"""
        issues = []
        
        # 检查缺少头文件保护
        if file_path.endswith('.hpp'):
            has_header_guard = False
            for line in lines[:20]:
                if '#ifndef' in line or '#pragma once' in line:
                    has_header_guard = True
                    break
            if not has_header_guard:
                issues.append({
                    'severity': 'warning',
                    'type': 'missing_header_guard',
                    'message': 'Missing header guard',
                    'line': 1
                })
        
        # 检查使用using namespace std
        for i, line in enumerate(lines, 1):
            if 'using namespace std;' in line:
                issues.append({
                    'severity': 'warning',
                    'type': 'using_namespace_std',
                    'message': 'Avoid using namespace std; in header files',
                    'line': i
                })
        
        # 检查内存管理
        for i, line in enumerate(lines, 1):
            if 'new ' in line and 'delete' not in line:
                issues.append({
                    'severity': 'info',
                    'type': 'memory_management',
                    'message': 'Potential memory leak (new without delete)',
                    'line': i
                })
        
        return issues
    
    def generate_review_report(self, output_dir):
        """生成审查报告"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成JSON报告
        report_file = os.path.join(output_dir, f'code_review_report_{self.timestamp}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.review_results, f, indent=2, ensure_ascii=False)
        
        # 生成文本报告
        text_report_file = os.path.join(output_dir, f'code_review_report_{self.timestamp}.txt')
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(f"Code Review Report - {self.timestamp}\n")
            f.write("=" * 60 + "\n")
            
            if 'review' in self.review_results:
                review = self.review_results['review']
                f.write(f"Status: {review.get('status')}\n")
                f.write(f"Total files reviewed: {review.get('total_files', 0)}\n")
                f.write(f"Files with issues: {review.get('files_with_issues', 0)}\n")
                f.write(f"Total issues found: {review.get('total_issues', 0)}\n")
                f.write(f"Source directory: {review.get('source_directory')}\n")
                
                if 'files' in review:
                    f.write("\nFiles with issues:\n")
                    f.write("-" * 40 + "\n")
                    
                    for file_result in review['files']:
                        if file_result.get('status') == 'issues_found':
                            f.write(f"\nFile: {file_result.get('file_path')}\n")
                            f.write(f"Extension: {file_result.get('file_extension')}\n")
                            f.write(f"Line count: {file_result.get('line_count')}\n")
                            f.write(f"Issues: {len(file_result.get('issues', []))}\n")
                            
                            if file_result.get('issues'):
                                f.write("\nDetails:\n")
                                for issue in file_result['issues']:
                                    f.write(f"  [{issue.get('severity')}] Line {issue.get('line')}: {issue.get('message')} ({issue.get('type')})\n")
        
        print(f"Code review report generated: {report_file}")
        print(f"Text report generated: {text_report_file}")

def main():
    parser = argparse.ArgumentParser(description='Code Reviewer')
    parser.add_argument('source_dir', help='Source directory to review')
    parser.add_argument('--output', default='code_review_reports', help='Output directory for reports')
    
    args = parser.parse_args()
    
    reviewer = CodeReviewer()
    reviewer.review_code(args.source_dir)
    reviewer.generate_review_report(args.output)

if __name__ == "__main__":
    main()
