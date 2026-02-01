#1
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1
#2
i = 1
while i <= 10:
    if i == 7:
        print("Finded!")
        break
    i += 1

#3
while True:
    x = int(input())
    if x < 0:
        break
    print(x)

#4
i = 1
s = 0
while True:
    s += i
    if s > 10:
        break
    i += 1
print(s)

#5
while True:
    pwd = input("Password: ")
    if pwd == "1234":
        break
print("Access is open")
