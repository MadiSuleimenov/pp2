#1
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()
#2
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)


myfunc()

print("Python is " + x)
#4
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)
#1
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
#2
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)


x=5 #integer 
y="John" #string
print(x)
print(y)

x=4 # x is of type int
x="Sally" # x is now of type str
print(x)


#You can get the data type of a variable with the type() function.
x = 5
y = "John"
print(type(x))
print(type(y))


x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0
