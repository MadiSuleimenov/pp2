# move_files.py
# 5 examples of moving files in Python

import os
import shutil

# Example 1: Move file to another folder
print("Example 1: Move file to another folder")
os.makedirs("destination", exist_ok=True)
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "destination/sample.txt")
    print("File moved")
else:
    print("sample.txt does not exist")

print("-" * 40)

# Example 2: Move and rename file
print("Example 2: Move and rename file")
if os.path.exists("destination/sample.txt"):
    shutil.move("destination/sample.txt", "destination/new_name.txt")
    print("File moved and renamed")
else:
    print("File does not exist")

print("-" * 40)

# Example 3: Move file back
print("Example 3: Move file back")
if os.path.exists("destination/new_name.txt"):
    shutil.move("destination/new_name.txt", "sample_returned.txt")
    print("File moved back")
else:
    print("File does not exist")

print("-" * 40)

# Example 4: Move multiple files
print("Example 4: Move multiple files")
os.makedirs("backup", exist_ok=True)
files = ["file1.txt", "file2.txt"]
for file in files:
    if os.path.exists(file):
        shutil.move(file, f"backup/{file}")
        print(f"{file} moved")
    else:
        print(f"{file} not found")

print("-" * 40)

# Example 5: Move only if destination does not exist
print("Example 5: Safe move")
source = "test.txt"
destination = "backup/test.txt"

if os.path.exists(source):
    if not os.path.exists(destination):
        shutil.move(source, destination)
        print("File moved safely")
    else:
        print("Destination file already exists")
else:
    print("Source file not found")