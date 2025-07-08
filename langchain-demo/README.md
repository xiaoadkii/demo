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

# 运行 LangChain Agent
python langchain-agent.py

# 运行 Langfuse 集成示例
python langfuse-cal.py
```

## 📁 项目结构

```
langchain-demo/
├── config.env              # 环境变量配置文件
├── config.py               # 配置管理模块
├── langchain-agent.py      # LangChain Agent 示例
├── langfuse-cal.py         # Langfuse 集成示例
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

## 📚 相关链接

- [LangChain 文档](https://python.langchain.com/)
- [Langfuse 文档](https://langfuse.com/docs)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [python-dotenv 文档](https://python-dotenv.readthedocs.io/) 