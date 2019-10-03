import asyncio

from asyncify import asyncify


@asyncify
def f(a, b):
    r = a + b
    print(r)
    return r



asyncio.run(f(1, 4))
