#1
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)
#2
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue
    print(i)

#3
numbers = [3, -1, 5, -2, 7]
i = 0
while i < len(numbers):
    if numbers[i] < 0:
        i += 1
        continue
    print(numbers[i])
    i += 1

#4
while True:
    word = input()
    if word == "stop":
        break
    if word == "skip":
        continue
    print(word)

#5
i = 0
while i < 10:
    i += 1
    if i % 3 == 0:
        continue
    print(i)
