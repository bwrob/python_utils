from time import perf_counter
from functools import wraps, partial


DEFAULT_VALUE_DEBUG_MODE = True
DEFAULT_VALUE_PRINT_VALUE = False
DEFAULT_VALUE_TIMER = True


def debugging(debug_mode, print_call_output, timer):
    """
    :param debug_mode: flag to gather debugging info during computation
    :param print_call_output: flag to print call and output info for the wrapped function
    :param timer: flag to time the execution time
    :return: decorated function
    """
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
          print_call_output=DEFAULT_VALUE_PRINT_VALUE,
          timer=DEFAULT_VALUE_TIMER,
          ):
    """
    Decorator for debugging purposes.
    If no debugging flags are enabled, just return the function.
    :param debug_mode: flag to gather debugging info during computation
    :param print_call_output: flag to print call and output info for the wrapped function
    :param timer: flag to time the execution time
    :return: decorated function
    """
    if any(control := (debug_mode, print_call_output, timer)):
        return debugging(*control)
    else:
        return lambda x: partial(x, debug=False)
