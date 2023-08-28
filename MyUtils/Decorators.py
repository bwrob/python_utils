from time import perf_counter
from functools import wraps

FUNCTIONS = dict()
DEFAULT_VALUE_DEBUG_MODE = True
DEFAULT_VALUE_PRINT_VALUE = False
DEFAULT_VALUE_TIMER = True


def time(func):
    """
    Print the runtime of the decorated function
    """
    @wraps(func)
    def handler(*args, **kwargs):
        start_time = perf_counter()
        output = func(*args, **kwargs)
        end_time = perf_counter()
        duration = end_time - start_time
        print(f"\nRuntime of {func.__name__!r} was {duration} seconds.")
        return output
    return handler


def debugging(debug_mode, print_call_output, timer):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if print_call_output:
                args_repr = [repr(a) for a in args]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                print(f"Calling {func.__name__}({signature})")
            if timer:
                tic = perf_counter()
            # actual function call
            result = func(debug_mode, *args, **kwargs)
            if timer:
                toc = perf_counter()
                print("{} evaluated in {} seconds".format(func.__name__, toc - tic))
            if print_call_output:
                print(f"{func.__name__!r} returned {result!r}")
            return result
        return wrapped
    return wrapper


def debug(debug_mode=DEFAULT_VALUE_DEBUG_MODE,
          print_value=DEFAULT_VALUE_PRINT_VALUE,
          timer=DEFAULT_VALUE_TIMER,
          ):
    """
    Decorator. If no debuging flags are enabled, just return the function.
    """
    if any(control := (debug_mode, print_value, timer)):
        return debugging(*control)
    else:
        return lambda x: x


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
