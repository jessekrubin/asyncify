import asyncio

import pytest

import classy
from asyncify import asyncify

print(dir(classy))
asyncify(classy)

print(dir(classy))
print(dir(classy.KitchenSink))
print(dir(classy.KitchenSink))
