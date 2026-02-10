# 1
class Person:
    def speak(self):
        print("Hello")

class Student(Person):
    pass

s = Student()
s.speak()
# 2
class Animal:
    def sound(self):
        print("Some sound")

class Dog(Animal):
    pass

Dog().sound()
# 3
class Parent:
    x = 10

class Child(Parent):
    pass

print(Child.x)
# 4
class Vehicle:
    def move(self):
        print("Moving")

class Car(Vehicle):
    pass

Car().move()
# 5
class A:
    pass

class B(A):
    pass

print(isinstance(B(), A))


