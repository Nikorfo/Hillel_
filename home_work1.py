
numbers = input("Введіть список цілих чисел через пробіл: ")
list = list(map(int, numbers.split()))
max_value = max(list)
max_index = list.index(max_value)
print(max_value, max_index)