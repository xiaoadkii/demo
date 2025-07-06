# 使用前先pip install redis
import redis
print('程序开始运行')
# 创建连接
r = redis.Redis(host='localhost', port=16379, password='myredissecret', decode_responses=True)

# 设置 key
r.set('name', 'LingDi')

# 获取 key
value = r.get('name')
print(value)  # 输出: LingDi
