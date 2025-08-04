import time
import functools
from typing import Callable, Any, Type, Union


def retry(tries: int = 3, delay: float = 1.0, exceptions: Union[Type[Exception], tuple] = Exception):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(tries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < tries - 1:
                        time.sleep(delay)
                    continue
            raise last_exception
        return wrapper
    return decorator
