from pico2d import load_image, draw_rectangle


class Field:
    def __init__(self):
        self.image = load_image('resource/field.png')

    def draw(self):
        self.image.clip_draw(0, 0, 512, 240, 1200 // 2, 800 // 2, 1200, 800)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 0 + 100, 0 + 50, 1200 - 100, 800 - 100

    def handle_collision(self, group, other):
        if group == 'user:field':
            pass
