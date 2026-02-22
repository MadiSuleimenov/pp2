nums = [10, 20, 30]
it = iter(nums)
print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30

class MyNumbers:
    def __iter__(self):
        self.n = 1
        return self

    def __next__(self):
        x = self.n
        self.n += 1
        return x

obj = MyNumbers()
it = iter(obj)
print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3

def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(5):
    print(x, end=" ")  # 5 4 3 2 1
print()

def gen_a():
    yield 1
    yield 2

def gen_b():
    yield 100
    yield from gen_a()
    yield 200

print(list(gen_b()))  # [100, 1, 2, 200]