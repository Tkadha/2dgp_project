from pico2d import load_image, draw_rectangle, load_font


class Enemy_Goalpost:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 40)
        self.right_score = 0
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.font.draw(730, 730, f'{self.right_score}', (255, 255, 255))

    def right_score_up(self):
        self.right_score += 1

    def update(self):
        pass

    def get_bb(self):
        return 995, 300, 985 + 50, 300 + 170

    def handle_collision(self, group, other):
        pass
