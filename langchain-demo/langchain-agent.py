from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# 导入配置管理模块
from config import config

# 配置会自动从 config.env 加载并设置环境变量
config.print_config()

# 使用 DeepSeek 替代 OpenAI 模型
llm = ChatOpenAI(
    temperature=config.default_temperature,
    model_name=config.default_model,
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
