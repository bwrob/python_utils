from time import perf_counter
from functools import wraps


FUNCTIONS = dict()


def time(func):
    """
    Print the runtime of the decorated function
    """
    @wraps(func)
    def handler(*args, **kwargs):
        start_time = perf_counter()
        output = func(*args, **kwargs)
        end_time = perf_counter()
        duration = end_time-start_time
        print(f"\nRuntime of {func.__name__!r} was {duration} seconds.")
        return output
    return handler


def debug_decorator(func):
    """
    Print the function signature and return value
    """
    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper_debug


def dummy_decorator(func):
    """
    Do-nothing decorator
    """
    return func


def debug(is_debug):
    """
    Print info about call/output
    """
    if is_debug:
        return debug_decorator
    else:
        return dummy_decorator


def register(func):
    """
    Register a function as available to use
    """
    FUNCTIONS[func.__name__] = func
    return func


def memo(func):
    """
    Keep a cache of previous function calls (memoization)
    This is just mock up better use @functools.lru_cache(maxsize=)
    """
    @wraps(func)
    def wrapper_memoize(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in wrapper_memoize.cache:
            wrapper_memoize.cache[cache_key] = func(*args, **kwargs)
        return wrapper_memoize.cache[cache_key]
    wrapper_memoize.cache = dict()
    return wrapper_memoize
