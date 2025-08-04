import functools
import threading
import time
from typing import Callable, Any


def debounce(wait: float):
    def decorator(func: Callable) -> Callable:
        timer = None
        lock = threading.Lock()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            nonlocal timer
            
            def call_func():
                with lock:
                    timer = None
                func(*args, **kwargs)
            
            with lock:
                if timer:
                    timer.cancel()
                timer = threading.Timer(wait, call_func)
                timer.start()
        
        return wrapper
    return decorator
