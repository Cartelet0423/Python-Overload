def overload(f):
    from inspect import signature, _empty

    if overload.__dict__.get("funcs") is None:
        overload.__dict__.update({"funcs": {}})
    annotations = tuple([(i, j.annotation) for i, j in signature(f).parameters.items()])
    if overload.funcs.get(f.__qualname__):
        overload.funcs[f.__qualname__].update({annotations: f})
    else:
        overload.funcs.update({f.__qualname__: {annotations: f}})

    def fork(*args, **kwargs):
        check = {}
        for anno, h in overload.funcs[f.__qualname__].items():
            d = dict(anno)
            if len(anno) < len(args) + len(kwargs):
                continue
            argcheck = {
                name: typ == _empty or isinstance(i, typ)
                for (name, typ), i in zip(anno, args)
            }
            kwargcheck = {
                name: d[name] == _empty or isinstance(i, d[name])
                for name, i in kwargs.items()
            }
            if all((argcheck | kwargcheck).values()):
                check[h] = len(d.keys() - (argcheck | kwargcheck).keys())
        if not check:
            raise NameError(
                f"name '{f.__qualname__}({', '.join([type(i).__name__ for i in args]+[':'.join([i, type(j).__name__]) for i, j in kwargs.items()])})' is not defined"
            )
        g = min(check, key=check.get)
        return g(*args, **kwargs)

    return fork
