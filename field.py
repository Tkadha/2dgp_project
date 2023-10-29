from pico2d import load_image


class Field:
    def __init__(self):
        self.image = load_image('field.png')

    def draw(self):
        self.image.clip_draw(0, 0, 512, 240, 400, 300, 800, 600)

    def update(self):
        pass