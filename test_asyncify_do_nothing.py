import pytest
from asyncify import asyncify, AWeight

from asyncify import property_async


@pytest.mark.asyncio
async def test_do_nothing():
    try:
        @asyncify
        async def add(a, b):
            return a + b
        raise AssertionError("Should have raised error that it was already async")
    except ValueError as ve:
        print(ve)



# @pytest.mark.asyncio
# async def test_do_nothing2():
#     @AWeight
#     def add(a, b):
#         return a + b
#
#     assert add(1, 5) == 6
#     print(add)
#     val = await add(1, 5)
#     assert val == 6
