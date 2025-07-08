# Agent 项目

一个模块化的智能Agent框架

## 📁 项目结构

```
agent/
├── __init__.py                 # 主包初始化
├── config/                     # 配置管理
│   ├── __init__.py
│   └── settings.py            # 配置类
├── core/                      # 核心模块
│   ├── __init__.py
│   └── agent.py              # Agent基础类
├── tools/                     # 工具模块
│   ├── __init__.py
│   └── base_tool.py          # 工具基础类
├── utils/                     # 工具模块
│   ├── __init__.py
│   └── logger.py             # 日志工具
├── config.env.example        # 环境变量示例
├── requirements.txt           # 项目依赖
└── README.md                 # 项目说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制并编辑配置文件：

```bash
cp config.env.example config.env
# 编辑 config.env 文件，填入实际的配置值
```

### 3. 基础使用

```python
from agent.config import get_config
from agent.core.agent import BaseAgent
from agent.utils.logger import get_logger

# 获取配置
config = get_config()

# 创建日志器
logger = get_logger("agent")

# 创建Agent实例
agent = BaseAgent("MyAgent")

# 运行Agent
result = agent.run("Hello, Agent!")
print(result)
```

## 🔧 扩展开发

### 添加新工具

```python
from agent.tools.base_tool import BaseTool

class MyTool(BaseTool):
    def __init__(self):
        super().__init__("MyTool", "我的自定义工具")
    
    def run(self, input_data: str) -> str:
        return f"处理: {input_data}"
```

### 扩展Agent功能

```python
from agent.core.agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyAgent")
    
    def run(self, query: str) -> str:
        # 自定义处理逻辑
        return super().run(query)
```

## 📝 开发指南

1. **配置管理**: 在 `config/` 目录下扩展配置类
2. **核心功能**: 在 `core/` 目录下实现Agent核心逻辑
3. **工具开发**: 在 `tools/` 目录下添加新的工具类
4. **工具函数**: 在 `utils/` 目录下添加辅助函数

## 📚 模块说明

- **config**: 配置管理，支持环境变量和文件配置
- **core**: Agent核心实现，包含基础的Agent类
- **tools**: 工具集合，可扩展的工具系统
- **utils**: 工具函数，日志、辅助函数等 