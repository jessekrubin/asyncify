import asyncio

import pytest

import things
from asyncify import asyncify

print(dir(things))
asyncify(things)

print(dir(things))


def fsync(a, b):
    r = a + b
    return r


fasync = asyncify(fsync)


@pytest.mark.asyncio
async def test_asyncify_module():
    rasync = await things.add_async(1, 2)
    rsync = things.add(1, 2)
    assert rsync == rasync


@pytest.mark.asyncio
async def test_asyncify_function():
    rsync = fsync(1, 4)
    rasync = await fasync(1, 4)
    assert rsync == rasync
