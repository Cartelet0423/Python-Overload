def overload(f):
    if overload.__dict__.get("funcs") is None:
        overload.__dict__.update({"funcs": {}})
    if overload.funcs.get(f.__name__):
        overload.funcs[f.__name__].update({tuple(f.__annotations__.items()): f})
    else:
        overload.funcs.update({f.__name__: {tuple(f.__annotations__.items()): f}})

    def fork(*args, **kwargs):
        check = {}
        for anno, h in overload.funcs[f.__name__].items():
            d = dict(anno)
            if len(anno) < len(args) + len(kwargs):
                continue
            argcheck = {name: isinstance(i, typ) for (name, typ), i in zip(anno, args)}
            kwargcheck = {name: isinstance(i, d[name]) for name, i in kwargs.items()}
            if all((argcheck | kwargcheck).values()):
                check[h] = len(d.keys() - (argcheck | kwargcheck).keys())
        if not check:
            raise NameError(
                f"name '{f.__name__}({', '.join([type(i).__name__ for i in args]+[':'.join([i, type(j).__name__]) for i, j in kwargs.items()])})' is not defined"
            )
        g = min(check, key=check.get)
        return g(*args, **kwargs)

    return fork
