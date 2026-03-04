#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自我进化系统
用于实现技能的自动自我修改、自我完善、自我进化和自我生长
"""

import os
import sys
import subprocess
import json
import time
import random
import platform
import threading
import queue
from datetime import datetime

class SelfEvolutionSystem:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # 使用用户目录作为基础目录，确保全局生效
        self.base_dir = os.path.join(os.path.expanduser('~'), '技能文件夹')
        self.evolution_dir = os.path.join(self.base_dir, '自动化工具', 'evolution')
        self.log_dir = os.path.join(self.evolution_dir, 'logs')
        self.model_config = os.path.join(self.evolution_dir, 'model_config.json')
        self.system_config = os.path.join(self.evolution_dir, 'system_config.json')
        
        # 确保目录存在
        self._ensure_directories()
        
        # 加载配置
        self.config = self._load_config()
        
        # 检测可用的AI模型
        self.available_models = self._detect_ai_models()
        
        # 初始化组件
        self.monitor = SystemMonitor(self)
        self.analyzer = SystemAnalyzer(self)
        self.planner = ImprovementPlanner(self)
        self.executor = CodeExecutor(self)
        self.deployer = AutoDeployer(self)
        self.learner = SelfLearner(self)
        
        # 初始化多线程相关
        self.thread = None
        self.stop_event = threading.Event()
        self.task_queue = queue.PriorityQueue()
        self.is_running = False
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        for directory in [self.evolution_dir, self.log_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                self._log(f"Created directory: {directory}")
    
    def _load_config(self):
        """加载配置文件"""
        default_config = {
            'evolution_interval': 3600,  # 每小时运行一次
            'max_modifications': 10,  # 每次最多修改10个文件
            'backup_enabled': True,  # 启用备份
            'testing_enabled': True,  # 启用测试
            'deployment_enabled': True,  # 启用自动部署
            'model_preference': []  # 模型偏好列表
        }
        
        if os.path.exists(self.system_config):
            with open(self.system_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            default_config.update(config)
        else:
            with open(self.system_config, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
    
    def _detect_ai_models(self):
        """检测可用的AI模型"""
        models = {
            # 国际模型
            'gpt4': {'name': 'GPT-4', 'available': False, 'api_key': None},
            'claude': {'name': 'Claude', 'available': False, 'api_key': None},
            'gemini': {'name': 'Gemini', 'available': False, 'api_key': None},
            'llama': {'name': 'Llama', 'available': False, 'api_key': None},
            # 国内模型
            'wenxin': {'name': '文心一言', 'available': False, 'api_key': None},
            'xinghuo': {'name': '讯飞星火', 'available': False, 'api_key': None},
            'qwen': {'name': '通义千问', 'available': False, 'api_key': None},
            'doubao': {'name': '豆包', 'available': False, 'api_key': None}
        }
        
        # 检查环境变量中的API密钥
        for model in models:
            api_key_env = f'{model.upper()}_API_KEY'
            if api_key_env in os.environ:
                models[model]['available'] = True
                models[model]['api_key'] = os.environ[api_key_env]
                self._log(f"Detected {models[model]['name']} model via API key")
        
        # 检查本地安装的模型
        if self._is_tool_available('ollama'):
            try:
                result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
                if 'llama' in result.stdout:
                    models['llama']['available'] = True
                    self._log("Detected Llama model via Ollama")
            except:
                pass
        
        # 检查国内模型的CLI工具
        if self._is_tool_available('wenxin-cli'):
            models['wenxin']['available'] = True
            self._log("Detected 文心一言 model via CLI")
        if self._is_tool_available('xinghuo-cli'):
            models['xinghuo']['available'] = True
            self._log("Detected 讯飞星火 model via CLI")
        if self._is_tool_available('qwen-cli'):
            models['qwen']['available'] = True
            self._log("Detected 通义千问 model via CLI")
        if self._is_tool_available('doubao-cli'):
            models['doubao']['available'] = True
            self._log("Detected 豆包 model via CLI")
        
        # 保存模型配置
        with open(self.model_config, 'w', encoding='utf-8') as f:
            json.dump(models, f, indent=2, ensure_ascii=False)
        
        return models
    
    def _is_tool_available(self, command):
        """检查工具是否可用"""
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(['where', command], capture_output=True, text=True)
                return result.returncode == 0
            else:
                result = subprocess.run(['which', command], capture_output=True, text=True)
                return result.returncode == 0
        except:
            return False
    
    def _log(self, message):
        """记录日志"""
        log_file = os.path.join(self.log_dir, f"evolution_{datetime.now().strftime('%Y-%m-%d')}.log")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        
        print(log_entry)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def get_available_model(self):
        """获取可用的AI模型"""
        # 优先使用用户偏好的模型
        for model in self.config['model_preference']:
            if model in self.available_models and self.available_models[model]['available']:
                return model
        
        # 随机选择一个可用的模型
        available = [model for model in self.available_models if self.available_models[model]['available']]
        if available:
            return random.choice(available)
        
        # 没有可用模型
        return None
    
    def start(self):
        """启动自我进化系统（后台运行）"""
        if self.is_running:
            self._log("Self-evolution system is already running")
            return
        
        self.is_running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run_background, daemon=True)
        self.thread.start()
        self._log("Self-evolution system started in background")
    
    def stop(self):
        """停止自我进化系统"""
        if not self.is_running:
            self._log("Self-evolution system is not running")
            return
        
        self._log("Stopping self-evolution system...")
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=30)
        self.is_running = False
        self._log("Self-evolution system stopped")
    
    def _run_background(self):
        """后台运行自我进化系统"""
        self._log("Starting self-evolution system in background...")
        
        while not self.stop_event.is_set():
            try:
                # 1. 监控系统状态
                self._log("Step 1: Monitoring system status")
                data = self.monitor.collect_data()
                
                # 2. 分析系统问题和改进机会
                self._log("Step 2: Analyzing system issues and improvement opportunities")
                issues, opportunities = self.analyzer.analyze(data)
                
                # 3. 制定改进计划
                self._log("Step 3: Creating improvement plan")
                plan = self.planner.create_plan(issues, opportunities)
                
                # 4. 执行改进（按优先级）
                if plan:
                    self._log("Step 4: Executing improvements with priority")
                    # 将任务按优先级放入队列
                    for item in plan:
                        # 计算优先级权重
                        priority = self._calculate_priority(item)
                        self.task_queue.put((priority, item))
                    
                    # 处理队列中的任务
                    results = []
                    while not self.task_queue.empty() and not self.stop_event.is_set():
                        priority, item = self.task_queue.get()
                        try:
                            if item['type'] == 'fix':
                                result = self.executor._fix_issue(item['issue'])
                            else:
                                result = self.executor._implement_improvement(item['opportunity'])
                            results.append({
                                'item': item,
                                'result': result,
                                'status': 'success'
                            })
                        except Exception as e:
                            results.append({
                                'item': item,
                                'error': str(e),
                                'status': 'failed'
                            })
                        finally:
                            self.task_queue.task_done()
                    
                    # 5. 部署改进
                    if results and self.config['deployment_enabled']:
                        self._log("Step 5: Deploying improvements")
                        deployment_result = self.deployer.deploy(results)
                        
                        # 6. 学习和调整
                        self._log("Step 6: Learning and adjusting")
                        self.learner.learn(deployment_result)
                
                # 等待下一个周期
                interval = self.config['evolution_interval']
                self._log(f"Waiting for next evolution cycle ( {interval} seconds )")
                
                # 检查是否需要停止
                for _ in range(interval):
                    if self.stop_event.is_set():
                        break
                    time.sleep(1)
                
            except Exception as e:
                self._log(f"Error in self-evolution system: {e}")
                import traceback
                traceback.print_exc()
                # 出错后等待一段时间再继续
                for _ in range(600):  # 10分钟
                    if self.stop_event.is_set():
                        break
                    time.sleep(1)
    
    def _calculate_priority(self, item):
        """计算任务优先级权重"""
        # 优先级权重：越高优先级越高
        priority_map = {
            'high': 1,
            'medium': 2,
            'low': 3
        }
        
        if item['type'] == 'fix':
            # 修复问题的优先级
            severity = item['issue'].get('severity', 'low')
            return priority_map.get(severity, 3)
        else:
            # 改进机会的优先级
            priority = item['opportunity'].get('priority', 'low')
            return priority_map.get(priority, 3)
    
    def run(self):
        """运行自我进化系统（前台运行）"""
        self.start()
        # 保持主线程运行
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

class SystemMonitor:
    def __init__(self, system):
        self.system = system
    
    def collect_data(self):
        """收集系统运行数据"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'system': {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'cpu_count': os.cpu_count(),
                'cwd': os.getcwd()
            },
            'files': {
                'modified': [],
                'created': [],
                'deleted': []
            },
            'performance': {
                'start_time': time.time()
            },
            'logs': self._collect_logs()
        }
        
        return data
    
    def _collect_logs(self):
        """收集系统日志"""
        logs = []
        log_dir = os.path.join(self.system.base_dir, 'automation', 'evolution', 'logs')
        
        if os.path.exists(log_dir):
            for file in os.listdir(log_dir):
                if file.endswith('.log'):
                    log_file = os.path.join(log_dir, file)
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()[-100:]  # 只读取最后100行
                            logs.extend([line.strip() for line in lines])
                    except:
                        pass
        
        return logs

