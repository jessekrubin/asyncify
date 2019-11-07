# -*- coding: utf-8 -*-
"""Asyncify your code

...or else...
"""
from asyncio import coroutine
from asyncio import get_event_loop
from functools import partial
from functools import wraps
from inspect import ismodule, getmembers, isfunction, isclass, ismethod
from typing import Any
from typing import Callable
from typing import TypeVar
from typing import cast
FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def asyncify(funk: F, functions=True, classes = True) -> F:
    """

    :param funk:
    :return:
    """

    @coroutine
    @wraps(funk)
    def afunk(*args, loop=None, executor=None, **kwargs):
        """

        :param args:
        :param loop:
        :param executor:
        :param kwargs:
        :return:
        """
        loop = loop if loop else get_event_loop()
        pfunc = partial(funk, *args, **kwargs)
        return loop.run_in_executor(executor, pfunc)
    print(funk)
    if ismodule(funk):
        for fname, f in getmembers(funk, isfunction):
            setattr(funk, '{}_async'.format(fname), asyncify(f))
        for fname, f in getmembers(funk, isclass):
            setattr(funk, '{}_async'.format(fname), asyncify(f))
    elif isclass(funk):
        print(funk)
        for a, b in funk.__dict__.items():
            print(a, b)
        print(getmembers(funk, predicate=ismethod))
        # print(getmembers(funk))
        members = [el for el in getmembers(funk) if not el[0].startswith('__') and not el[0].endswith('__')]
        print(members)

        for mem in members:
            setattr(funk, '{}_async'.format(mem[0]), asyncify(mem[-1]))
        members = [el for el in getmembers(funk) if not el[0].startswith('__') and not el[0].endswith('__')]

        print(members)

        # setattr(funk, '{}_async'.format(fname), asyncify(f))
    else:
        return cast(F, afunk)


a = asyncify
aio = asyncify
