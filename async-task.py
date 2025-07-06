import  time
import  asyncio
import aiohttp
import threading
# 定义异步
def  sync_task():
    print('sync task')
    print(time.time()) 
    # await asyncio.sleep(2)
    print('sync task done')
    print(time.time())

# asyncio.run(sync_task())

sync_task()

import asyncio

async def task(name, delay):
    print(f"{name} 开始，延迟 {delay} 秒")
    await asyncio.sleep(delay)
    print(f"{name} 完成")

async def main():
    # 并发执行三个异步任务
    tasks = [
        task("任务1", 2),
        task("任务2", 1),
        task("任务3", 3)
    ]
    await asyncio.gather(*tasks)
    print("所有任务完成")

# 启动事件循环
asyncio.run(main())


def task1 ():
    print('task1')

async def task2 ():
    await asyncio.sleep(0)
    print('task2')

def taskRun(): 
    print('taskRun')
    asyncio.run(task2())
    print('taskRun2')
    task1()

taskRun()

# taskRun task2 taskRun2 task1
# taskRun taskRun2 

# 传入name参数:
async def hello(name):
    # 打印name和当前线程:
    print("Hello %s! (%s)" % (name, threading.current_thread))
    # 异步调用asyncio.sleep(1):
    await asyncio.sleep(1)
    print("Hello %s again! (%s)" % (name, threading.current_thread))
    return name

async def main():
    L = await asyncio.gather(hello("Bob"), hello("Alice"))
    print(L)

asyncio.run(main())
