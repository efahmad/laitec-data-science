def star(func):
    def my_func():
        print("*" * 100)
        print("Executing " + func.__name__)
        func()
        print("*" * 100)

    return my_func


@star
def test_decorator():
    print("In the test_decorator function")


test_decorator()
