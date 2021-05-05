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
        arrays = []
        id_args = []
        id_outputs = []
        for arg in args:
            if isinstance(arg, LoggedNDArray):
                arg.write_log = False
                arrays.append(arg)
                id_args.append(arg.get_id())

        result = orig_func(*args, **kwargs)
        if isinstance(result, Iterable):
            for output in result:
                if isinstance(output, LoggedNDArray):
                    id_outputs.append(output.get_id())

        if len(arrays) != 0:
            write_log(arrays[0].file, str(time.time()), orig_func.__name__, id_args, id_outputs, kwargs)
        for arg in arrays:
            arg.write_log = True
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
