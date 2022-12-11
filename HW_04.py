def maximum(a, b):
    result = a
    if b > result:
        result = b
    return result


def minimum(a, b, c):
    result = a
    if b < result:
        result = b
    if c < result:
        result = c
    return result


def module(a):
    if a < 0:
        a = -a
    return a


def print_sum(a, b):
    print(a + b)


def print_sign(a):
    if a > 0:
        print("positive")
    elif a < 0:
        print("negative")
    else:
        print("zero")


print(maximum(-100, -5))
print(minimum(-100, -6, 9))
print(module(100))
print_sum(-100, 50)
print_sign(-100)
