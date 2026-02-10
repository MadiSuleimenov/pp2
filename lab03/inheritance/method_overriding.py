# 1
class Animal:
    def sound(self):
        print("...")

class Dog(Animal):
    def sound(self):
        print("Woof")

Dog().sound()

# 2
class Bird(Animal):
    def sound(self):
        super().sound()
        print("Chirp")

Bird().sound()

# 3
a = Animal()
d = Dog()
a.sound()
d.sound()

# 4
class Cow(Animal):
    def sound(self):
        print("Moo")

for x in [Dog(), Cow(), Bird()]:
    x.sound()

# 5
class Person:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Person(name={self.name})"

print(Person("Madi"))
