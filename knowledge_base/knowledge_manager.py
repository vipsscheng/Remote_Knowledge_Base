#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库管理工具
用于管理和维护结构化的知识库体系
"""

import os
import sys
import argparse
import json
import re
from datetime import datetime

class KnowledgeManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.knowledge_structure = {
            'core': '核心知识和基础概念',
            'domain': '领域特定知识',
            'tools': '工具和技术栈',
            'best_practices': '最佳实践',
            'examples': '代码示例和案例'
        }
        
        # 确保目录结构存在
        self._ensure_directory_structure()
    
    def _ensure_directory_structure(self):
        """确保目录结构存在"""
        for category in self.knowledge_structure:
            category_dir = os.path.join(self.base_dir, category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
                print(f"Created directory: {category_dir}")
    
    def add_knowledge(self, category, title, content, tags=None):
        """添加知识条目"""
        if category not in self.knowledge_structure:
            print(f"Error: Category '{category}' does not exist")
            return False
        
        # 创建知识文件
        slug = self._create_slug(title)
        file_path = os.path.join(self.base_dir, category, f'{slug}.md')
        
        # 生成元数据
        metadata = {
            'title': title,
            'slug': slug,
            'category': category,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'tags': tags or [],
            'author': 'AI Agent Core Skill'
        }
        
        # 构建文件内容
        content_lines = [
            '---',
            json.dumps(metadata, ensure_ascii=False, indent=2),
            '---',
            '',
            content
        ]
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))
        
        print(f"Added knowledge: {title} to {category}")
        print(f"File created: {file_path}")
        return True
    
    def update_knowledge(self, category, slug, content=None, tags=None):
        """更新知识条目"""
        file_path = os.path.join(self.base_dir, category, f'{slug}.md')
        
        if not os.path.exists(file_path):
            print(f"Error: Knowledge '{slug}' not found in {category}")
            return False
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 解析元数据
        metadata_end = 0
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:
                metadata_end = i
                break
        
        if metadata_end == 0:
            print("Error: Invalid knowledge file format")
            return False
        
        # 解析元数据
        metadata_str = ''.join(lines[1:metadata_end])
        metadata = json.loads(metadata_str)
        
        # 更新元数据
        metadata['updated_at'] = datetime.now().isoformat()
        if tags is not None:
            metadata['tags'] = tags
        
        # 更新内容
        if content is not None:
            new_lines = [
                '---',
                json.dumps(metadata, ensure_ascii=False, indent=2),
                '---',
                '',
                content
            ]
        else:
            new_lines = [
                '---',
                json.dumps(metadata, ensure_ascii=False, indent=2),
                '---',
            ] + lines[metadata_end+1:]
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"Updated knowledge: {metadata['title']} in {category}")
        return True
    
    def delete_knowledge(self, category, slug):
        """删除知识条目"""
        file_path = os.path.join(self.base_dir, category, f'{slug}.md')
        
        if not os.path.exists(file_path):
            print(f"Error: Knowledge '{slug}' not found in {category}")
            return False
        
        # 删除文件
        os.remove(file_path)
        print(f"Deleted knowledge: {slug} from {category}")
        return True
    
    def list_knowledge(self, category=None):
        """列出知识条目"""
        if category:
            if category not in self.knowledge_structure:
                print(f"Error: Category '{category}' does not exist")
                return
            
            category_dir = os.path.join(self.base_dir, category)
            print(f"Knowledge in {category} ({self.knowledge_structure[category]}):")
            print("-" * 60)
            
            for file in os.listdir(category_dir):
                if file.endswith('.md'):
                    file_path = os.path.join(category_dir, file)
                    metadata = self._get_metadata(file_path)
                    if metadata:
                        print(f"- {metadata['title']} ({metadata['slug']})")
                        print(f"  Tags: {', '.join(metadata.get('tags', []))}")
                        print(f"  Updated: {metadata['updated_at']}")
                        print()
        else:
            for cat in self.knowledge_structure:
                print(f"\n{cat.upper()}: {self.knowledge_structure[cat]}")
                print("-" * 40)
                category_dir = os.path.join(self.base_dir, cat)
                count = 0
                for file in os.listdir(category_dir):
                    if file.endswith('.md'):
                        count += 1
                        metadata = self._get_metadata(os.path.join(category_dir, file))
                        if metadata:
                            print(f"  - {metadata['title']}")
                if count == 0:
                    print("  No knowledge items")
    
    def search_knowledge(self, query):
        """搜索知识条目"""
        results = []
        
        for category in self.knowledge_structure:
            category_dir = os.path.join(self.base_dir, category)
            for file in os.listdir(category_dir):
                if file.endswith('.md'):
                    file_path = os.path.join(category_dir, file)
                    metadata = self._get_metadata(file_path)
                    if metadata:
                        # 搜索标题和内容
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if query.lower() in metadata['title'].lower() or query.lower() in content.lower():
                            results.append({
                                'title': metadata['title'],
                                'category': category,
                                'slug': metadata['slug'],
                                'tags': metadata.get('tags', []),
                                'updated_at': metadata['updated_at']
                            })
        
        print(f"Search results for '{query}':")
        print("-" * 60)
        
        if results:
            for result in results:
                print(f"- {result['title']} (Category: {result['category']})")
                print(f"  Tags: {', '.join(result['tags'])}")
                print(f"  Updated: {result['updated_at']}")
                print()
        else:
            print("No results found")
    
    def export_knowledge(self, output_file):
        """导出知识库"""
        knowledge_base = {
            'exported_at': datetime.now().isoformat(),
            'categories': {}
        }
        
        for category in self.knowledge_structure:
            category_dir = os.path.join(self.base_dir, category)
            knowledge_base['categories'][category] = []
            
            for file in os.listdir(category_dir):
                if file.endswith('.md'):
                    file_path = os.path.join(category_dir, file)
                    metadata = self._get_metadata(file_path)
                    if metadata:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        knowledge_base['categories'][category].append({
                            'metadata': metadata,
                            'content': content
                        })
        
        # 写入导出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
        
        print(f"Knowledge base exported to: {output_file}")
    
    def import_knowledge(self, input_file):
        """导入知识库"""
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} not found")
            return False
        
        # 读取导入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            knowledge_base = json.load(f)
        
        # 导入知识条目
        imported_count = 0
        for category, items in knowledge_base.get('categories', {}).items():
            for item in items:
                metadata = item.get('metadata', {})
                content = item.get('content', '')
                
                # 提取内容（去除元数据部分）
                if content.startswith('---'):
                    lines = content.split('\n')
                    metadata_end = 0
                    for i, line in enumerate(lines):
                        if line.strip() == '---' and i > 0:
                            metadata_end = i
                            break
                    if metadata_end > 0:
                        content = '\n'.join(lines[metadata_end+1:])
                
                # 添加知识条目
                self.add_knowledge(
                    category=category,
                    title=metadata.get('title', 'Untitled'),
                    content=content,
                    tags=metadata.get('tags', [])
                )
                imported_count += 1
        
        print(f"Imported {imported_count} knowledge items")
        return True
    
    def _get_metadata(self, file_path):
        """从文件中提取元数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if lines[0].strip() != '---':
                return None
            
            metadata_end = 0
            for i, line in enumerate(lines):
                if line.strip() == '---' and i > 0:
                    metadata_end = i
                    break
            
            if metadata_end == 0:
                return None
            
            metadata_str = ''.join(lines[1:metadata_end])
            return json.loads(metadata_str)
        except:
            return None
    
    def _create_slug(self, title):
        """从标题创建slug"""
        # 转换为小写
        slug = title.lower()
        # 替换空格为连字符
        slug = slug.replace(' ', '-')
        # 移除非字母数字字符
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        # 移除连续的连字符
        slug = re.sub(r'-+', '-', slug)
        # 移除首尾连字符
        slug = slug.strip('-')
        return slug

