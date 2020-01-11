# -*- coding: utf-8 -*-
"""Asyncify your code

...or else...
"""
import functools
from asyncio import coroutine
from asyncio import get_event_loop
from functools import partial

from functools import wraps, update_wrapper
from inspect import getmembers
from inspect import isawaitable
from inspect import isclass
from inspect import iscoroutine
from inspect import iscoroutinefunction
from inspect import isfunction
from inspect import ismethod
from inspect import ismodule
from typing import Any
from typing import Callable
from typing import TypeVar
from typing import cast
from asyncio import iscoroutinefunction

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)

class AWeight:
    """This wraps a coroutine will call it on await."""
    __slots__ = ['_funk']

    def __init__(self, funk):
        self._funk = funk

    def __repr__(self):
        return f'<AWeight "{self._funk.__qualname__}">'

    def __await__(self):
        return self._funk().__await__()

def property_async(func, *args, **kwargs):
    try:
        assert iscoroutinefunction(func)
        return PropertyAsync(func, *args, **kwargs)
    except AssertionError:
        return PropertyAsync(_asyncify_function(func), *args, **kwargs)
    # assert iscoroutinefunction(func), 'Can only use with async def'
    # return PropertyAsync(func, *args, **kwargs)

class PropertyAsync:
    def __init__(self, _fget, field_name=None):
        self._fget = _fget
        self.field_name = field_name or _fget.__name__
        update_wrapper(self, _fget)

    def __set_name__(self, owner, name):
        self.field_name = name

    def __get__(self, instance, owner):
        # return self
        return self if instance is None else self.awaitable_only(instance)

    def __set__(self, instance, value):
        print("crap")
        # raise ValueError(INVALID_ACTION.format('set'))
        # raise ValueError(INVALID_ACTION.format('set'))

    def __delete__(self, instance):
        print("crap")
        # raise ValueError(INVALID_ACTION.format('delete'))

    def get_loader(self, instance):
        @wraps(self._fget)
        async def get_value():
            return await self._fget(instance)

        return get_value

    def awaitable_only(self, instance):
        @wraps(self._fget)
        async def get_value():
            return await self._fget(instance)

        return AWeight(
            get_value
            )

# class PropertyAsync(property):
#     pass

def _asyncify_function(funk: F):
    @coroutine
    @wraps(funk)
    def _funk_async(*args, loop=None, executor=None, **kwargs):
        """WRAPPER"""
        loop = loop if loop else get_event_loop()
        pfunc = partial(funk, *args, **kwargs)
        return loop.run_in_executor(executor, pfunc)

    return cast(F, _funk_async)

def _asyncify_class(cls: F):
    # @coroutine
    # @wraps(cls)
    # def _funk_async(*args, loop=None, executor=None, **kwargs):
    #     """WRAPPER"""
    #     loop = loop if loop else get_event_loop()
    #     pfunc = partial(funk, *args, **kwargs)
    #     return loop.run_in_executor(executor, pfunc)
    print("INCLASEE")
    print(cls, dir(cls))
    members = [
        el
        for el in getmembers(cls)
        if not el[0].startswith("__")
           and not el[0].endswith("__")
           and not el[0].endswith("_async")
        ]
    for mem in members:
        print("looking at members", mem, mem[-1])
        _async_class_func = asyncify(mem[-1])
        # setattr(funk, "{}_async".format(mem[0]), cast(F, mem[-1]))
        setattr(cls, "{}_async".format(mem[0]), _async_class_func)
        # cast(F, mem[-1]))

    members = [
        el
        for el in getmembers(cls)
        if not el[0].startswith("__") and not el[0].endswith("__")
        ]
    from pprint import pprint
    pprint(members)

    # return cast(F, _funk_async)
    # return cast(F, )
    return cls

def asyncify(funk: F, functions=True, classes=True) -> F:
    """ASYNCIFY STUFF"""

    @coroutine
    @wraps(funk)
    def afunk(*args, loop=None, executor=None, **kwargs):
        """WRAPPER"""
        loop = loop if loop else get_event_loop()
        pfunc = partial(funk, *args, **kwargs)
        return loop.run_in_executor(executor, pfunc)

    print("HERE", funk)
    if ismodule(funk):
        for fname, f in getmembers(funk, isfunction):
            setattr(funk, "{}_async".format(fname), asyncify(f))
        for fname, f in getmembers(funk, isclass):
            print(funk)
            asyncify(f)
    elif isclass(funk):
        print("IS CLASS", funk, dir(funk))
        _asyncify_class(funk)
        return funk
    elif isinstance(funk, property):
        print('_______________________')
        print("ITS A PROP", print(funk), dir(funk))
        for thing in dir(funk):
            print(thing, getattr(funk, thing))
        print("HERM we are here at a prop")
        print(funk.fget)
        newfunk = asyncify(funk.fget)
        print('this is the wrapped funk', newfunk)
        import inspect
        print(inspect.getsource(newfunk))
        return property_async(newfunk)
        # funk.getter = _asyncify_function(funk.fget)
        # setattr(funk, funk)
        # print("INCLASEE")
        # print(funk, dir(funk))
        # members = [
        #     el
        #     for el in getmembers(funk)
        #     if not el[0].startswith("__")
        #        and not el[0].endswith("__")
        #        and not el[0].endswith("_async")
        #     ]
        # for mem in members:
        #     print("looking at members", mem, mem[-1])
        #     _async_class_func = asyncify(mem[-1])
        #     # setattr(funk, "{}_async".format(mem[0]), cast(F, mem[-1]))
        #     setattr(funk, "{}_async".format(mem[0]), _async_class_func)
        #     # cast(F, mem[-1]))
        #
        # members = [
        #     el
        #     for el in getmembers(funk)
        #     if not el[0].startswith("__") and not el[0].endswith("__")
        #     ]

        # return funk
    elif (
            isfunction(funk)
            and not funk.__name__.endswith("_async")
            and not iscoroutinefunction(funk)
            # and not iscoroutine(funk)
            # and not isawaitable(funk)
    ):
        print('=================')
        print(funk, dir(funk))
        return _asyncify_function(funk)
        # return cast(F, afunk)

a = asyncify
