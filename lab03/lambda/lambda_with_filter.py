# 1
numbers = [1, 2, 3, 4]
result = filter(lambda x: x % 2 == 0, numbers)
print(list(result))

# 2
numbers = [5, 10, 15]
print(list(filter(lambda x: x > 7, numbers)))

# 3
numbers = [-1, 2, -3, 4]
print(list(filter(lambda x: x > 0, numbers)))

# 4
words = ["apple", "hi", "banana"]
print(list(filter(lambda x: len(x) > 3, words)))

# 5
numbers = [0, 1, 2]
print(list(filter(lambda x: x, numbers)))
