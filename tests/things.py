from os import listdir


def save_string(filepath, string):
    with open(filepath, 'w') as f:
        f.write(string)

def add(x, y):
    return x + y
