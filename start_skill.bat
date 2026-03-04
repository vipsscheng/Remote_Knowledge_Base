@echo off
echo Starting AI Agent Core Skill...
echo Starting self-evolution system in background...

REM 启动自我进化系统（后台运行）
python -c "from automation.evolution.self_evolution import SelfEvolutionSystem; system = SelfEvolutionSystem(); system.start(); print('Self-evolution system started successfully'); import time; time.sleep(2)"

echo AI Agent Core Skill started successfully!
echo Self-evolution system is running in background.
echo
echo 技能已启动，自我进化系统正在后台运行...
echo 系统已配置为使用用户模型，无需额外AI配置。
echo 技能已激活，可以直接使用。
pause