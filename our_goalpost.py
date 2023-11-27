from pico2d import load_image, draw_rectangle, load_font


class Our_Goalpost:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 40)
        self.left_score = 0
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.font.draw(430, 730, f'{self.left_score}', (255, 255, 255))

    def left_score_up(self):
        self.left_score += 1

    def update(self):
        pass

    def get_bb(self):
        return 160, 300, 160 + 40, 300 + 170

    def handle_collision(self, group, other):
        pass
