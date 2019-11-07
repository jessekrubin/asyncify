from os import listdir

class ASink:

    def __init__(volume):
        self.volume = volume

    def get_volume(self):
        return self.volume

    def get_type(self):
        return 'ASink'

class KitchenSink(ASink):

    def get_type(self):
        return 'KitchenSink'


class BathroomSink(ASink):

    def get_type(self):
        return 'BathroomSink'

def add(a, b):
    return a + b

async def add_awaited(a, b):
    return a + b

async def add_awaitable(a, b):
    r = await add_awaited(a, b)
    return r
