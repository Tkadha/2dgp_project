from pico2d import load_image, draw_rectangle, load_music


class Field:
    bgm = None

    def __init__(self):
        self.image = load_image('./resource/field.png')
        Field.bgm = load_music('./sound/background.mp3')
        Field.bgm.set_volume(32)
        Field.bgm.repeat_play()

    def draw(self):
        self.image.clip_draw(0, 0, 512, 240, 1200 // 2, 800 // 2, 1200, 800)

    def update(self):
        pass

    def get_bb(self):
        return 0 + 100, 0 + 50, 1200 - 100, 800 - 100

    def handle_collision(self, group, other):
        if group == 'user:field':
            pass
        if group == 'puck:field':
            pass
