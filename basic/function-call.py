# 方法引用 import 方法名 引用方法1,引用方法2....
from function import my_abs,trim_spaces,find_min_max
print(my_abs(-1))
print(trim_spaces('  hello world  ')=='hello world')
# 测试找到最小值，最大值
if find_min_max([] != (None, None)):
    print('测试失败!')
elif find_min_max([7]) != (7, 7):
    print('测试失败!')
elif find_min_max([7, 1]) != (1, 7):
    print('测试失败!')
elif find_min_max([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
