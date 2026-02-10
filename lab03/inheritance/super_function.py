# 1) super() in __init__
class A:
    def __init__(self, x):
        self.x = x

class B(A):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y

b = B(1, 2)
print(b.x, b.y)

# 2) super() methods
class Parent:
    def greet(self):
        print("Hello from Parent")

class Child(Parent):
    def greet(self):
        super().greet()
        print("Hello from Child")

Child().greet()

# 3) expand behavior

class Logger:
    def log(self, msg):
        print("LOG:", msg)

class App(Logger):
    def log(self, msg):
        super().log(msg)
        print("Saved!")

App().log("Start")

# 4) super() in the class chain
class X:
    def show(self):
        print("X")

class Y(X):
    def show(self):
        super().show()
        print("Y")

class Z(Y):
    def show(self):
        super().show()
        print("Z")

Z().show()

# 5) super() and code reuse
class Shape:
    def __init__(self, color="black"):
        self.color = color

class Circle(Shape):
    def __init__(self, r, color="black"):
        super().__init__(color)
        self.r = r

c = Circle(5, "red")
print(c.r, c.color)
