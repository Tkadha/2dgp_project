from pico2d import load_image




class StateMachine:
    def __init__(self, enemy):
        self.enemy = enemy

    def start(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass




class User_char:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.face_dir = 1
        self.image = load_image('')

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
