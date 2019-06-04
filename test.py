class Test:
    a = 1
    b = 2
    c = 3


def maketest(*args):
    test = Test()
    for i in args:
        test.i = 0
    print(test.a)
    print(test.b)
    print(test.c)


a = b = c = 9

for i in range(a):
    print(i)