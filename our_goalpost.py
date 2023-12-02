from pico2d import load_image, draw_rectangle, load_font


class Our_Goalpost:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 40)
        self.left_score = 0
        self.x=160
        self.y=300
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.font.draw(430, 730, f'{self.left_score}', (255, 255, 255))

    def left_score_up(self):
        self.left_score += 1

    def update(self):
        pass

    def get_bb(self):
        return self.x, self.y, self.x + 40, self.y + 170

    def handle_collision(self, group, other):
        pass
