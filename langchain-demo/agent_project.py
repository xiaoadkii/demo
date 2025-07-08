#!/usr/bin/env python3
"""
完整的智能Agent项目
集成LangChain、Langfuse观测、多种工具和任务管理
"""

import os
import json
import time
import math
import random
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult

# 导入配置管理模块
from config import config

# Langfuse 集成
from langfuse import get_client
from langfuse.callback import CallbackHandler as LangfuseCallbackHandler


class AgentLogger:
    """Agent 日志记录器"""
    
    def __init__(self):
        self.logs = []
    
    def log(self, level: str, message: str, **kwargs):
        """记录日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }
        self.logs.append(log_entry)
        print(f"[{level}] {message}")
    
    def info(self, message: str, **kwargs):
        self.log("INFO", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log("ERROR", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log("WARNING", message, **kwargs)


class CalculatorTool:
    """计算器工具"""
    
    @staticmethod
    def calculate(expression: str) -> str:
        """执行数学计算"""
        try:
            # 安全的数学计算，只允许基本运算
            allowed_names = {
                k: v for k, v in math.__dict__.items() 
                if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"


class WeatherTool:
    """天气查询工具（模拟）"""
    
    @staticmethod
    def get_weather(city: str) -> str:
        """获取城市天气（模拟数据）"""
        try:
            # 模拟天气数据
            weather_conditions = ["晴天", "多云", "小雨", "大雨", "雪", "雾"]
            temperature = random.randint(-10, 35)
            condition = random.choice(weather_conditions)
            humidity = random.randint(30, 90)
            
            weather_data = {
                "city": city,
                "temperature": f"{temperature}°C",
                "condition": condition,
                "humidity": f"{humidity}%",
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return f"""
🌤️ {city}天气信息:
温度: {weather_data['temperature']}
天气: {weather_data['condition']}
湿度: {weather_data['humidity']}
更新时间: {weather_data['update_time']}
            """.strip()
        except Exception as e:
            return f"天气查询失败: {str(e)}"


class FileManagerTool:
    """文件管理工具"""
    
    def __init__(self, base_dir: str = "agent_workspace"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def create_file(self, filename: str, content: str) -> str:
        """创建文件"""
        try:
            file_path = self.base_dir / filename
            file_path.write_text(content, encoding='utf-8')
            return f"✅ 文件 {filename} 创建成功"
        except Exception as e:
            return f"❌ 文件创建失败: {str(e)}"
    
    def read_file(self, filename: str) -> str:
        """读取文件"""
        try:
            file_path = self.base_dir / filename
            if not file_path.exists():
                return f"❌ 文件 {filename} 不存在"
            content = file_path.read_text(encoding='utf-8')
            return f"📄 文件内容:\n{content}"
        except Exception as e:
            return f"❌ 文件读取失败: {str(e)}"
    
    def list_files(self) -> str:
        """列出文件"""
        try:
            files = list(self.base_dir.glob("*"))
            if not files:
                return "📁 工作空间为空"
            
            file_list = []
            for file in files:
                if file.is_file():
                    size = file.stat().st_size
                    modified = datetime.fromtimestamp(file.stat().st_mtime)
                    file_list.append(f"📄 {file.name} ({size} bytes, {modified.strftime('%Y-%m-%d %H:%M:%S')})")
                elif file.is_dir():
                    file_list.append(f"📁 {file.name}/")
            
            return "📁 工作空间文件列表:\n" + "\n".join(file_list)
        except Exception as e:
            return f"❌ 文件列表获取失败: {str(e)}"


class DataAnalysisTool:
    """数据分析工具"""
    
    @staticmethod
    def analyze_numbers(numbers_str: str) -> str:
        """分析数字列表"""
        try:
            # 解析数字
            numbers = [float(x.strip()) for x in numbers_str.split(",")]
            
            if not numbers:
                return "❌ 没有有效的数字"
            
            # 计算统计信息
            total = sum(numbers)
            count = len(numbers)
            mean = total / count
            sorted_nums = sorted(numbers)
            
            # 中位数
            if count % 2 == 0:
                median = (sorted_nums[count//2-1] + sorted_nums[count//2]) / 2
            else:
                median = sorted_nums[count//2]
            
            # 标准差
            variance = sum((x - mean) ** 2 for x in numbers) / count
            std_dev = math.sqrt(variance)
            
            analysis = f"""
