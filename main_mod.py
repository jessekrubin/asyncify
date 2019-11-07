import asyncio
from asyncify import asyncify
import classy
import pytest
print(dir(classy))
asyncify(classy)

print(dir(classy))
print(dir(classy.KitchenSink))
print(dir(classy.KitchenSink))
