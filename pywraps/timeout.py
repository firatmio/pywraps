import asyncio
import functools
import signal
import threading
from typing import Callable, Any


class TimeoutError(Exception):
    pass


def timeout(seconds: float):
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                try:
                    return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
                except asyncio.TimeoutError:
                    raise TimeoutError(f"Function '{func.__name__}' timed out after {seconds} seconds")
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                result = [None]
                exception = [None]
                
                def target():
                    try:
                        result[0] = func(*args, **kwargs)
                    except Exception as e:
                        exception[0] = e
                
                thread = threading.Thread(target=target)
                thread.daemon = True
                thread.start()
                thread.join(seconds)
                
                if thread.is_alive():
                    raise TimeoutError(f"Function '{func.__name__}' timed out after {seconds} seconds")
                
                if exception[0]:
                    raise exception[0]
                
                return result[0]
            return sync_wrapper
    return decorator
