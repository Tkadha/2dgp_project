from pico2d import load_image, draw_rectangle, load_font


class Our_Goalpost:
    score = 0
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 40)
        self.x=160
        self.y=300
        Our_Goalpost.score = 0
        pass

    def draw(self):
        self.font.draw(430, 730, f'{Our_Goalpost.score}', (255, 255, 255))

    def left_score_up(self):
        Our_Goalpost.score += 1

    def update(self):
        pass

    def get_bb(self):
        return self.x, self.y, self.x + 40, self.y + 170

    def handle_collision(self, group, other):
        if group == 'puck:post':
            left_post, bottom_post, right_post, top_post = self.get_bb()
            if other.x + other.bounding_box_size >= right_post:
                self.left_score_up()
                print(f'{Our_Goalpost.score}')
            pass
