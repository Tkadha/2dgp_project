from pico2d import load_image

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
IDLE_FRAMES_PER_ACTION = 2
RUN_FRAMES_PER_ACTION = 4

RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_PPS = (((RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)


class Ai:
    image = None

    def load_image(self, image):
        if Ai.image is None:
            if image == 'black':
                self.image = load_image('./resource/black_hockey.png')
            elif image == 'yellow':
                self.image = load_image('./resource/yellow_hockey.png')
            elif image == 'red':
                self.image = load_image('./resource/red_hockey.png')

    def __init__(self, x=None, y=None, image=None):
        self.x, self.y = x, y
        self.frame = 0
        self.action = 3
        self.dir = 1
        self.face_dir = 1
        self.size = 75
        self.load_image(image)

    def update(self):
        self.frame = (self.frame + IDLE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % IDLE_FRAMES_PER_ACTION
        pass

    def draw(self):
        if self.dir == 0:
            self.image.clip_draw(int(self.frame) * 35, self.action * 40, 35, 40, self.x, self.y, self.size, self.size)
        elif self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 35, self.action * 40, 35, 40, 0, 'h', self.x, self.y,
                                           self.size, self.size)
        pass
