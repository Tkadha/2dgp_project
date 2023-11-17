from pico2d import *
import game_world
import game_framework


class Puck:
    image = None

    def __init__(self):
        if Puck.image == None:
            Puck.image = load_image('./resource/hockeypuck.png')
        self.x = 600
        self.y = 375
        self.x_velocity = 3
        self.y_velocity = 5
        self.size = 25
        self.bounding_box_size = self.size / 2

    def draw(self):
        self.image.clip_draw(0, 0, 100, 75, self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.x_velocity * 100 * game_framework.frame_time
        self.y += self.y_velocity * 100 * game_framework.frame_time
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

    # fill here
    def get_bb(self):
        return self.x - self.bounding_box_size, self.y - self.bounding_box_size, self.x + self.bounding_box_size, self.y + self.bounding_box_size

    def handle_collision(self, group, other):
        if group == 'user:puck':
            if other.dir == 0:
                self.x = other.x + self.size
                self.y = other.y - self.size
                pass
            elif other.dir == 1:
                self.x = other.x - self.size
                self.y = other.y - self.size
                pass
        if group == 'puck:field':
            if self.x - self.bounding_box_size <= 100:
                self.x_velocity *= -1
            elif self.x + self.bounding_box_size >= 1100:
                self.x_velocity *= -1
            if self.y - self.bounding_box_size <= 50:
                self.y_velocity *= -1
            elif self.y + self.bounding_box_size>= 700:
                self.y_velocity *= -1
            pass

