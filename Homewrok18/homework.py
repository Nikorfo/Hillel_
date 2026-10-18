import logging


logger =logging.getLogger("homework")
logger.setLevel(logging.DEBUG)


console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s: [%(levelname)s] -- %(message)s"))


file = logging.FileHandler("homework.log", encoding="utf-8")
file.setLevel(logging.DEBUG)
file.setFormatter(logging.Formatter("%(asctime)s: [%(levelname)s] [%(funcName)s - %(lineno)d]: %(message)s"))


logger.addHandler(console)
logger.addHandler(file)


def divide(a ,b ):
    logger.debug("divide called with a=%s , b=%s" , a, b )

    try:
        result = a / b

    except ZeroDivisionError:
        logger.error("Division by zero: a=%s , b=%s", a, b)
        return None
    
    logger.info("%s / %s = %s" , a , b, result)
    return result


divide(10,2)
divide(10,0)
