# map_filter_reduce.py
# 5 examples of map(), filter(), and reduce()

from functools import reduce

# Example 1: map() - square numbers
print("Example 1: map() square numbers")
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
print(squares)

print("-" * 40)

# Example 2: map() - convert strings to integers
print("Example 2: map() strings to integers")
nums = ["1", "2", "3", "4"]
integers = list(map(int, nums))
print(integers)

print("-" * 40)

# Example 3: filter() - keep even numbers
print("Example 3: filter() even numbers")
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)

print("-" * 40)

# Example 4: filter() - keep positive numbers
print("Example 4: filter() positive numbers")
numbers = [-2, -1, 0, 1, 2, 3]
positives = list(filter(lambda x: x > 0, numbers))
print(positives)

print("-" * 40)

# Example 5: reduce() - sum all numbers
print("Example 5: reduce() sum all numbers")
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, numbers)
print(total)