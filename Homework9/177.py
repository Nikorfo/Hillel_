

for _ in range(2):
    n = int(input())
    s = str(n).zfill(4)
    print(len(set(s)) == 4)

