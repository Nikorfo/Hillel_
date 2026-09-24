from functools import wraps

def log_args (func):

    def wrapper(*args , **kwargs):
     print(f"Виклик {func.__name__} з args={args}, kwargs={kwargs}")
     return func(*args , **kwargs)
    return wrapper    

@log_args
def alotofargs(*args, **kwargs):
    return args, kwargs

def log_args(func):
   @wraps(func)
   def wrapper(*args , **kwargs):
      print(f"Виклик {func.__name__} з args={args}, kwargs={kwargs}")
      return func(*args, **kwargs)
   return wrapper 

@log_args
def alotofargs(*args, **kwargs):
   return args , kwargs

def repeat(times):
   def dekorator(func):
      @wraps(func)
      def wrapper(*args , **kwargs):
         for _ in  range(times):
            func(*args , **kwargs)
      return wrapper   
   return dekorator


@repeat(4)
def greet():
   print("IDKTG")


def print_long_words(words):
   for word in words:
      if (length := len(word)) > 4:
        print(f"{word}: {length}")

def countdown(n):
   while n >= 1:
      yield n
      n -=1
   yield "Старт!"  


if __name__ == "__main__":
    print("--- Завдання 1 ---")
    alotofargs(1, 2, 3, name="Saber")
 
    print("\n--- Завдання 2 ---")
    greet()
 
    print("\n--- Завдання 3 ---")
    words = ["кіт", "яблуко", "дім", "комп'ютер", "сон", "місяць"]
    print_long_words(words)
 
    print("\n--- Завдання 4 ---")
    for value in countdown(5):
        print(value)
   


   

      