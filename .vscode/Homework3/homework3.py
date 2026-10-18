

def a():
   info = input("Введіть дані: ") 
   return info

def b(info):
    parts = info.split()

    if len(parts) != 12:
        print("Помилка: потрібно ввести 12 чисел")
        exit()

    for part in parts:
        try:
            float(part)
        except ValueError:
            print(f"Помилка: '{part}' не є числом")
            exit()

def c(info):
    parts = info.split()
    values = [float(x) for x in parts]

    months = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
    total = sum(values)
    average = total / 12

    max_value = max(values)
    min_value = min(values)
    max_month = months[values.index(max_value)]
    min_month = months[values.index(min_value)]

    result = (total, average, (max_value, max_month), (min_value, min_month))
    return result

def d(result):

    print(result)



def main():
    info = a()
    b(info)
    result = c(info)
    d(result)

main()