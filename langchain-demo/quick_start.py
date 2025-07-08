#!/usr/bin/env python3
"""
快速启动脚本
快速体验智能Agent功能
"""

import sys
import os
from pathlib import Path

# 确保可以导入项目模块
sys.path.insert(0, str(Path(__file__).parent))

try:
    from agent_project import IntelligentAgent
    from config import config
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装所有依赖：pip install -r requirements.txt")
    sys.exit(1)


def check_dependencies():
    """检查依赖是否安装"""
    required_packages = [
        "langchain",
        "langchain_community", 
        "langfuse",
        "requests",
        "dotenv"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("_", "-"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行: pip install -r requirements.txt")
        return False
    
    return True


def main():
    """主函数"""
    print("🚀 智能Agent快速启动器")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 显示配置状态
    try:
        config.print_config()
        print("✅ 配置加载成功")
    except Exception as e:
        print(f"⚠️  配置加载警告: {e}")
        print("将使用默认配置继续...")
    
    print("\n" + "=" * 40)
    print("🎯 选择体验模式:")
    print("1. 🎬 演示模式 - 自动运行预设任务")
    print("2. 💬 交互模式 - 与Agent对话")
    print("3. ⚡ 快速测试 - 单个任务测试")
    print("4. 🔧 工具列表 - 查看可用工具")
    
    while True:
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == "1":
            print("\n🎬 启动演示模式...")
            agent = IntelligentAgent()
            agent.demo_tasks()
            break
            
        elif choice == "2":
            print("\n💬 启动交互模式...")
            print("提示: 您可以尝试以下命令:")
            print("  - 计算 100 * 50 + 25")
            print("  - 查询上海天气")
            print("  - 创建任务：学习Python|深入学习Python编程|high")
            print("  - 分析数字：1,5,10,15,20,25,30")
            agent = IntelligentAgent()
            agent.interactive_mode()
            break
            
        elif choice == "3":
            print("\n⚡ 快速测试模式")
            test_tasks = [
                "计算 15 * 8 的结果",
                "查询北京天气",
                "分析数字：5,10,15,20,25"
            ]
            
            print("选择测试任务:")
            for i, task in enumerate(test_tasks, 1):
                print(f"  {i}. {task}")
            print("  4. 自定义任务")
            
            task_choice = input("选择任务 (1-4): ").strip()
            
            if task_choice in ["1", "2", "3"]:
                task = test_tasks[int(task_choice) - 1]
            elif task_choice == "4":
                task = input("输入自定义任务: ").strip()
            else:
                print("无效选择")
                continue
            
            if task:
                print(f"\n执行任务: {task}")
                agent = IntelligentAgent()
                result = agent.run_task(task)
                print(f"\n结果: {result}")
            break
            
        elif choice == "4":
            print("\n🔧 可用工具列表:")
            tools_info = [
                ("计算器", "执行数学计算", "示例: 计算 2^8 + sqrt(16)"),
                ("天气查询", "查询城市天气(模拟)", "示例: 查询广州天气"),
                ("文件管理", "创建、读取、列出文件", "示例: 创建备忘录.txt|今天要完成的任务"),
                ("数据分析", "分析数字统计", "示例: 分析 1,3,5,7,9,11,13,15"),
                ("任务管理", "创建和管理任务", "示例: 创建任务：写报告|完成月度报告|high"),
                ("图表数据", "生成可视化数据", "示例: 生成random类型的图表数据")
            ]
            
            for tool_name, description, example in tools_info:
                print(f"\n📋 {tool_name}")
                print(f"   功能: {description}")
                print(f"   {example}")
            
            input("\n按回车键返回主菜单...")
            continue
            
        else:
            print("无效选择，请输入 1-4")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        print("如需帮助，请查看 README.md 文件") 