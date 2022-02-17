from sqlalchemy import func


class Foo:
    a = 1


foo = Foo()
print(foo.__getattribute__("a"))
