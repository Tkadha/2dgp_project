objects = [[],[],[]]
# layer 0: 배경
# layer 1: 캐릭터, 볼
# later 2: 골대

def add_object(o,depth):
    objects[depth].append(o)

def add_objects(ol,depth):
    objects[depth] +=ol

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    return ValueError('Cannot delete object')

def update():
    for layer in objects:
        for o in layer:
            o.update()
def render():
    for layer in objects:
        for o in layer:
            o.draw()