class SystemAnalyzer:
    def __init__(self, system):
        self.system = system
    
    def analyze(self, data):
        """分析系统数据"""
        issues = []
        opportunities = []
        
        # 分析日志中的错误
        error_patterns = ['error', 'fail', 'exception', 'crash']
        for log in data.get('logs', []):
            if any(pattern in log.lower() for pattern in error_patterns):
                issues.append({
                    'type': 'error',
                    'description': log,
                    'severity': 'medium'
                })
        
        # 分析文件修改
        modified_files = data.get('files', {}).get('modified', [])
        if len(modified_files) > 10:
            issues.append({
                'type': 'file_modification',
                'description': f'Too many files modified: {len(modified_files)}',
                'severity': 'low'
            })
        
        # 发现改进机会
        opportunities.append({
            'type': 'performance',
            'description': 'Optimize system performance',
            'priority': 'medium'
        })
        
        opportunities.append({
            'type': 'feature',
            'description': 'Add new features based on user needs',
            'priority': 'low'
        })
        
        return issues, opportunities

class ImprovementPlanner:
    def __init__(self, system):
        self.system = system
    
    def create_plan(self, issues, opportunities):
        """创建改进计划"""
        plan = []
        
        # 优先处理高优先级问题
        for issue in sorted(issues, key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x.get('severity', 'low')], reverse=True):
            plan.append({
                'type': 'fix',
                'issue': issue,
                'priority': issue.get('severity', 'low'),
                'estimated_effort': 'low'
            })
        
        # 添加改进机会
        for opportunity in sorted(opportunities, key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x.get('priority', 'low')], reverse=True):
            plan.append({
                'type': 'improvement',
                'opportunity': opportunity,
                'priority': opportunity.get('priority', 'low'),
                'estimated_effort': 'medium'
            })
        
        # 限制修改数量
        plan = plan[:self.system.config['max_modifications']]
        
        return plan

