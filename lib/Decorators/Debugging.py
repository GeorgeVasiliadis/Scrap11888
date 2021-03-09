import time

def timeMe(func):
    def time_wrapper(*args, **kwargs):
        t1 = time.time()
        ret = func(*args, **kwargs)
        t2 = time.time()
        print(f"Total Time of {func.__name__}() --> {(t2-t1):.3f}s")
        return ret
    return time_wrapper
