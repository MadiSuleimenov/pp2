# 1) two parents, both methods available
class A:
    def a(self): print("A")

class B:
    def b(self): print("B")

class C(A, B):
    pass

c = C()
c.a(); c.b()

# 2) If the methods are the same, the order (MRO) decides
class A1:
    def show(self): print("A1")

class B1:
    def show(self): print("B1")

class C1(A1, B1):
    pass

C1().show()  # возьмёт из A1

# 3)View MRO
print(C1.mro())

# 4) Multiple inheritance + super() 
class Base:
    def run(self):
        print("Base")

class Left(Base):
    def run(self):
        super().run()
        print("Left")

class Right(Base):
    def run(self):
        super().run()
        print("Right")

class Mix(Left, Right):
    def run(self):
        super().run()
        print("Mix")

Mix().run()

# 5) Mixin-style (adding functionality)
class PrintableMixin:
    def print_me(self):
        print(self.__dict__)

class User(PrintableMixin):
    def __init__(self, name):
        self.name = name

User("Madi").print_me()
