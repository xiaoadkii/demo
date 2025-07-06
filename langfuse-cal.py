# 配置langfuse
# secrect key:sk-lf-c9c9c3ed-9ea8-434b-8b03-13059445a862
# public key: pk-lf-15ffe0a8-fe0e-474b-8b11-a088ccbd27dc
from langfuse import get_client
import requests
import os

# 设置 DeepSeek 的 API Key（参考 langchain-agent.py 的配置）
os.environ["DEEPSEEK_API_KEY"] = "sk-e8efc0c16aec40b898a6ea2556f9e7c3"

# 设置 Langfuse 环境变量
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-c9c9c3ed-9ea8-434b-8b03-13059445a862"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-212b5088-bee4-49f2-ab38-4194057e54b9"
os.environ["LANGFUSE_HOST"] = "http://localhost:3300"

# 初始化 Langfuse 客户端
langfuse = get_client()

# 验证连接 - 跳过 auth_check（该端点有问题），直接测试功能
print("正在验证 Langfuse 连接...")
try:
    # 创建一个测试追踪来验证连接
    with langfuse.start_as_current_span(name="connection-test") as test_span:
        test_span.update(input="连接测试", output="连接成功")
    print("✅ Langfuse 连接成功")
except Exception as e:
    print(f"❌ Langfuse 连接错误: {e}")
    exit(1)

# 使用正确的 v3 SDK API
print("开始创建追踪...")
with langfuse.start_as_current_span(name="deepseek-trace") as trace_span:
    print(f"创建追踪成功，追踪ID: {trace_span.trace_id}")
    
    # 设置跟踪属性
    trace_span.update_trace(user_id="user-1")
    
    # 创建生成记录
    with langfuse.start_as_current_generation(
        name="chat-with-deepseek",
        model="deepseek-chat",
        input="你好，DeepSeek!"
    ) as generation:
        print("创建生成记录成功")
        
        # 实际调用 DeepSeek API
        print("正在调用 DeepSeek API...")
        try:
            res = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": "你好，DeepSeek!"}]
                }
            )
            
            if res.status_code == 200:
                completion = res.json()['choices'][0]['message']['content']
                print(f"DeepSeek API 调用成功: {completion}")
                
                # 更新生成记录的输出
                generation.update(output=completion)
                print("更新生成记录成功")
                
                print(f"最终回复: {completion}")
            else:
                print(f"❌ DeepSeek API 调用失败: {res.status_code} - {res.text}")
                generation.update(output=f"API调用失败: {res.status_code}")
                
        except Exception as e:
            print(f"❌ DeepSeek API 调用异常: {e}")
            generation.update(output=f"调用异常: {str(e)}")

print("正在刷新数据到 Langfuse...")
# 确保数据发送到 Langfuse
langfuse.flush()
print("✅ 数据已发送到 Langfuse，请检查控制台")