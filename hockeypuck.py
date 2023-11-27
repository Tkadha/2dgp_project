import random

from pico2d import *

import field
import game_world
import game_framework


class Puck:
    image = None

    def __init__(self):
        if Puck.image == None:
            Puck.image = load_image('./resource/hockeypuck.png')
        self.x = 600
        self.y = 375
        self.x_velocity = 0
        self.y_velocity = 0
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
            other.contact_puck = True
            self.x_velocity = 0
            self.y_velocity = 0
            if other.dir == 0:
                self.x = other.x + self.size
                self.y = other.y - self.size
                pass
            elif other.dir == 1:
                self.x = other.x - self.size
                self.y = other.y - self.size
            if other.shooting:
                x1, y1 = self.x, self.y
                x2, y2 = 1000, random.randint(300 + 25, 470 - 20)
                self.x_velocity = x2 - x1
                self.y_velocity = y2 - y1
                self.x_velocity /= 150
                self.y_velocity /= 150
                if self.x_velocity > 20:
                    self.x_velocity /= 4
                    self.y_velocity /= 4
                elif self.x_velocity > 10:
                    self.x_velocity /= 2
                    self.y_velocity /= 2
                elif self.x_velocity < 10:
                    self.x_velocity *= 2
                    self.y_velocity *= 2
                #     pass
                if other.dir == 0:
                    self.x += self.x_velocity * 40 * 100 * game_framework.frame_time
                    self.y += self.y_velocity * 40 * 100 * game_framework.frame_time
                else:
                    self.x += self.x_velocity * 50 * 100 * game_framework.frame_time
                    self.y += self.y_velocity * 50 * 100 * game_framework.frame_time
                other.shooting = False
                other.contact_puck = False
                print(f"{self.x_velocity, self.y_velocity}")
                pass
        if group == 'puck:field':
            if self.x - self.bounding_box_size <= 100:
                self.x = 110
                self.x_velocity *= -1
            elif self.x + self.bounding_box_size >= 1100:
                self.x = 1090
                self.x_velocity *= -1
            if self.y - self.bounding_box_size <= 50:
                self.y = 70
                self.y_velocity *= -1
            elif self.y + self.bounding_box_size >= 700:
                self.y = 680
                self.y_velocity *= -1
            pass
        if group == 'puck:post':
            left_post, bottom_post, right_post, top_post = other.get_bb()
            if left_post < 600:  # 왼쪽 골대
                if self.x - self.bounding_box_size <= left_post:
                    self.x_velocity *= -1
                elif self.x + self.bounding_box_size >= right_post:
                    other.left_score_up()
                    self.x = 600
                    self.y = 375
                    self.x_velocity = 0
                    self.y_velocity = 0
                if self.y - self.bounding_box_size <= bottom_post:
                    self.y_velocity *= -1
                elif self.y + self.bounding_box_size >= top_post:
                    self.y_velocity *= -1
            else:
                if self.x - self.bounding_box_size <= left_post:
                    other.right_score_up()
                    self.x = 600
                    self.y = 375
                    self.x_velocity = 0
                    self.y_velocity = 0
                elif self.x + self.bounding_box_size >= right_post:
                    self.x_velocity *= -1
                if self.y - self.bounding_box_size <= bottom_post:
                    self.y_velocity *= -1
                elif self.y + self.bounding_box_size >= top_post:
                    self.y_velocity *= -1
            pass
