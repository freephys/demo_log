def foo():
    pass
def bar():
    foo()
    time.sleep(1)
    return 0
#def error():
#    1/0
def recur(i):
    if i == 0:
        return
    recur(i-1)
@stack_trace(with_return=True, with_exception=True, max_depth=1)
def test():
    bar()
    recur(5)
#    error()
test()
