from pico2d import load_image, draw_rectangle


class Enemy_Goalpost:
    def __init__(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 995, 300, 985 + 50, 300 + 170

    def handle_collision(self, group, other):
        pass
