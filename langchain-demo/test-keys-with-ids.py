#!/usr/bin/env python3
import requests
import os
import base64
import json

# 请您替换为从 Langfuse 控制台获取的正确密钥
SECRET_KEY = "sk-lf-c9c9c3ed-9ea8-434b-8b03-13059445a862"  # sk-lf-开头
PUBLIC_KEY = "pk-lf-212b5088-bee4-49f2-ab38-4194057e54b9"  # pk-lf-开头
HOST = "http://localhost:3300"

# 组织和项目ID
ORG_ID = "cmcr46s390000nu07erofy4s8"
PROJECT_ID = "cmcr474rp0005nu07pnr2lorj"

print("=== 完整 API 密钥测试 ===")
print(f"Secret Key: {SECRET_KEY}")
print(f"Public Key: {PUBLIC_KEY}")
print(f"Host: {HOST}")
print(f"Org ID: {ORG_ID}")
print(f"Project ID: {PROJECT_ID}")

if SECRET_KEY.startswith("请替换") or PUBLIC_KEY.startswith("请替换"):
    print("❌ 请先在代码中替换为正确的 API 密钥")
    exit(1)

# 准备认证
auth_string = f"{PUBLIC_KEY}:{SECRET_KEY}"
auth_bytes = auth_string.encode('ascii')
auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json'
}

print("\n=== 测试系列 ===")

# 测试 1: 基本项目列表
print("\n1. 测试项目列表...")
try:
    response = requests.get(f"{HOST}/api/public/projects", headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ 找到 {len(projects)} 个项目")
        for project in projects:
            print(f"  - 项目: {project.get('name', 'N/A')} (ID: {project.get('id', 'N/A')})")
    else:
        print("❌ 项目列表获取失败")
        
except Exception as e:
    print(f"❌ 测试失败: {e}")

# 测试 2: 特定项目的Traces端点
print(f"\n2. 测试特定项目的Traces端点...")
try:
    url = f"{HOST}/api/public/traces"
    params = {"projectId": PROJECT_ID}
    
    response = requests.get(url, headers=headers, params=params)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text[:200]}...")
    
    if response.status_code == 200:
        print("✅ 项目Traces端点可访问")
    else:
        print("❌ 项目Traces端点访问失败")
        
except Exception as e:
    print(f"❌ 测试失败: {e}")

# 测试 3: 创建一个简单的trace
print(f"\n3. 测试创建Trace...")
try:
    url = f"{HOST}/api/public/traces"
    
    trace_data = {
        "id": "test-trace-123",
        "name": "API测试trace",
        "userId": "test-user",
        "projectId": PROJECT_ID,
        "metadata": {"test": True}
    }
    
    response = requests.post(url, headers=headers, json=trace_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    if response.status_code in [200, 201]:
        print("✅ Trace创建成功")
    else:
        print("❌ Trace创建失败")
        
except Exception as e:
    print(f"❌ 测试失败: {e}")

# 测试 4: 使用 SDK 方式测试
print(f"\n4. 测试 SDK 方式...")
try:
    os.environ["LANGFUSE_SECRET_KEY"] = SECRET_KEY
    os.environ["LANGFUSE_PUBLIC_KEY"] = PUBLIC_KEY
    os.environ["LANGFUSE_HOST"] = HOST
    os.environ["LANGFUSE_PROJECT_ID"] = PROJECT_ID
    os.environ["LANGFUSE_ORG_ID"] = ORG_ID
    
    from langfuse import get_client
    
    langfuse = get_client(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY", "pk-xxx"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY", "sk-yyy"),
        host=os.getenv("LANGFUSE_HOST", "http://localhost:3300"),
        project_id=os.getenv("LANGFUSE_PROJECT_ID", "cmcr474rp0005nu07pnr2lorj"),
        organization_id=os.getenv("LANGFUSE_ORG_ID", "cmcr46s390000nu07erofy4s8"),
    )
    
    # 创建测试trace
    with langfuse.start_as_current_span(name="sdk-test-trace") as span:
        span.update(input="SDK测试输入", output="SDK测试输出")
        span.update_trace(user_id="sdk-test-user")
        print(f"✅ SDK Trace创建成功，ID: {span.trace_id}")
    
    # 刷新数据
    langfuse.flush()
    print("✅ SDK 数据已刷新")
    
except Exception as e:
    print(f"❌ SDK 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试完成 ===")
print("如果所有测试都通过，说明密钥配置正确") 