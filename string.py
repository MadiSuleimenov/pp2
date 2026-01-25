#1
print("Hello")
print('Hello')
#2
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)
#3
a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)
#1
b = "Hello, World!"
print(b[2:5])
#2
b = "Hello, World!"
print(b[:5])
#3
b = "Hello, World!"
print(b[2:])
#4
b = "Hello, World!"
print(b[-5:-2])
#1
a = "Hello, World!"
print(a.upper())
#2
a = "Hello, World!"
print(a.lower())
#3
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"
#1
a = "Hello"
b = "World"
c = a + b
print(c)
#2
a = "Hello"
b = "World"
c = a + b
print(c)
#1
age = 36
txt = "My name is John, I am " + age
print(txt)
#2
quantity = 3
itemno = 567
price = 49.95
myorder = "I want {} pieces of item {} for {} dollars."
print(myorder.format(quantity, itemno, price))