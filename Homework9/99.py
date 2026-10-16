

k = int(input())
n = int(input())

page = (n - 1) // k + 1
line = (n - 1) % k + 1

print(page, line)