# copy_delete_files.py
# 5 examples of copying and deleting files in Python

import os
import shutil

# Example 1: Copy a file
print("Example 1: Copy a file")
shutil.copy("sample.txt", "sample_copy.txt")
print("File copied")
print("-" * 40)

# Example 2: Copy file with metadata
print("Example 2: Copy file with metadata")
shutil.copy2("sample.txt", "sample_copy2.txt")
print("File copied with metadata")
print("-" * 40)

# Example 3: Delete a file
print("Example 3: Delete a file")
if os.path.exists("old_file.txt"):
    os.remove("old_file.txt")
    print("File deleted")
else:
    print("File does not exist")
print("-" * 40)

# Example 4: Rename a file
print("Example 4: Rename a file")
if os.path.exists("sample_copy.txt"):
    os.rename("sample_copy.txt", "renamed_sample.txt")
    print("File renamed")
else:
    print("Source file does not exist")
print("-" * 40)

# Example 5: Check before deleting
print("Example 5: Safe delete")
filename = "temporary.txt"
if os.path.isfile(filename):
    os.remove(filename)
    print(f"{filename} deleted")
else:
    print(f"{filename} not found")