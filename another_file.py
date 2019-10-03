
import asyncio
import things
from asyncify import asyncify
print(dir(things))
asyncify(things)

print(dir(things))

async def something():
    res = await things.add_async(1, 2)
    print(res)
    return res

asyncio.run(something())
