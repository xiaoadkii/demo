print('hello, world')
# break 跳出循环 continue 跳过当前循环
# for  循环
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print('hello,',name)
sum = 0
# 0-9
for i in range(10):
    sum = sum + i
print(sum)
# while 循环
sumStr = '0'
n = 99
sum=int(sumStr)
while n > 0:
    sum = sum + n
    n = n-1
print(sum)
# dict 字典 相当于  java 的 map, key-value
paramMap = {'name':'Michael', 'age':30}
print(paramMap['name'])
# set 集合 相当于 java 的 set, 只有key  没有value，set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：
paramSet = {'Michael', 'Bob', 'Tracy'}
print('Michael' in paramSet)
paramSet.add('Adam')
print(len(paramSet))
paramSet.remove('Michael')
print(len(paramSet))
s1={1,2,3}
s2={3,4,5}
print('交集：',s1&s2)
print('并集: ',s1|s2)
# tuple 元组 相当于 java 的数组，tuple一旦初始化，就不能修改。tuple的创建方式如下：
paramTuple = ('Michael', 'Bob', 'Tracy')
print(paramTuple[0])
print(len(paramTuple))
#  list 列表 相当于 java 的数组，list一旦初始化，就可以修改。list的创建方式如下：
paramList = ['Michael', 'Bob', 'Tracy']
print(paramList[0])
print(len(paramList))
paramList.append('Adam')
print(len(paramList))

# name=input('please input your name:')
# print('hello',name)
print('中文测试正常')
L= [
    ['APPLE','GOOGLE','MICROSOFT'],
    ['JAVA', 'PYTHON', 'RUBY'],
    ['Adam', 'Haskell', 'Go']
]
print(L[0][0])
print(L[1][1])
print(L[2][2]) 
age=3
if age>=18:
    print('adult')
    print('third')
elif age>=6:
    print('teenager')
else:
    print('kid')

score = 'B'
match score:
    case 'A':
        print('优秀')
    case 'B':
        print('良好')
    case 'C':
        print('及格')
    case 'D':
        print('不及格')
    case _:
        print('bad')
  
age = 15
match age:
    # 匹配大于10并赋值到x
    case x if x >10:
        print('teenager')
    case 10:
        print('ten')
    case _:
        print('kid')
print(x)

args = ['gcc', 'world.c', 'hello.c']
match args:
    case ['gcc']:
        print('gcc: missing source file(s)')
    case ['gcc',file1, *files]:
        print('gcc: ' + file1+' ,' + ' ,'.join(files))    
    case [x, *rest]:
        print(x)
        print(rest)
    case _:
        print('no match')
    