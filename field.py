from pico2d import load_image, draw_rectangle, load_font


class Field:
    def __init__(self):
        self.image = load_image('./resource/field.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.left_score=0
        self.right_score=0

    def draw(self):
        self.image.clip_draw(0, 0, 512, 240, 1200 // 2, 800 // 2, 1200, 800)
        self.font.draw(430, 730, f'{self.left_score}', (255, 255, 255))
        self.font.draw(730, 730, f'{self.right_score}', (255, 255, 255))
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 0 + 100, 0 + 50, 1200 - 100, 800 - 100

    def handle_collision(self, group, other):
        if group == 'user:field':
            pass
        if group == 'puck:field':
            pass
