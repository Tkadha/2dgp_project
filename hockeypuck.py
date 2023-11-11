from pico2d import *
import game_world
import game_framework

class Puck:
    image = None

    def __init__(self):
        if Puck.image == None:
            Puck.image = load_image('resource/hockeypuck.png')
        self.x = 600
        self.y = 375
        self.x_velocity = 0
        self.y_velocity = 0
        self.size = 25
        self.bounding_box_size = self.size / 2

    def draw(self):
        self.image.clip_draw(0, 0, 100, 75, self.x, self.y, self.size,self.size)
        draw_rectangle(*self.get_char_bb())

    def update(self):
        self.x += self.x_velocity * 100 * game_framework.frame_time
        self.y += self.y_velocity * 100 * game_framework.frame_time
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

    # fill here
    def get_char_bb(self):
        return self.x - self.bounding_box_size, self.y - self.bounding_box_size, self.x + self.bounding_box_size, self.y + self.bounding_box_size