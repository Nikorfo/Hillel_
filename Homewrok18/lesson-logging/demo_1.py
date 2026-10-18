# class Order:
#     def __init__(self, order_id, items):
#         self.order_id = order_id
#         self.items = items

#     def __str__(self):
#         return f"ID={self.order_id} with {self.items}"

# my_order = Order(11111111, [1, 2, 3])

# print(my_order)

#-------------------------------------------------------------------

# import logging

# logging.debug("DEBUG")
# logging.info("INFO")
# logging.warning("WARN")
# logging.error("ERROR")
# logging.critical("CRITICAL")


#-------------------------------------------------------------------

# import logging

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s: [%(levelname)s] %(funcName)s: %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )

# logging.debug("This is a debug message...")

#-------------------------------------------------------------------


import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("shop")

logger.setLevel( logging.DEBUG )

# --- console
console = logging.StreamHandler()
console.setLevel( logging.ERROR )

console_formatter = logging.Formatter("%(asctime)s: [%(levelname)s] -- %(message)s")

console.setFormatter( console_formatter )

# --- file
file = logging.FileHandler("shop.log", encoding="utf-8")

file.setLevel( logging.DEBUG )

file_formatter = logging.Formatter("%(asctime)s: [%(levelname)s] [%(funcName)s - %(lineno)d]: %(message)s")

file.setFormatter(file_formatter)

# --- rotation
rotation = RotatingFileHandler("rotating.log", maxBytes=500, backupCount=3, encoding="utf-8")

rotation.setFormatter(file_formatter)
# --

logger.addHandler(console)
logger.addHandler(file)
logger.addHandler(rotation)

# FORMATTER (формує формат повідомлення) --> HANDLER (кудись те повідомлення діти) -> logger ( керує логуванням )


def do_something( arg1, arg2 ):

    logger = logging.getLogger("shop")

    logger.debug("ARGS = %d + %d", arg1, arg2)

    result = arg1 + arg2

    logger.debug(f"RESULT = {result}")

    if result < 0:
        logger.error("Not enough money...")

    return result

do_something(1, 2)
do_something(4, 55)
do_something(1, -4)
do_something(11, 2)
