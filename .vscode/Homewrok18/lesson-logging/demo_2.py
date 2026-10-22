# pip install loguru
import sys

from loguru import logger

# logger.remove()

# logger.add( sys.stderr, level="INFO", format="{time:HH:mm:ss} [{level:<8}] -- {message}" )

# logger.info("TEST")


@logger.catch
def do_something( a, b ):
    return a / b

do_something(1, 0)
