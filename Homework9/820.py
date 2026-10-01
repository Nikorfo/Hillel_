

class Buffer:
    def __init__(self):
        self.buffer = []

    def add(self, *a):
        self.buffer += a

        while len(self.buffer) >= 5:
            print(sum(self.buffer[:5]))
            self.buffer = self.buffer[5:]

    def get_current_part(self):
        return self.buffer


buffer = Buffer()

while True:
    line = input()

    if line == "":
        break

    numbers = map(int, line.split())
    buffer.add(*numbers)

    print(buffer.get_current_part())