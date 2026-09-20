
def shout(func):
    def wrapper(*args , **kwargs):
        result = func(*args , **kwargs)
        return result.upper()
    return wrapper


def positive_only(func):
    def wrapper(*args , **kwargs):
        for arg in args :
            if isinstance(arg , bool) or not isinstance(arg , (int , float)) or arg <= 0:
                raise ValueError( f"Аргумент {arg} має бути додатнім")
        return func(*args , **kwargs)
    return wrapper     


@positive_only
def add_two(x):
    return x + 2

@shout
def add_suffix(value):
    return value + "suffix"

# --> add_suffix("i")
# --> "ISUFFIX"
if __name__ == "__main__":
    print(add_suffix("i"))
    print(add_two(3))
 
    try:
        add_two(-1)
    except ValueError as e:
        print(f"Помилка: {e}")