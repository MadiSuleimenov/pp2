# create_list_dirs.py
# 5 examples of directory management in Python

import os

# Example 1: Create a directory
print("Example 1: Create a directory")
if not os.path.exists("new_folder"):
    os.mkdir("new_folder")
    print("Directory created")
else:
    print("Directory already exists")

print("-" * 40)

# Example 2: Create nested directories
print("Example 2: Create nested directories")
os.makedirs("parent/child/grandchild", exist_ok=True)
print("Nested directories created")

print("-" * 40)

# Example 3: List files and folders in current directory
print("Example 3: List files and folders")
items = os.listdir(".")
for item in items:
    print(item)

print("-" * 40)

# Example 4: Check if path is a directory
print("Example 4: Check if path is a directory")
path = "new_folder"
if os.path.isdir(path):
    print(f"{path} is a directory")
else:
    print(f"{path} is not a directory")

print("-" * 40)

# Example 5: Get current working directory
print("Example 5: Current working directory")
cwd = os.getcwd()
print(cwd)