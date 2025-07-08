#!/usr/bin/env python3
"""
配置管理模块
使用 python-dotenv 从 config.env 文件加载环境变量
"""
import os
import logging
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("警告: python-dotenv 未安装，将使用系统环境变量")


class Config:
    """配置管理类"""
    
    def __init__(self, env_file: str = "config.env"):
        """
        初始化配置
        
        Args:
            env_file: 环境变量文件名，默认为 config.env
        """
        self.env_file = env_file
        self.load_config()
        self.setup_logging()
    
    def load_config(self) -> None:
        """加载配置文件"""
        if DOTENV_AVAILABLE:
            # 获取当前文件所在目录
            current_dir = Path(__file__).parent
            env_path = current_dir / self.env_file
            
            if env_path.exists():
                load_dotenv(env_path)
                print(f"✅ 配置文件 {self.env_file} 加载成功")
            else:
                print(f"⚠️  配置文件 {env_path} 不存在，使用系统环境变量")
        else:
            print("⚠️  python-dotenv 未安装，使用系统环境变量")
    
    def setup_logging(self) -> None:
        """设置日志级别"""
        log_level = self.get("LOG_LEVEL", "INFO")
        logging.basicConfig(
            level=getattr(logging, log_level.upper(), logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        获取配置值
        
        Args:
            key: 配置键名
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        return os.getenv(key, default)
    
    def get_required(self, key: str) -> str:
        """
        获取必需的配置值
        
        Args:
            key: 配置键名
            
        Returns:
            配置值
            
        Raises:
            ValueError: 如果配置值不存在
        """
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"必需的环境变量 {key} 未设置")
        return value
    
    def get_int(self, key: str, default: int = 0) -> int:
        """
        获取整数配置值
        
        Args:
            key: 配置键名
            default: 默认值
            
        Returns:
            整数配置值
        """
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            print(f"警告: {key}={value} 不是有效的整数，使用默认值 {default}")
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """
        获取浮点数配置值
        
        Args:
            key: 配置键名
            default: 默认值
            
        Returns:
            浮点数配置值
        """
        value = self.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            print(f"警告: {key}={value} 不是有效的浮点数，使用默认值 {default}")
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        获取布尔配置值
        
        Args:
            key: 配置键名
            default: 默认值
            
        Returns:
            布尔配置值
        """
        value = self.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
    
    # 预定义的配置属性
    @property
    def deepseek_api_key(self) -> str:
        """DeepSeek API Key"""
        return self.get_required("DEEPSEEK_API_KEY")
    
    @property
    def openai_api_key(self) -> str:
        """OpenAI API Key (用于兼容)"""
        return self.get_required("OPENAI_API_KEY")
    
    @property
    def openai_api_base(self) -> str:
        """OpenAI API Base URL"""
        return self.get("OPENAI_API_BASE", "https://api.deepseek.com")
    
    @property
    def langfuse_secret_key(self) -> str:
        """Langfuse Secret Key"""
        return self.get_required("LANGFUSE_SECRET_KEY")
    
    @property
    def langfuse_public_key(self) -> str:
        """Langfuse Public Key"""
        return self.get_required("LANGFUSE_PUBLIC_KEY")
    
    @property
    def langfuse_host(self) -> str:
        """Langfuse Host"""
        return self.get("LANGFUSE_HOST", "http://localhost:3300")
    
    @property
    def langfuse_project_id(self) -> Optional[str]:
        """Langfuse Project ID"""
        return self.get("LANGFUSE_PROJECT_ID")
    
    @property
    def langfuse_org_id(self) -> Optional[str]:
        """Langfuse Organization ID"""
        return self.get("LANGFUSE_ORG_ID")
    
    @property
    def default_model(self) -> str:
        """默认模型名称"""
        return self.get("DEFAULT_MODEL", "deepseek-chat")
    
    @property
    def default_temperature(self) -> float:
        """默认温度参数"""
        return self.get_float("DEFAULT_TEMPERATURE", 0.0)
    
    def setup_environment(self) -> None:
        """设置环境变量"""
        # 设置 DeepSeek/OpenAI 相关环境变量
        os.environ["DEEPSEEK_API_KEY"] = self.deepseek_api_key
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
        os.environ["OPENAI_API_BASE"] = self.openai_api_base
        
        # 设置 Langfuse 相关环境变量
        os.environ["LANGFUSE_SECRET_KEY"] = self.langfuse_secret_key
        os.environ["LANGFUSE_PUBLIC_KEY"] = self.langfuse_public_key
        os.environ["LANGFUSE_HOST"] = self.langfuse_host
        
        if self.langfuse_project_id:
            os.environ["LANGFUSE_PROJECT_ID"] = self.langfuse_project_id
        
        if self.langfuse_org_id:
            os.environ["LANGFUSE_ORG_ID"] = self.langfuse_org_id
        
        print("✅ 环境变量设置完成")
    
    def print_config(self) -> None:
        """打印当前配置（隐藏敏感信息）"""
        print("=== 当前配置 ===")
        print(f"DeepSeek API Key: {self.deepseek_api_key[:10]}...")
        print(f"OpenAI API Base: {self.openai_api_base}")
        print(f"Langfuse Host: {self.langfuse_host}")
        print(f"Langfuse Public Key: {self.langfuse_public_key[:10]}...")
        if self.langfuse_project_id:
            print(f"Langfuse Project ID: {self.langfuse_project_id}")
        if self.langfuse_org_id:
            print(f"Langfuse Org ID: {self.langfuse_org_id}")
        print(f"Default Model: {self.default_model}")
        print(f"Default Temperature: {self.default_temperature}")
        print("================")


# 全局配置实例
config = Config()

# 自动设置环境变量
config.setup_environment()


if __name__ == "__main__":
    # 测试配置
    config.print_config() 