📊 数据分析结果:
数据: {numbers}
总数: {count}
总和: {total:.2f}
平均值: {mean:.2f}
中位数: {median:.2f}
最小值: {min(numbers):.2f}
最大值: {max(numbers):.2f}
标准差: {std_dev:.2f}
            """.strip()
            
            return analysis
        except Exception as e:
            return f"❌ 数据分析失败: {str(e)}"
    
    @staticmethod
    def generate_chart_data(data_type: str = "random") -> str:
        """生成图表数据"""
        try:
            if data_type == "random":
                data = [random.randint(1, 100) for _ in range(10)]
                labels = [f"项目{i+1}" for i in range(10)]
            elif data_type == "time_series":
                base_date = datetime.now()
                data = [random.randint(20, 80) for _ in range(7)]
                labels = [(base_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
            else:
                return "❌ 不支持的数据类型"
            
            chart_data = {
                "type": data_type,
                "labels": labels,
                "data": data,
                "generated_at": datetime.now().isoformat()
            }
            
            return f"📈 图表数据生成成功:\n{json.dumps(chart_data, indent=2, ensure_ascii=False)}"
        except Exception as e:
            return f"❌ 图表数据生成失败: {str(e)}"


class TaskManagerTool:
    """任务管理工具"""
    
    def __init__(self):
        self.tasks = []
        self.task_counter = 0
    
    def create_task(self, title: str, description: str = "", priority: str = "medium") -> str:
        """创建任务"""
        try:
            self.task_counter += 1
            task = {
                "id": self.task_counter,
                "title": title,
                "description": description,
                "priority": priority,
                "status": "待办",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            self.tasks.append(task)
            return f"✅ 任务创建成功 (ID: {task['id']}): {title}"
        except Exception as e:
            return f"❌ 任务创建失败: {str(e)}"
    
    def list_tasks(self) -> str:
        """列出所有任务"""
        try:
            if not self.tasks:
                return "📋 暂无任务"
            
            task_list = ["📋 任务列表:"]
            for task in self.tasks:
                status_emoji = {"待办": "⏳", "进行中": "🔄", "已完成": "✅"}
                emoji = status_emoji.get(task["status"], "❓")
                task_list.append(f"{emoji} [{task['id']}] {task['title']} ({task['priority']}) - {task['status']}")
            
            return "\n".join(task_list)
        except Exception as e:
            return f"❌ 任务列表获取失败: {str(e)}"
    
    def update_task_status(self, task_id: int, status: str) -> str:
        """更新任务状态"""
        try:
            task_id = int(task_id)
            valid_statuses = ["待办", "进行中", "已完成"]
            
            if status not in valid_statuses:
                return f"❌ 无效的状态，请使用: {', '.join(valid_statuses)}"
            
            for task in self.tasks:
                if task["id"] == task_id:
                    task["status"] = status
                    task["updated_at"] = datetime.now().isoformat()
                    return f"✅ 任务 {task_id} 状态已更新为: {status}"
            
            return f"❌ 未找到ID为 {task_id} 的任务"
        except ValueError:
            return "❌ 任务ID必须是数字"
        except Exception as e:
            return f"❌ 任务状态更新失败: {str(e)}"


class IntelligentAgent:
    """智能Agent主类"""
    
    def __init__(self):
        self.logger = AgentLogger()
        self.file_manager = FileManagerTool()
        self.task_manager = TaskManagerTool()
        
        # 初始化Langfuse
        self.langfuse = get_client()
        self.langfuse_handler = LangfuseCallbackHandler(
            user_id="agent-user",
            session_id=f"agent-session-{int(time.time())}"
        )
        
        # 初始化LLM
        self.llm = ChatOpenAI(
            temperature=config.default_temperature,
            model_name=config.default_model,
            callbacks=[self.langfuse_handler]
        )
        
        # 初始化记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 创建工具
        self.tools = self._create_tools()
        
        # 初始化Agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            callbacks=[self.langfuse_handler],
            handle_parsing_errors=True
        )
        
        self.logger.info("智能Agent初始化完成")
    
    def _create_tools(self) -> List[Tool]:
        """创建工具列表"""
        tools = [
            Tool(
                name="计算器",
                func=CalculatorTool.calculate,
                description="执行数学计算。输入数学表达式，如 '2 + 2' 或 'sqrt(16)'"
            ),
            Tool(
                name="天气查询",
                func=WeatherTool.get_weather,
                description="查询城市天气信息。输入城市名称，如 '北京' 或 '上海'"
            ),
            Tool(
                name="创建文件",
                func=lambda x: self._parse_file_create(x),
                description="创建文件。输入格式：'filename.txt|文件内容'"
            ),
            Tool(
                name="读取文件",
                func=self.file_manager.read_file,
                description="读取文件内容。输入文件名，如 'test.txt'"
            ),
            Tool(
                name="列出文件",
                func=lambda x: self.file_manager.list_files(),
                description="列出工作空间中的所有文件"
            ),
            Tool(
                name="数据分析",
                func=DataAnalysisTool.analyze_numbers,
                description="分析数字列表。输入逗号分隔的数字，如 '1,2,3,4,5'"
            ),
            Tool(
                name="生成图表数据",
                func=DataAnalysisTool.generate_chart_data,
                description="生成图表数据。输入数据类型：'random' 或 'time_series'"
            ),
            Tool(
                name="创建任务",
                func=lambda x: self._parse_task_create(x),
                description="创建新任务。输入格式：'任务标题|任务描述|优先级(high/medium/low)'"
            ),
            Tool(
                name="列出任务",
                func=lambda x: self.task_manager.list_tasks(),
                description="列出所有任务"
            ),
            Tool(
                name="更新任务状态",
                func=lambda x: self._parse_task_update(x),
                description="更新任务状态。输入格式：'任务ID|状态(待办/进行中/已完成)'"
            )
        ]
        return tools
    
    def _parse_file_create(self, input_str: str) -> str:
        """解析文件创建输入"""
        try:
            if "|" not in input_str:
                return "❌ 输入格式错误，请使用：'filename.txt|文件内容'"
            filename, content = input_str.split("|", 1)
            return self.file_manager.create_file(filename.strip(), content.strip())
        except Exception as e:
            return f"❌ 文件创建解析失败: {str(e)}"
    
    def _parse_task_create(self, input_str: str) -> str:
        """解析任务创建输入"""
        try:
            parts = input_str.split("|")
            title = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            priority = parts[2].strip() if len(parts) > 2 else "medium"
            return self.task_manager.create_task(title, description, priority)
        except Exception as e:
            return f"❌ 任务创建解析失败: {str(e)}"
    
    def _parse_task_update(self, input_str: str) -> str:
        """解析任务状态更新输入"""
        try:
            if "|" not in input_str:
                return "❌ 输入格式错误，请使用：'任务ID|状态'"
            task_id_str, status = input_str.split("|", 1)
            task_id = int(task_id_str.strip())
            return self.task_manager.update_task_status(task_id, status.strip())
        except ValueError:
            return "❌ 任务ID必须是数字"
        except Exception as e:
            return f"❌ 任务状态更新解析失败: {str(e)}"
    
    def run_task(self, query: str) -> str:
        """执行任务"""
        try:
            self.logger.info(f"收到任务: {query}")
            
            # 使用Langfuse追踪
            with self.langfuse.start_as_current_span(name="agent-task") as span:
                span.update(input=query)
                
                # 执行Agent
                result = self.agent.run(query)
                
                span.update(output=result)
                self.logger.info("任务执行完成")
                
                return result
        except Exception as e:
            error_msg = f"任务执行失败: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def interactive_mode(self):
        """交互模式"""
        print("🤖 智能Agent已启动！输入 'quit' 退出")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 您: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                    print("👋 再见！")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 Agent: ", end="")
                response = self.run_task(user_input)
                print(response)
                
                # 刷新Langfuse数据
                self.langfuse.flush()
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误: {str(e)}")
    
    def demo_tasks(self):
        """演示任务"""
        demo_queries = [
            "计算 25 * 4 + 10 的结果",
            "查询北京的天气情况",
            "创建一个名为 demo.txt 的文件，内容是 'Hello, World!'",
            "读取 demo.txt 文件",
            "分析这些数字：10,20,30,40,50,60,70,80,90,100",
            "创建一个任务：完成项目文档|编写完整的项目文档|high",
            "列出所有任务",
            "将任务1的状态更新为进行中"
        ]
        
        print("🎯 开始演示任务...")
        for i, query in enumerate(demo_queries, 1):
            print(f"\n📋 演示任务 {i}: {query}")
            print("-" * 50)
            response = self.run_task(query)
            print(f"🤖 回复: {response}")
            time.sleep(1)  # 短暂延迟
        
        print("\n✅ 演示任务完成！")
        self.langfuse.flush()


def main():
    """主函数"""
    print("🚀 启动智能Agent项目...")
    
    # 显示配置信息
    config.print_config()
    
    # 创建Agent实例
    agent = IntelligentAgent()
    
    # 选择运行模式
    print("\n请选择运行模式:")
    print("1. 交互模式 (interactive)")
    print("2. 演示模式 (demo)")
    print("3. 单次任务 (single)")
    
    choice = input("请输入选择 (1/2/3): ").strip()
    
    if choice == "1":
        agent.interactive_mode()
    elif choice == "2":
        agent.demo_tasks()
    elif choice == "3":
        task = input("请输入任务: ").strip()
        if task:
            result = agent.run_task(task)
            print(f"结果: {result}")
    else:
        print("无效选择，启动交互模式...")
        agent.interactive_mode()


if __name__ == "__main__":
    main() 