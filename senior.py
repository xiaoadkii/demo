
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
