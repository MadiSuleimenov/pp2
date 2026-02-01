#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue
    print(x)
#2 
for i in range(1, 7):
    if i % 2 == 0:
        continue
    print("san:", i)

#3
x = ["a", "", "b", "", "c"]
for i in x:
    if x == "":
        continue
    print(x)
#4
sandar = [1, -2, 3, -4, 5]
for n in sandar:
    if n < 0:
        continue
    print("non-negative:", n)
    