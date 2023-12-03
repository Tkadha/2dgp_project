from pico2d import load_image, draw_rectangle, load_font


class Enemy_Goalpost:
    score = 0
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 40)
        Enemy_Goalpost.score = 0
        pass

    def draw(self):
        self.font.draw(730, 730, f'{Enemy_Goalpost.score}', (255, 255, 255))

    def right_score_up(self):
        Enemy_Goalpost.score += 1

    def update(self):
        pass

    def get_bb(self):
        return 995, 300, 985 + 50, 300 + 170

    def handle_collision(self, group, other):
        if group == 'puck:post':
            left_post, bottom_post, right_post, top_post = self.get_bb()
            if other.x - other.bounding_box_size <= left_post:
                self.right_score_up()
        pass
