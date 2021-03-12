"""
Decorator functions that capture a pattern for a function
"""
from ds_clean.logged_array import *
import functools
import inspect

def basic_tracker(function):
    @functools.wraps(function)
    def funct(*args, **kwargs):
        save_ids = []
        for arg in args:
            if isinstance(arg, LoggedNDArray):
                pass
                
        outputs = function(*args, **kwargs)
        
        for output in outputs:
            if isinstance(output, LoggedNDArray):
                pass
                
        return outputs
    return funct

def logging_func(orig_func):
    @functools.wraps(orig_func)
    def decorator(*args, **kwargs):
        print("Method called: %s, id: %s" % (orig_func.__name__, id(orig_func)))
        cf = currentframe()
        while cf.f_back:
            cf = cf.f_back
            filename = getframeinfo(cf).filename
            print(" File:", filename, "at Line", cf.f_lineno, "\n Caller:", cf.f_code.co_name)
        for arg in args:
            if isinstance(arg, np.ndarray):
                print(" Numpy array id passed as argument:", id(arg), "\n Raw array:\n", arg)
        result = orig_func(*args, **kwargs)
        print("Return object id:", id(result), "type:", type(result), "raw:", result)
        return result

    return decorator


def logging_class(cls):
    for name, method in inspect.getmembers(cls):
        if (not inspect.ismethod(method) and not inspect.isfunction(method)) or inspect.isbuiltin(method):
            continue
        if inspect.ismethod(method):
            continue
        print("Decorating function %s" % name)
        setattr(cls, name, logging_func(method))
    return cls