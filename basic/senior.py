from collections.abc import Iterable, Iterator
# python高级用法
# 1.切片 slice（相当于java中的substr，只不过比subStr更强大，可以对list/tuple/str都能进行操作，原类型是什么，切片后还是什么类型）
# : 切片是按照索引进行取值，切片的索引可以省略，如果省略，默认为0,正着取是从左到右（索引为0开始，取到索引为N-1），负数从右到左（索引为-1开始，取到-N）
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
# ['Michael', 'Sarah', 'Tracy']
print(L[0:3])
# ['Michael', 'Sarah', 'Tracy']
print(L[:3])
# ['Sarah', 'Tracy', 'Bob', 'Jack']
print(L[1:])
# ['Bob', 'Jack']
print(L[-2:])
# ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(L[:])
print(L[::])
# 每隔2 个取一个
# ['Michael', 'Tracy']
print(L[:4:2])
# ['Michael', 'Tracy', 'Jack']
print(L[::2])
# 迭代，不仅可以用在list或tuple上，只要是可迭代对象都可以用for循环迭代。比如dict、str、tuple、set、list、range等。
# dict迭代的是key。如果要迭代value，可以用for value in d.values()，如果要同时迭代key和value，可以用for k, v in d.items()
d={'a':1,'b':2,'c':3}
for key in d:
    print(key)
    print(d[key])

for ch in 'hello':
    print(ch)
# 实现Java中的下标循环
for i,value in enumerate(['A','B','C']):
    print(i,value)

# generator 生成器一边计算一算生成，避免占用太多内容，列表生成的[]改为()就是生成器，生成器只有在需要时才计算，节省内存。另外生成器也可以用next()函数获取下一个值，但是只能获取一次，再次获取会报错。
# 生成器中用yield 关键字可以返回一个值，并且保存当前状态，下次再获取时从这里继续往下执行。
#生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator。
# 把list、dict、str等Iterable变成Iterator可以使用iter()函数：

isinstance(iter([]), Iterator)
# True
isinstance(iter('abc'), Iterator)
# True