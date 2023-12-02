# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, SDLK_s, \
    draw_rectangle, get_time
from sdl2 import SDLK_d

import game_framework


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def above_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def above_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def under_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def under_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def time_out(e):
    return e[0] == 'TIME_OUT'


def change_idle(e):
    return e[0] == 'CHANGE_IDLE'


def shooting_end(e):
    return e[0] == 'SHOOTING_END'


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
IDLE_FRAMES_PER_ACTION = 2
RUN_FRAMES_PER_ACTION = 4
SHOOT_FRAMES_PER_ACTION = 6


class Idle:

    @staticmethod
    def enter(user, e):
        user.action = 3
        user.frame = 0
        user.key_down_count = 0
        user.LR_way, user.UD_way = 0, 0
        user.RUN_SPEED_KMPH = 20.0  # Km / Hour
        if time_out(e):
            if user.skill == 'SizeUp':
                user.size = 75
                user.bounding_box_size = 25
        pass

    @staticmethod
    def exit(user, e):
        if s_down(e) and user.skill_onoff == 'off':
            if user.skill == 'SizeUp':
                user.size *= 2
                user.bounding_box_size *= 2
                pass
            user.skill_onoff = 'on'
            user.skill_time = get_time()
        pass

    @staticmethod
    def do(user):
        user.frame = (
                             user.frame + IDLE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % IDLE_FRAMES_PER_ACTION
        if user.skill_onoff == 'on':
            if get_time() - user.skill_time > 3:
                user.skill_onoff = 'off'
                user.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(user):
        if user.dir == 0:
            user.image.clip_draw(int(user.frame) * 35, user.action * 40, 35, 40, user.x, user.y, user.size, user.size)
        elif user.dir == 1:
            user.image.clip_composite_draw(int(user.frame) * 35, user.action * 40, 35, 40, 0, 'h', user.x, user.y,
                                           user.size,
                                           user.size)
        pass
class Run:

    @staticmethod
    def enter(user, e):
        user.action = 2
        user.frame = 0
        if right_down(e):
            user.LR_way = 1
            user.dir = 0
            user.key_down_count += 1
        elif left_down(e):
            user.LR_way = 2
            user.dir = 1
            user.key_down_count += 1
        elif under_down(e):
            user.UD_way = 1
            user.key_down_count += 1
        elif above_down(e):
            user.UD_way = 2
            user.key_down_count += 1

        if time_out(e):
            if user.skill == 'SizeUp':
                user.size = 75
                user.bounding_box_size = 25
        pass

    @staticmethod
    def exit(user, e):
        if s_down(e) and user.skill_onoff == 'off':
            if user.skill == 'SizeUp':
                user.size *= 2
                user.bounding_box_size *= 2
            user.skill_onoff = 'on'
            user.skill_time = get_time()

        if right_up(e):
            user.key_down_count -= 1
            user.LR_way = 0
            pass
        elif left_up(e):
            user.key_down_count -= 1
            user.LR_way = 0
            pass
        elif under_up(e):
            user.key_down_count -= 1
            user.UD_way = 0
            pass
        elif above_up(e):
            user.key_down_count -= 1
            user.UD_way = 0
            pass
        pass

    @staticmethod
    def do(user):
        user.frame = (
                             user.frame + RUN_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % RUN_FRAMES_PER_ACTION
        if 0 + 50 <= user.x <= 1200 - 50:
            if user.LR_way == 1:
                user.x += user.RUN_SPEED_PPS * game_framework.frame_time
            elif user.LR_way == 2:
                user.x -= user.RUN_SPEED_PPS * game_framework.frame_time
        if 0 <= user.y <= 800:
            if user.UD_way == 1:
                user.y -= user.RUN_SPEED_PPS * game_framework.frame_time
            elif user.UD_way == 2:
                user.y += user.RUN_SPEED_PPS * game_framework.frame_time

        check_out_field(user)

        if user.skill_onoff == 'on':
            if get_time() - user.skill_time > 3:
                user.skill_onoff = 'off'
                user.state_machine.handle_event(('TIME_OUT', 0))
        if user.key_down_count <= 0:
            user.state_machine.handle_event(('CHANGE_IDLE', 0))
        pass

    @staticmethod
    def draw(user):
        if user.dir == 0:
            user.image.clip_draw(int(user.frame) * 35, user.action * 40, 35, 40, user.x, user.y, user.size, user.size)
        elif user.dir == 1:
            user.image.clip_composite_draw(int(user.frame) * 35, user.action * 40, 35, 40, 0, 'h', user.x, user.y,
                                           user.size, user.size)
        pass


class Shoot:
    @staticmethod
    def enter(user, e):
        user.action = 1
        user.frame = 0
        if time_out(e):
            if user.skill == 'SizeUp':
                user.size = 75
                user.bounding_box_size = 25
        pass

    @staticmethod
    def exit(user, e):
        if user.contact_puck:
            user.shooting = True
        if s_down(e) and user.skill_onoff == 'off':
            if user.skill == 'SizeUp':
                user.size *= 2
                user.bounding_box_size *= 2
            user.skill_onoff = 'on'
            user.skill_time = get_time()
        pass

    @staticmethod
    def do(user):
        if user.frame + 1 >= SHOOT_FRAMES_PER_ACTION:
            user.state_machine.handle_event(('SHOOTING_END', 0))
        user.frame = (
                             user.frame + SHOOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SHOOT_FRAMES_PER_ACTION
        if user.skill_onoff == 'on':
            if get_time() - user.skill_time > 3:
                user.skill_onoff = 'off'
                user.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(user):
        if user.dir == 0:
            if user.frame < 4:
                user.image.clip_draw(int(user.frame) * 35, user.action * 40, 35, 38, user.x, user.y, user.size,
                                     user.size)
            else:
                user.image.clip_draw(int(user.frame - 3) * 40 + 3 * 35, user.action * 40, 35, 38, user.x, user.y,
                                     user.size, user.size)
        elif user.dir == 1:
            if user.frame < 4:
                user.image.clip_composite_draw(int(user.frame) * 35, user.action * 40, 35, 40, 0, 'h', user.x, user.y,
                                            user.size, user.size)
            else:
                user.image.clip_composite_draw(int(user.frame - 3) * 40 + 3 * 35, user.action * 40, 35, 40, 0, 'h', user.x, user.y,
                                            user.size, user.size)

        pass

    pass


class StateMachine:
    def __init__(self, user):
        self.user = user
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, above_down: Run, above_up: Run,
                   under_down: Run, under_up: Run, s_down: Idle, time_out: Idle, d_down: Shoot},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, above_down: Run, above_up: Run,
                  under_down: Run, under_up: Run, s_down: Run, time_out: Run, change_idle: Idle, d_down: Shoot},
            Shoot: {shooting_end: Idle, s_down: Shoot, time_out: Shoot}
        }

    def start(self):
        self.cur_state.enter(self.user, ('START', 0))

    def update(self):
        self.cur_state.do(self.user)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.user, e)
                self.cur_state = next_state
                self.cur_state.enter(self.user, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.user)


