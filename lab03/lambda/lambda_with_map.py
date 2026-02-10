# 1
numbers = [1, 2, 3]
result = map(lambda x: x * 2, numbers)
print(list(result))

# 2
numbers = [5, 10, 15]
print(list(map(lambda x: x + 1, numbers)))

# 3
numbers = [1, 4, 9]
print(list(map(lambda x: x * x, numbers)))

# 4
numbers = [2, 4, 6]
print(list(map(lambda x: x // 2, numbers)))

# 5
numbers = [10, 20]
print(list(map(lambda x: str(x), numbers)))
