# write_files.py
# 5 examples of writing files in Python

# Example 1: Write text to a file (overwrites existing content)
print("Example 1: Write text to a file")
with open("write_example.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!\n")

print("Done")
print("-" * 40)

# Example 2: Write multiple lines
print("Example 2: Write multiple lines")
lines = ["Apple\n", "Banana\n", "Cherry\n"]
with open("write_example.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Done")
print("-" * 40)

# Example 3: Append text to a file
print("Example 3: Append text to a file")
with open("write_example.txt", "a", encoding="utf-8") as f:
    f.write("This line was appended.\n")

print("Done")
print("-" * 40)

# Example 4: Write numbers as strings
print("Example 4: Write numbers as strings")
numbers = [1, 2, 3, 4, 5]
with open("numbers.txt", "w", encoding="utf-8") as f:
    for num in numbers:
        f.write(str(num) + "\n")

print("Done")
print("-" * 40)

# Example 5: Ask user for input and save it
print("Example 5: Save user input")
user_text = input("Enter some text: ")
with open("user_input.txt", "w", encoding="utf-8") as f:
    f.write(user_text)

print("Saved successfully")