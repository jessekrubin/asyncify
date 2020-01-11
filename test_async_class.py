import pytest
from asyncify import asyncify

from asyncify import property_async

# @asyncify
# class Rectangle2:
#     height: int
#     width: int
#
#     def __init__(self, height, width):
#         self.height = height
#         self.width = width
#
#     def area_function(self):
#         return self.height * self.width
#
#     @property
#     def area_property(self):
#         return self.height * self.width
#
#     # asyncify(Rectangle)
# @pytest.mark.asyncio
# async def test_asyncify_class2():
#
#     r = Rectangle2(3, 5)
#     print(r)
#     print(dir(r))
#     area_from_func_sync = r.area_function()
#     assert area_from_func_sync == 15
#     area_from_func_async = await r.area_function_async()
#     assert area_from_func_sync == area_from_func_async
#
#     area_from_prop = r.area_p
#     assert False
#
@pytest.mark.asyncio
async def test_asyncify_class():
    @asyncify
    class Rectangle:
        height: int
        width: int

        def __init__(self, height, width):
            self.height = height
            self.width = width

        def area_function(self):
            return self.height * self.width

        @property
        def area_property(self):
            return self.height * self.width

        @property_async
        def area_property_async_already(self):
            return self.height * self.width

        # asyncify(Rectangle)

    r = Rectangle(3, 5)
    print(r)
    print(dir(r))
    area_from_func_sync = r.area_function()
    assert area_from_func_sync == 15
    area_from_func_async = await r.area_function_async()
    assert area_from_func_sync == area_from_func_async
    assert r.area_property == 15

    _area_from_prop_async = await r.area_property_async
    assert _area_from_prop_async == 15

    _area_from_prop_async_already_there = await r.area_property_async_already
    assert _area_from_prop_async_already_there == 15

    area_from_prop = r.area_function()
    # assert False
