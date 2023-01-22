# Python Overload
 Introducing Overload into Python.
 
# Usage
To overload a function, simply deocorate it.
Annotations must be of a Type.

```py
@overload
def f(a: list, b:str):
    return a, b

@overload
def f(a: int, b:int):
    return a + b

@overload
def f(a: list, b:tuple):
    return {b: a}

@overload
def f(a: list, b:tuple, c:int):
    return {b: a, c:a}
```
```py
f([1], "2") # -> ([1], '2')

f(1, 2) # -> 3

f([1], (2,)) # -> {(2,): [1]}

f("1", "2") # -> 
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In [3], line 1
----> 1 f("1", "2")

Cell In [1], line 30, in overload.<locals>.fork(*args, **kwargs)
     28         check[h] = len(d.keys() - (argcheck | kwargcheck).keys())
     29 if not check:
---> 30     raise NameError(
     31         f"name '{f.__name__}({', '.join([type(i).__name__ for i in args]+[':'.join([i, type(j).__name__]) for i, j in kwargs.items()])})' is not defined"
     32     )
     33 g = min(check, key=check.get)
     34 return g(*args, **kwargs)

NameError: name 'f(str, str)' is not defined
```
```py
class MyClass:
    @overload
    def __init__(self, a:str, b:int):
        self.ab = (a, b)
        
    @overload
    def __init__(self, a:int|float, b:int):
        self.ab = a + b
```
```py
MyClass("a", 1).ab # -> ("a", 1)
MyClass(1, 2).ab # -> 3
MyClass(1., 2).ab # -> 3.0
```
