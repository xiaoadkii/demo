#!/usr/bin/env python3
import os
import requests
from langfuse import get_client

# 设置环境变量
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-c9c9c3ed-9ea8-434b-8b03-13059445a862"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-15ffe0a8-fe0e-474b-8b11-a088ccbd27dc"
os.environ["LANGFUSE_HOST"] = "http://localhost:3300"

print("=== Langfuse 连接测试 ===")

# 1. 测试基本HTTP连接
print("\n1. 测试基本 HTTP 连接...")
try:
    response = requests.get("http://localhost:3300")
    print(f"✅ HTTP 连接成功: {response.status_code}")
except Exception as e:
    print(f"❌ HTTP 连接失败: {e}")
    exit(1)

# 2. 测试健康检查端点
print("\n2. 测试健康检查端点...")
try:
    response = requests.get("http://localhost:3300/api/public/health")
    print(f"✅ 健康检查成功: {response.status_code}")
    if response.status_code == 200:
        print(f"响应内容: {response.text}")
except Exception as e:
    print(f"❌ 健康检查失败: {e}")

# 3. 测试 Langfuse 客户端
print("\n3. 测试 Langfuse 客户端...")
try:
    langfuse = get_client()
    print("✅ 客户端创建成功")
    
    # 测试认证
    auth_result = langfuse.auth_check()
    print(f"认证结果: {auth_result}")
    
    if auth_result:
        print("✅ 认证成功")
    else:
        print("❌ 认证失败")
        
except Exception as e:
    print(f"❌ 客户端测试失败: {e}")
    import traceback
    traceback.print_exc()

# 4. 创建简单的追踪测试
print("\n4. 创建简单的追踪测试...")
try:
    langfuse = get_client()
    
    with langfuse.start_as_current_span(name="test-trace") as span:
        span.update_trace(user_id="test-user")
        span.update(
            input="测试输入",
            output="测试输出",
            metadata={"test": True}
        )
        print(f"✅ 追踪创建成功，ID: {span.trace_id}")
    
    # 刷新数据
    langfuse.flush()
    print("✅ 数据已刷新")
    
except Exception as e:
    print(f"❌ 追踪创建失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试完成 ===")
print("如果所有测试都通过，请检查 Langfuse 控制台中的 Traces 页面") 