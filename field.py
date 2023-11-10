from pico2d import load_image


class Field:
    def __init__(self):
        self.image = load_image('resource/field.png')

    def draw(self):
        self.image.clip_draw(0, 0, 512, 240, 1200 // 2, 800 // 2, 1200, 800)

    def update(self):
        pass