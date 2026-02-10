# 1
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Madi", 17)

print(p1.name)
print(p1.age)
# 2
class Person:
  pass

p1 = Person()
p1.name = "Madi"
p1.age = 25

print(p1.name)
print(p1.age)
# 3
class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country

p1 = Person("Linus", 30, "Oslo", "Norway")

print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)

# 4
class Student:
    def __init__(self, grade):
        self.grade = grade

print(Student(11).grade)

# 5
class Box:
    def __init__(self, size):
        self.size = size

print(Box(10).size)
