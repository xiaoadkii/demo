#!/usr/bin/env python3
import os
from langfuse import get_client

# 使用云端 Langfuse 进行测试
# 你需要在 https://cloud.langfuse.com 注册并获取新的密钥
print("注意：请先在 https://cloud.langfuse.com 注册并获取API密钥")
print("然后替换下面的密钥")

# 替换为你的云端密钥
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-your-cloud-secret-key"  
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-your-cloud-public-key"   
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"  # 云端服务

print("=== 云端 Langfuse 测试 ===")

try:
    langfuse = get_client()
    
    # 测试认证
    print("正在测试认证...")
    auth_result = langfuse.auth_check()
    print(f"认证结果: {auth_result}")
    
    if auth_result:
        print("✅ 云端认证成功")
        
        # 创建测试追踪
        with langfuse.start_as_current_span(name="cloud-test-trace") as span:
            span.update_trace(user_id="cloud-test-user")
            span.update(
                input="云端测试输入",
                output="云端测试输出"
            )
            print(f"✅ 云端追踪创建成功，ID: {span.trace_id}")
        
        langfuse.flush()
        print("✅ 数据已发送到云端 Langfuse")
        print("请访问 https://cloud.langfuse.com 查看数据")
        
    else:
        print("❌ 云端认证失败，请检查密钥")
        
except Exception as e:
    print(f"❌ 云端测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 云端测试完成 ===") 