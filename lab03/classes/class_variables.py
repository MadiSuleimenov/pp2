# 1) Shared class variable
class Person:
    species = "Human"

p1 = Person()
p2 = Person()
print(p1.species, p2.species)

# 2) Changing a class variable through a class
Person.species = "Homo sapiens"
print(p1.species)

# 3) Instance variable does not affect the class
p1.species = "Robot"
print("p1:", p1.species)
print("p2:", p2.species)
print("class:", Person.species)

# 4) Counter of created objects
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1

a = Counter(); b = Counter()
print(Counter.count)

# 5) Using a class variable in a method
class Shop:
    tax = 0.12
    def price_with_tax(self, price):
        return price * (1 + Shop.tax)

s = Shop()
print(s.price_with_tax(100))
