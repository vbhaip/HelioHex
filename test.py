def decorator(foo):
    def magic(*args, **kwargs):
        print("decorated!")
        print(kwargs['repeat'])
        foo(*args, **kwargs)
        #return foo
    return magic

@decorator
def basic(val, val2, repeat=False):
    print(val)

basic(1,2, repeat=False)
