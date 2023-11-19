from pico2d import load_image, draw_rectangle


class Our_Goalpost:
    def __init__(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 160, 300, 160 + 40, 300 + 170

    def handle_collision(self, group, other):
        pass
