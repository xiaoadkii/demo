#!/usr/bin/env python3
import requests
import os
import base64

# 请您替换为从 Langfuse 控制台获取的正确密钥
SECRET_KEY = "sk-lf-c9c9c3ed-9ea8-434b-8b03-13059445a862"  # sk-lf-开头
PUBLIC_KEY = "pk-lf-212b5088-bee4-49f2-ab38-4194057e54b9"  # pk-lf-开头
HOST = "http://localhost:3300"

print("=== API 密钥测试 ===")
print(f"Secret Key: {SECRET_KEY}")
print(f"Public Key: {PUBLIC_KEY}")
print(f"Host: {HOST}")

if SECRET_KEY.startswith("请替换") or PUBLIC_KEY.startswith("请替换"):
    print("❌ 请先在代码中替换为正确的 API 密钥")
    exit(1)

# 测试 Basic Auth
print("\n正在测试 Basic Auth...")
try:
    auth_string = f"{PUBLIC_KEY}:{SECRET_KEY}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"{HOST}/api/public/projects", headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    if response.status_code == 200:
        print("✅ API 认证成功！")
        print("现在您可以使用这些密钥更新 langfuse-cal.py 文件")
    else:
        print("❌ API 认证失败，请检查密钥是否正确")
        
except Exception as e:
    print(f"❌ 测试失败: {e}")

print("\n=== 测试完成 ===")
print("如果认证成功，请复制这些密钥到 langfuse-cal.py 中") 