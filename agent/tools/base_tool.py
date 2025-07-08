"""
工具基础类
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """工具基础类"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
    
    @abstractmethod
    def run(self, input_data: str) -> str:
        """执行工具"""
        pass
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}" 