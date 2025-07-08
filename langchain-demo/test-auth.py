#!/usr/bin/env python3
import requests
import os
import json

# 设置环境变量
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-c9c9c3ed-9ea8-434b-8b03-13059445a862"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-212b5088-bee4-49f2-ab38-4194057e54b9"
os.environ["LANGFUSE_HOST"] = "http://localhost:3300"

print("=== API 认证测试 ===")
print(f"Secret Key: {os.environ['LANGFUSE_SECRET_KEY']}")
print(f"Public Key: {os.environ['LANGFUSE_PUBLIC_KEY']}")
print(f"Host: {os.environ['LANGFUSE_HOST']}")

# 测试不同的认证方式
print("\n1. 测试 Basic Auth...")
try:
    import base64
    
    # 使用 Basic Auth（public:secret）
    auth_string = f"{os.environ['LANGFUSE_PUBLIC_KEY']}:{os.environ['LANGFUSE_SECRET_KEY']}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"{os.environ['LANGFUSE_HOST']}/api/public/projects", headers=headers)
    print(f"Basic Auth 状态码: {response.status_code}")
    print(f"Basic Auth 响应: {response.text[:200]}")
    
except Exception as e:
    print(f"Basic Auth 错误: {e}")

print("\n2. 测试 Bearer Token...")
try:
    headers = {
        'Authorization': f'Bearer {os.environ["LANGFUSE_SECRET_KEY"]}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"{os.environ['LANGFUSE_HOST']}/api/public/projects", headers=headers)
    print(f"Bearer Token 状态码: {response.status_code}")
    print(f"Bearer Token 响应: {response.text[:200]}")
    
except Exception as e:
    print(f"Bearer Token 错误: {e}")

print("\n3. 测试 API Keys 端点...")
try:
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"{os.environ['LANGFUSE_HOST']}/api/public/health", headers=headers)
    print(f"Health 状态码: {response.status_code}")
    print(f"Health 响应: {response.text}")
    
except Exception as e:
    print(f"Health 错误: {e}")

print("\n=== 测试完成 ===") 