from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
import os

# 设置 DeepSeek 的 API Key 和 Base URL
os.environ["OPENAI_API_KEY"] = "sk-e8efc0c16aec40b898a6ea2556f9e7c3"
os.environ["OPENAI_API_BASE"] = "https://api.deepseek.com"  # 示例 URL，按实际为准

# 使用 DeepSeek 替代 OpenAI 模型
llm = ChatOpenAI(
    temperature=0,
    model_name="deepseek-chat",   # 或 deepseek-coder，如支持
)

# 示例工具（计算器）
def calculator(input_str):
    try:
        return str(eval(input_str))
    except Exception as e:
        return str(e)

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="用来执行数学计算。输入如 '2 + 2'"
    )
]

# 初始化 Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 测试执行
agent.run("计算一下 123 * 456 是多少")
