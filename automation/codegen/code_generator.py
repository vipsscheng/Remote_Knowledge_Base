#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码生成器
用于自动生成各种代码模板和骨架
"""

import os
import json
import argparse
from datetime import datetime

class CodeGenerator:
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            self._create_default_templates()
    
    def _create_default_templates(self):
        """创建默认模板"""
        # C语言模板
        c_template = """
/**
 * @file {{filename}}.c
 * @brief {{description}}
 * @author AI Agent Core Skill
 * @date {{date}}
 */

#include <stdio.h>
#include <stdlib.h>

{{includes}}

/**
 * @brief {{function_description}}
 * @param {{param1}} - {{param1_description}}
 * @param {{param2}} - {{param2_description}}
 * @return {{return_description}}
 */
{{return_type}} {{function_name}}({{params}}) {
    // 实现代码
    return {{default_return}};
}

int main(int argc, char *argv[]) {
    // 主函数
    return 0;
}
"""
        
        # Python模板
        python_template = """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{{filename}}.py
{{description}}
Author: AI Agent Core Skill
Date: {{date}}
"""

{{imports}}

def {{function_name}}({{params}}):
    """
    {{function_description}}
    
    Args:
        {{param1}}: {{param1_description}}
        {{param2}}: {{param2_description}}
    
    Returns:
        {{return_description}}
    """
    # 实现代码
    return {{default_return}}

if __name__ == "__main__":
    # 主函数
    pass
"""
        
        # 保存模板
        with open(os.path.join(self.templates_dir, 'c_template.txt'), 'w', encoding='utf-8') as f:
            f.write(c_template)
        
        with open(os.path.join(self.templates_dir, 'python_template.txt'), 'w', encoding='utf-8') as f:
            f.write(python_template)
    
    def load_template(self, template_name):
        """加载模板"""
        template_path = os.path.join(self.templates_dir, f'{template_name}_template.txt')
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template {template_name} not found")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_code(self, template_name, output_file, **kwargs):
        """生成代码"""
        template = self.load_template(template_name)
        
        # 替换变量
        kwargs['date'] = datetime.now().strftime('%Y-%m-%d')
        kwargs['filename'] = os.path.splitext(os.path.basename(output_file))[0]
        
        # 填充默认值
        kwargs.setdefault('description', 'Generated code')
        kwargs.setdefault('function_description', 'Function description')
        kwargs.setdefault('function_name', 'example_function')
        kwargs.setdefault('return_type', 'int')
        kwargs.setdefault('params', 'void')
        kwargs.setdefault('param1', 'param1')
        kwargs.setdefault('param1_description', 'Parameter 1')
        kwargs.setdefault('param2', 'param2')
        kwargs.setdefault('param2_description', 'Parameter 2')
        kwargs.setdefault('return_description', 'Return value')
        kwargs.setdefault('default_return', '0')
        kwargs.setdefault('includes', '')
        kwargs.setdefault('imports', '')
        
        # 替换模板变量
        for key, value in kwargs.items():
            template = template.replace(f'{{{{{key}}}}}', str(value))
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"Code generated successfully: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Code Generator')
    parser.add_argument('template', choices=['c', 'python'], help='Template type')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('--description', help='Code description')
    parser.add_argument('--function-name', help='Function name')
    parser.add_argument('--function-description', help='Function description')
    parser.add_argument('--return-type', help='Return type (for C)')
    parser.add_argument('--params', help='Parameters')
    parser.add_argument('--includes', help='Include statements (for C)')
    parser.add_argument('--imports', help='Import statements (for Python)')
    
    args = parser.parse_args()
    
    generator = CodeGenerator()
    
    # 构建参数
    kwargs = {}
    if args.description:
        kwargs['description'] = args.description
    if args.function_name:
        kwargs['function_name'] = args.function_name
    if args.function_description:
        kwargs['function_description'] = args.function_description
    if args.return_type:
        kwargs['return_type'] = args.return_type
    if args.params:
        kwargs['params'] = args.params
    if args.includes:
        kwargs['includes'] = args.includes
    if args.imports:
        kwargs['imports'] = args.imports
    
    generator.generate_code(args.template, args.output, **kwargs)

if __name__ == "__main__":
    main()
