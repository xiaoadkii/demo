# LangChain Demo 项目

这个项目演示了如何使用 LangChain 和 Langfuse 进行 AI 应用开发和观测。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

项目使用 `config.env` 文件管理配置。主要配置项：

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=your-deepseek-api-key
OPENAI_API_KEY=your-deepseek-api-key
OPENAI_API_BASE=https://api.deepseek.com

# Langfuse 配置
LANGFUSE_SECRET_KEY=your-langfuse-secret-key
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
LANGFUSE_HOST=http://localhost:3300
LANGFUSE_PROJECT_ID=your-project-id
LANGFUSE_ORG_ID=your-org-id

# 模型配置
DEFAULT_MODEL=deepseek-chat
DEFAULT_TEMPERATURE=0

# 日志配置
LOG_LEVEL=DEBUG
```

### 3. 运行示例

```bash
# 测试配置
python config.py

# 🚀 快速启动完整Agent项目（推荐）
python quick_start.py

# 运行完整智能Agent项目
python agent_project.py

# 运行基础 LangChain Agent
python langchain-agent.py

# 运行 Langfuse 集成示例
python langfuse-cal.py
```

## 📁 项目结构

```
langchain-demo/
├── config.env              # 环境变量配置文件
├── config.py               # 配置管理模块
├── langchain-agent.py      # LangChain Agent 基础示例
├── langfuse-cal.py         # Langfuse 集成示例
├── agent_project.py        # 完整智能Agent项目 ⭐
├── quick_start.py          # 快速启动脚本 🚀
├── requirements.txt        # 项目依赖
└── README.md              # 项目说明
```

## 🔧 配置说明

### config.py 模块功能

- **自动加载配置**: 从 `config.env` 文件加载环境变量
- **类型转换**: 支持字符串、整数、浮点数、布尔值类型
- **默认值**: 为配置项提供合理的默认值
- **环境变量设置**: 自动将配置设置到系统环境变量中
- **安全显示**: 打印配置时隐藏敏感信息

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 必需 |
| `OPENAI_API_BASE` | API 基础 URL | `https://api.deepseek.com` |
| `LANGFUSE_SECRET_KEY` | Langfuse Secret Key | 必需 |
| `LANGFUSE_PUBLIC_KEY` | Langfuse Public Key | 必需 |
| `LANGFUSE_HOST` | Langfuse 服务地址 | `http://localhost:3300` |
| `DEFAULT_MODEL` | 默认模型名称 | `deepseek-chat` |
| `DEFAULT_TEMPERATURE` | 默认温度参数 | `0.0` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

## 🔐 安全注意事项

1. **不要提交敏感信息**: `config.env` 文件包含 API 密钥，不应提交到版本控制系统
2. **使用环境变量**: 在生产环境中使用系统环境变量而非配置文件
3. **权限控制**: 确保配置文件只有必要的用户可以访问

## 📝 使用示例

### 基本用法

```python
from config import config

# 获取配置值
api_key = config.deepseek_api_key
model = config.default_model

# 配置会自动设置到环境变量中
import os
print(os.getenv("OPENAI_API_KEY"))  # 自动设置
```

### 自定义配置

```python
from config import Config

# 使用自定义配置文件
custom_config = Config("my-config.env")

# 获取特定类型的配置
temperature = custom_config.get_float("TEMPERATURE", 0.7)
debug_mode = custom_config.get_bool("DEBUG", False)
```

## 🛠️ 开发指南

1. **修改配置**: 编辑 `config.env` 文件
2. **添加新配置**: 在 `config.py` 中添加对应的属性方法
3. **测试配置**: 运行 `python config.py` 验证配置
4. **使用配置**: 导入 `config` 对象并使用其属性

## 🤖 完整智能Agent项目

### 🌟 项目亮点

`agent_project.py` 是一个功能完整的智能Agent项目，包含：

#### 🛠️ 多种工具集成
- **计算器**: 安全的数学计算（支持复杂表达式）
- **天气查询**: 模拟天气数据查询
- **文件管理**: 创建、读取、列出文件
- **数据分析**: 统计分析（均值、中位数、标准差等）
- **任务管理**: 创建、列出、更新任务状态
- **图表数据**: 生成可视化数据

#### 🎯 核心功能
- **智能对话**: 使用 ConversationBufferMemory 保持上下文
- **完整观测**: 集成 Langfuse 全程追踪
- **错误处理**: 优雅处理异常和解析错误  
- **多种模式**: 交互、演示、单次任务
- **日志记录**: 详细的操作日志

#### 🚀 快速体验

```bash
# 方式1: 使用快速启动器（推荐新手）
python quick_start.py

# 方式2: 直接运行完整项目
python agent_project.py
```

### 📖 使用示例

#### 交互对话示例：
```
👤 您: 帮我计算一下 25 的平方根加上 100 除以 4
🤖 Agent: 我来帮您计算...
计算结果: 30.0

👤 您: 创建一个任务：学习LangChain|深入学习Agent开发|high  
🤖 Agent: ✅ 任务创建成功 (ID: 1): 学习LangChain

👤 您: 分析这些数字：1,4,7,10,13,16,19,22,25
🤖 Agent: 📊 数据分析结果:
数据: [1.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0]
总数: 9
平均值: 13.00
中位数: 13.00
...
```

#### 演示模式功能：
- 自动执行8个预设任务
- 展示所有工具功能
- 完整的 Langfuse 追踪记录

### 🎮 运行模式

1. **交互模式**: 与Agent持续对话
2. **演示模式**: 自动运行预设任务
3. **单次任务**: 执行单个任务后退出

### 🔍 观测和调试

所有Agent操作都会被 Langfuse 自动追踪：
- 用户输入和Agent回复
- 工具调用和结果
- 错误信息和性能指标
- 对话历史和上下文

在 Langfuse 控制台中可以看到：
- 完整的对话链路
- 每个工具的执行时间
- 模型的 token 使用量
- 错误堆栈和调试信息

## 📚 相关链接

- [LangChain 文档](https://python.langchain.com/)
- [Langfuse 文档](https://langfuse.com/docs)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [python-dotenv 文档](https://python-dotenv.readthedocs.io/) 