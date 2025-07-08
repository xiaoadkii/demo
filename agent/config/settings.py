"""
配置设置模块
"""

from typing import Optional


class Config:
    """基础配置类"""
    
    def __init__(self):
        self.debug = False
        self.environment = "development"
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> "Config":
        """从环境变量创建配置"""
        return cls()


def get_config() -> Config:
    """获取配置实例"""
    return Config.from_env() 