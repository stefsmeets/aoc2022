import time

def timeit(func):

    def wrapper(*args, **kw):

        t0 = time.time()
        result = func(*args, **kw)
        t1 = time.time()

        print(f'> {func.__name__} took: {t1-t0:.3f} s, result: {result}')

        return result

    return wrapper


def download():
    pass

def submit():
    pass