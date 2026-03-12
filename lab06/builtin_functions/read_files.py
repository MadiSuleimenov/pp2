# read_files.py
# 5 examples of reading files in Python

# Example 1: Read entire file
print("Example 1: Read entire file")
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

print("-" * 40)

# Example 2: Read first 10 characters
print("Example 2: Read first 10 characters")
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read(10)
    print(content)

print("-" * 40)

# Example 3: Read one line
print("Example 3: Read one line")
with open("sample.txt", "r", encoding="utf-8") as f:
    line = f.readline()
    print(line)

print("-" * 40)

# Example 4: Read all lines into a list
print("Example 4: Read all lines into a list")
with open("sample.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(lines)

print("-" * 40)

# Example 5: Loop through file line by line
print("Example 5: Loop through file line by line")
with open("sample.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())