def main():
    # 获取当前用户目录
    import getpass
    import os
    user_home = os.path.expanduser('~')
    default_base_dir = os.path.join(user_home, '技能文件夹', '知识库')
    
    parser = argparse.ArgumentParser(description='Knowledge Base Manager')
    parser.add_argument('--base-dir', default=default_base_dir, help='Knowledge base directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add knowledge
    add_parser = subparsers.add_parser('add', help='Add knowledge')
    add_parser.add_argument('category', help='Category')
    add_parser.add_argument('title', help='Title')
    add_parser.add_argument('--content', help='Content (use - for stdin)')
    add_parser.add_argument('--tags', nargs='+', help='Tags')
    
    # Update knowledge
    update_parser = subparsers.add_parser('update', help='Update knowledge')
    update_parser.add_argument('category', help='Category')
    update_parser.add_argument('slug', help='Slug')
    update_parser.add_argument('--content', help='Content (use - for stdin)')
    update_parser.add_argument('--tags', nargs='+', help='Tags')
    
    # Delete knowledge
    delete_parser = subparsers.add_parser('delete', help='Delete knowledge')
    delete_parser.add_argument('category', help='Category')
    delete_parser.add_argument('slug', help='Slug')
    
    # List knowledge
    list_parser = subparsers.add_parser('list', help='List knowledge')
    list_parser.add_argument('--category', help='Category')
    
    # Search knowledge
    search_parser = subparsers.add_parser('search', help='Search knowledge')
    search_parser.add_argument('query', help='Search query')
    
    # Export knowledge
    export_parser = subparsers.add_parser('export', help='Export knowledge')
    export_parser.add_argument('output', help='Output file')
    
    # Import knowledge
    import_parser = subparsers.add_parser('import', help='Import knowledge')
    import_parser.add_argument('input', help='Input file')
    
    args = parser.parse_args()
    
    manager = KnowledgeManager(args.base_dir)
    
    if args.command == 'add':
        if args.content == '-':
            content = sys.stdin.read()
        else:
            content = args.content or ''
        manager.add_knowledge(args.category, args.title, content, args.tags)
    
    elif args.command == 'update':
        if args.content == '-':
            content = sys.stdin.read()
        else:
            content = args.content
        manager.update_knowledge(args.category, args.slug, content, args.tags)
    
    elif args.command == 'delete':
        manager.delete_knowledge(args.category, args.slug)
    
    elif args.command == 'list':
        manager.list_knowledge(args.category)
    
    elif args.command == 'search':
        manager.search_knowledge(args.query)
    
    elif args.command == 'export':
        manager.export_knowledge(args.output)
    
    elif args.command == 'import':
        manager.import_knowledge(args.input)

if __name__ == "__main__":
    main()
