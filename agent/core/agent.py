"""
Agent核心类
"""

from typing import Optional, List, Dict, Any


class BaseAgent:
    """Agent基础类"""
    
    def __init__(self, name: str = "BaseAgent"):
        self.name = name
        self.tools: List = []
        self.memory: Optional[Any] = None
    
    def add_tool(self, tool):
        """添加工具"""
        self.tools.append(tool)
    
    def run(self, query: str) -> str:
        """执行任务"""
        return f"Agent {self.name} 处理: {query}" 