class CodeExecutor:
    def __init__(self, system):
        self.system = system
    
    def execute(self, plan):
        """执行改进计划"""
        results = []
        
        for item in plan:
            try:
                if item['type'] == 'fix':
                    result = self._fix_issue(item['issue'])
                else:
                    result = self._implement_improvement(item['opportunity'])
                
                results.append({
                    'item': item,
                    'result': result,
                    'status': 'success'
                })
                
            except Exception as e:
                results.append({
                    'item': item,
                    'error': str(e),
                    'status': 'failed'
                })
        
        return results
    
    def fix_issue(self, issue):
        """修复问题"""
        # 这里应该使用AI模型生成修复代码
        # 由于我们不指定特定模型，会根据可用模型自动选择
        model = self.system.get_available_model()
        
        if model:
            self.system._log(f"Using {self.system.available_models[model]['name']} to fix issue: {issue['description']}")
            # 模拟AI模型生成修复
            return f"Fixed issue using {self.system.available_models[model]['name']}"
        else:
            self.system._log("No AI model available, using user model or default implementation")
            # 没有AI模型时，使用默认实现
            return "Fixed issue using default implementation"
    
    def implement_improvement(self, opportunity):
        """实现改进"""
        model = self.system.get_available_model()
        
        if model:
            self.system._log(f"Using {self.system.available_models[model]['name']} to implement improvement: {opportunity['description']}")
            # 模拟AI模型生成改进
            return f"Implemented improvement using {self.system.available_models[model]['name']}"
        else:
            self.system._log("No AI model available, using user model or default implementation")
            # 没有AI模型时，使用默认实现
            return "Implemented improvement using default implementation"
    
    def _fix_issue(self, issue):
        """修复问题（内部方法）"""
        return self.fix_issue(issue)
    
    def _implement_improvement(self, opportunity):
        """实现改进（内部方法）"""
        return self.implement_improvement(opportunity)

class AutoDeployer:
    def __init__(self, system):
        self.system = system
    
    def deploy(self, results):
        """部署改进"""
        deployment_result = {
            'timestamp': datetime.now().isoformat(),
            'success_count': sum(1 for r in results if r['status'] == 'success'),
            'failed_count': sum(1 for r in results if r['status'] == 'failed'),
            'results': results
        }
        
        # 模拟部署过程
        self.system._log(f"Deploying {deployment_result['success_count']} successful changes")
        
        # 生成部署报告
        report_file = os.path.join(self.system.evolution_dir, f"deployment_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(deployment_result, f, indent=2, ensure_ascii=False)
        
        return deployment_result

class SelfLearner:
    def __init__(self, system):
        self.system = system
    
    def learn(self, deployment_result):
        """从部署结果中学习"""
        # 分析部署结果
        success_rate = deployment_result['success_count'] / (deployment_result['success_count'] + deployment_result['failed_count'])
        
        # 更新系统配置
        if success_rate < 0.5:
            # 降低修改频率
            self.system.config['evolution_interval'] = min(self.system.config['evolution_interval'] * 2, 86400)  # 最多24小时
            self.system._log(f"Lowering evolution frequency to {self.system.config['evolution_interval']} seconds due to low success rate")
        elif success_rate > 0.8:
            # 增加修改频率
            self.system.config['evolution_interval'] = max(self.system.config['evolution_interval'] // 2, 300)  # 最少5分钟
            self.system._log(f"Increasing evolution frequency to {self.system.config['evolution_interval']} seconds due to high success rate")
        
        # 保存更新后的配置
        with open(self.system.system_config, 'w', encoding='utf-8') as f:
            json.dump(self.system.config, f, indent=2, ensure_ascii=False)
        
        # 学习模型性能
        self._learn_model_performance(deployment_result)
    
    def _learn_model_performance(self, deployment_result):
        """学习模型性能"""
        # 这里可以分析不同模型的性能，调整模型偏好
        pass

def main():
    system = SelfEvolutionSystem()
    system.run()

if __name__ == "__main__":
    main()