class MyClass:
    def __init__(self):
        self.some_list = []

    def append_to_list(self, val):
        self.some_list.append(val)


my_instance = MyClass()

my_instance.append_to_list("some value")
my_instance.append_to_list("another value")
my_instance.append_to_list("third value")

print(my_instance.some_list)

if 'a':
    print("a is True")

if not 0:
    print("0 is False")

if '0':
    print("'0' is True")
