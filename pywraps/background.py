import functools
import threading
from typing import Callable


def background(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> None:
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return wrapper
