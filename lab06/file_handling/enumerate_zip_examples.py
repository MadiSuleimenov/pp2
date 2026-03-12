# enumerate_zip_examples.py
# 5 examples of enumerate() and zip()

# Example 1: enumerate() list items
print("Example 1: enumerate() list items")
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(index, fruit)

print("-" * 40)

# Example 2: enumerate() starting from 1
print("Example 2: enumerate() starting from 1")
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)

print("-" * 40)

# Example 3: zip() two lists
print("Example 3: zip() two lists")
names = ["Ali", "Aruzhan", "Madi"]
scores = [85, 90, 78]
result = list(zip(names, scores))
print(result)

print("-" * 40)

# Example 4: Loop through zipped lists
print("Example 4: Loop through zipped lists")
names = ["Ali", "Aruzhan", "Madi"]
scores = [85, 90, 78]
for name, score in zip(names, scores):
    print(name, score)

print("-" * 40)

# Example 5: Create dictionary using zip()
print("Example 5: Create dictionary using zip()")
keys = ["name", "age", "city"]
values = ["Madi", 18, "Almaty"]
person = dict(zip(keys, values))
print(person)