# 函数相关
# 定义函数
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x

def  power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
def none():
    pass

# 默认参数必须指向不变对象，比如数字、字符串、元组，但是不能是列表、字典、集合。以下代码每次调用都会在原来列表上中添加一个元素，导致下次调用时，参数列表中的列表已经不是原来的列表了。
def app_end(L=[]):
    L.append('END')
    return L

#  解决方法: 创建一个空列表，在函数内部返回该列表。
def app_end2(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
# 可变参数, *numbers是可变参数，可以传入任意个数参数，返回一个tuple。
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
# 关键字参数  **kw是关键字参数，可以传入任意个数关键字参数，返回一个dict。
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

# 命名关键字参数，和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数。
# def person2(name, age, *, city, job):
def person2(name, age, *param,city, job):
    print(name, age, city, job)

# 删除前后空格
def trim_spaces(s):
    if not isinstance(s, str):
        raise TypeError('bad operand type')
    start=0
    end=len(s)-1
    while start <= end and s[start]=='':
        start = start + 1
    while end > start and s[end]=='':
        end = end - 1
    return s[start:end+1]

def find_min_max(nums):
    if not nums:
        return (None, None)
    min_val = nums[0]
    max_val = nums[0]
    for n in nums:
        if n < min_val:
            min = n
        elif n > max_val:
            max = n
    return (min_val, max_val)

# 以下代码块代表只有在执行py文件时才会执行，普通方法调用是不会走到这里的
if __name__ == '__main__':
    # 函数调用
    # print(my_abs(-1))
    # inputV=input("请输入内容：")
    # print(my_abs(int(inputV)))
    # app_end2()
    print(app_end2())
    print(calc(1,2,3))
    nums=[1,2,3]
    # 在list或tuple等可迭代对象，用*号把函数参数变成可变参数。
    print(calc(*nums))
    # **kw表示接受任意个数关键字参数， kw是一个dict，如果函数定义中已经有了**kw参数，那么**kw只能定义在函数参数列表的末尾。
    person('Michael', 30)
    person('Bob', 35, city='Beijing')
    person('Adam', 45, gender='M', job='Engineer')
    person2('Adam', 45, city='Beijing', job='Engineer')

# 定义函数时，需要确定函数名和参数个数；

#如果有必要，可以先对参数的数据类型做检查；

#函数体内部可以用return随时返回函数结果；

#函数执行完毕也没有return语句时，自动return None。

#函数可以同时返回多个值，但其实就是一个tuple。
"""
Python的函数具有非常灵活的参数形态，既可以实现简单的调用，又可以传入非常复杂的参数。

默认参数一定要用不可变对象，如果是可变对象，程序运行时会有逻辑错误！

要注意定义可变参数和关键字参数的语法：

*args是可变参数，args接收的是一个tuple；

**kw是关键字参数，kw接收的是一个dict。

以及调用函数时如何传入可变参数和关键字参数的语法：

可变参数既可以直接传入：func(1, 2, 3)，又可以先组装list或tuple，再通过*args传入：func(*(1, 2, 3))；

关键字参数既可以直接传入：func(a=1, b=2)，又可以先组装dict，再通过**kw传入：func(**{'a': 1, 'b': 2})。

使用*args和**kw是Python的习惯写法，当然也可以用其他参数名，但最好使用习惯用法。

命名的关键字参数是为了限制调用者可以传入的参数名，同时可以提供默认值。

定义命名的关键字参数在没有可变参数的情况下不要忘了写分隔符*，否则定义的将是位置参数。
"""