class User:
    image = None

    def load_image(self, image):
        if User.image is None:
            if image == 'black':
                self.image = load_image('./resource/black_hockey.png')
            elif image == 'yellow':
                self.image = load_image('./resource/yellow_hockey.png')
            elif image == 'red':
                self.image = load_image('./resource/red_hockey.png')

    def __init__(self, image=None):
        self.x, self.y = 400, 400
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.LR_way = 1
        self.UD_way = 1
        self.key_down_count = 0
        self.size = 75
        self.bounding_box_size = 25
        self.shooting = False
        self.contact_puck = False
        self.skill = 'SizeUp'
        self.skill_time = get_time()
        self.skill_onoff = 'off'
        self.RUN_SPEED_KMPH = 20.0  # Km / Hour
        self.RUN_SPEED_PPS = (((self.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)
        self.load_image(image)
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.bounding_box_size, self.y - self.bounding_box_size - 10, self.x + self.bounding_box_size, self.y

    def handle_collision(self, group, other):
        if group == 'user:puck':
            pass
        if group == 'user:field':
            if self.x - self.bounding_box_size <= 100:
                self.x = 100 + self.bounding_box_size
            elif self.x + self.bounding_box_size >= 1100:
                self.x = 1100 - self.bounding_box_size
            if self.y - self.bounding_box_size - 10 <= 50:
                self.y = 50 + self.bounding_box_size + 10
            elif self.y >= 700:
                self.y = 700
            pass
        if group == 'user:post':
            if 0 + 50 <= self.x <= 1200 - 50:
                if self.LR_way == 1:
                    self.x -= self.RUN_SPEED_PPS * game_framework.frame_time
                elif self.LR_way == 2:
                    self.x += self.RUN_SPEED_PPS * game_framework.frame_time
            if 0 <= self.y <= 800:
                if self.UD_way == 1:
                    self.y += self.RUN_SPEED_PPS * game_framework.frame_time
                elif self.UD_way == 2:
                    self.y -= self.RUN_SPEED_PPS * game_framework.frame_time
            pass


def check_out_field(user):
    if user.x < 50:
        user.x = 50
    elif user.x > 1150:
        user.x = 1150
    if user.y < 50:
        user.y = 50
    elif user.y > 750:
        user.y = 750
