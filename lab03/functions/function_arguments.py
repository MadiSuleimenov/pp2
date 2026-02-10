#Single argument
def my_function(fname):
    print(fname)

my_function("Ali")

#Two arguments
def my_function(fname, lname):
    print(fname + " " + lname)

my_function("Ali", "Khan")

#Keyword arguments
def my_function(child3, child2, child1):
    print(child3)

my_function(child1="Emil", child2="Tobias", child3="Linus")

#Default parameter value
def my_function(country="Norway"):
    print(country)

my_function()
my_function("Sweden")

#Arbitrary arguments (*args)
def my_function(*kids):
    print(kids[2])

my_function("Emil", "Tobias", "Linus")
