#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流自动化工具
用于自动执行开发流程中的各个环节
"""

import os
import sys
import subprocess
import argparse
import json
import time
from datetime import datetime

class WorkflowAutomator:
    def __init__(self):
        self.workflow_results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def run_workflow(self, workflow_file):
        """运行工作流"""
        print(f"Running workflow from {workflow_file}...")
        
        try:
            # 加载工作流配置
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow_config = json.load(f)
            
            # 执行工作流步骤
            steps = workflow_config.get('steps', [])
            step_results = []
            
            for i, step in enumerate(steps):
                step_name = step.get('name', f'Step {i+1}')
                print(f"\nExecuting step: {step_name}")
                
                start_time = time.time()
                
                # 执行步骤
                result = self._execute_step(step)
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                result['name'] = step_name
                result['execution_time'] = execution_time
                step_results.append(result)
                
                # 检查是否需要停止
                if result.get('status') == 'error' and step.get('stop_on_error', True):
                    print(f"Step {step_name} failed, stopping workflow")
                    break
            
            self.workflow_results['workflow'] = {
                'status': 'success' if all(r.get('status') != 'error' for r in step_results) else 'failed',
                'steps': step_results,
                'workflow_file': workflow_file,
                'total_steps': len(steps),
                'completed_steps': len([r for r in step_results if r.get('status') == 'success'])
            }
            
            print("\nWorkflow execution completed")
            
        except Exception as e:
            self.workflow_results['workflow'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error running workflow: {e}")
    
    def _execute_step(self, step):
        """执行单个步骤"""
        step_type = step.get('type', 'command')
        
        if step_type == 'command':
            return self._execute_command(step)
        elif step_type == 'script':
            return self._execute_script(step)
        elif step_type == 'condition':
            return self._execute_condition(step)
        elif step_type == 'parallel':
            return self._execute_parallel(step)
        else:
            return {
                'status': 'error',
                'error': f'Unknown step type: {step_type}'
            }
    
    def _execute_command(self, step):
        """执行命令"""
        command = step.get('command')
        cwd = step.get('cwd', os.getcwd())
        env = step.get('env', {})
        
        if not command:
            return {
                'status': 'error',
                'error': 'No command specified'
            }
        
        try:
            print(f"Running command: {command}")
            
            # 构建环境变量
            process_env = os.environ.copy()
            process_env.update(env)
            
            # 执行命令
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=cwd, 
                env=process_env
            )
            
            return {
                'status': 'success' if result.returncode == 0 else 'error',
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _execute_script(self, step):
        """执行脚本"""
        script_path = step.get('script')
        args = step.get('args', [])
        cwd = step.get('cwd', os.getcwd())
        
        if not script_path:
            return {
                'status': 'error',
                'error': 'No script specified'
            }
        
        try:
            print(f"Running script: {script_path}")
            
            # 构建命令
            if script_path.endswith('.py'):
                command = [sys.executable, script_path] + args
            else:
                command = [script_path] + args
            
            # 执行脚本
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                cwd=cwd
            )
            
            return {
                'status': 'success' if result.returncode == 0 else 'error',
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _execute_condition(self, step):
        """执行条件判断"""
        condition = step.get('condition')
        then_steps = step.get('then', [])
        else_steps = step.get('else', [])
        
        if not condition:
            return {
                'status': 'error',
                'error': 'No condition specified'
            }
        
        try:
            print(f"Evaluating condition: {condition}")
            
            # 评估条件
            condition_result = eval(condition)
            print(f"Condition result: {condition_result}")
            
            # 执行相应的步骤
            if condition_result:
                steps_to_execute = then_steps
            else:
                steps_to_execute = else_steps
            
            # 执行步骤
            sub_step_results = []
            for sub_step in steps_to_execute:
                sub_result = self._execute_step(sub_step)
                sub_step_results.append(sub_result)
            
            return {
                'status': 'success',
                'condition_result': condition_result,
                'sub_steps': sub_step_results
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _execute_parallel(self, step):
        """并行执行步骤"""
        parallel_steps = step.get('steps', [])
        
        if not parallel_steps:
            return {
                'status': 'error',
                'error': 'No parallel steps specified'
            }
        
        try:
            print(f"Running {len(parallel_steps)} steps in parallel")
            
            # 并行执行步骤
            import concurrent.futures
            sub_step_results = []
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_step = {executor.submit(self._execute_step, sub_step): sub_step for sub_step in parallel_steps}
                
                for future in concurrent.futures.as_completed(future_to_step):
                    sub_step = future_to_step[future]
                    try:
                        sub_result = future.result()
                        sub_result['name'] = sub_step.get('name', 'Parallel Step')
                        sub_step_results.append(sub_result)
                    except Exception as e:
                        sub_step_results.append({
                            'status': 'error',
                            'error': str(e),
                            'name': sub_step.get('name', 'Parallel Step')
                        })
            
            return {
                'status': 'success' if all(r.get('status') != 'error' for r in sub_step_results) else 'failed',
                'parallel_steps': sub_step_results
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def generate_workflow_report(self, output_dir):
        """生成工作流报告"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成JSON报告
        report_file = os.path.join(output_dir, f'workflow_report_{self.timestamp}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.workflow_results, f, indent=2, ensure_ascii=False)
        
        # 生成文本报告
        text_report_file = os.path.join(output_dir, f'workflow_report_{self.timestamp}.txt')
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(f"Workflow Report - {self.timestamp}\n")
            f.write("=" * 60 + "\n")
            
            if 'workflow' in self.workflow_results:
                workflow = self.workflow_results['workflow']
                f.write(f"Status: {workflow.get('status')}\n")
                f.write(f"Total steps: {workflow.get('total_steps', 0)}\n")
                f.write(f"Completed steps: {workflow.get('completed_steps', 0)}\n")
                f.write(f"Workflow file: {workflow.get('workflow_file')}\n")
                
                if 'steps' in workflow:
                    f.write("\nSteps:\n")
                    f.write("-" * 40 + "\n")
                    
                    for i, step in enumerate(workflow['steps']):
                        f.write(f"\nStep {i+1}: {step.get('name')}\n")
                        f.write(f"Status: {step.get('status')}\n")
                        f.write(f"Execution time: {step.get('execution_time', 0):.2f} seconds\n")
                        
                        if 'stdout' in step and step['stdout']:
                            f.write("\nOutput:\n")
                            f.write(step['stdout'] + "\n")
                        
                        if 'stderr' in step and step['stderr']:
                            f.write("\nError:\n")
                            f.write(step['stderr'] + "\n")
        
        print(f"Workflow report generated: {report_file}")
        print(f"Text report generated: {text_report_file}")
    
    def create_workflow_template(self, output_file):
        """创建工作流模板"""
        template = {
            "name": "Sample Workflow",
            "description": "A sample workflow template",
            "steps": [
                {
                    "name": "Checkout code",
                    "type": "command",
                    "command": "git checkout main",
                    "stop_on_error": true
                },
                {
                    "name": "Update dependencies",
                    "type": "command",
                    "command": "pip install -r requirements.txt",
                    "stop_on_error": true
                },
                {
                    "name": "Run tests",
                    "type": "script",
                    "script": "automation/test/test_runner.py",
                    "args": ["--python-tests", "tests", "--code-quality", "src"],
                    "stop_on_error": true
                },
                {
                    "name": "Create deployment package",
                    "type": "script",
                    "script": "automation/deploy/deploy_script.py",
                    "args": ["--create-package", "src"],
                    "stop_on_error": true
                },
                {
                    "name": "Deploy to staging",
                    "type": "condition",
                    "condition": "os.path.exists('deploy_reports/deployment_1.0.0_*.zip')",
                    "then": [
                        {
                            "name": "Deploy to staging server",
                            "type": "command",
                            "command": "echo 'Deploying to staging'"
                        }
                    ],
                    "else": [
                        {
                            "name": "Skip deployment",
                            "type": "command",
                            "command": "echo 'Deployment package not found, skipping deployment'"
                        }
                    ]
                }
            ]
        }
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"Workflow template created: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Workflow Automator')
    parser.add_argument('--run', help='Workflow file to run')
    parser.add_argument('--create-template', help='Create a workflow template')
    parser.add_argument('--output', default='workflow_reports', help='Output directory for reports')
    
    args = parser.parse_args()
    
    automator = WorkflowAutomator()
    
    if args.run:
        automator.run_workflow(args.run)
        automator.generate_workflow_report(args.output)
    
    if args.create_template:
        automator.create_workflow_template(args.create_template)

if __name__ == "__main__":
    main()
