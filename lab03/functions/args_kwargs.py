#*args
def my_function(*kids):
    print(kids[0])

my_function("Ernar", "Nurkadam", "Nuradil")

#*args with numbers
def my_function(*numbers):
    print(sum(numbers))

my_function(1, 2, 3)

#**kwargs
def my_function(**kid):
    print(kid["fname"])

my_function(fname="Tobias", lname="Refsnes")

#**kwargs as dictionary
def my_function(**data):
    print(data)

my_function(name="Golym", age=17)

#Normal + *args
def my_function(a, b, *args):
    print(a, b, args)

my_function(1, 2, 3, 4)
