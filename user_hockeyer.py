# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, draw_rectangle

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


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
IDLE_FRAMES_PER_ACTION = 2
RUN_FRAMES_PER_ACTION = 4


class Idle:

    @staticmethod
    def enter(user, e):
        user.action = 3
        user.frame = 0
        user.LR_way, user.UD_way = 0, 0
        user.RUN_SPEED_KMPH = 20.0  # Km / Hour
        pass

    @staticmethod
    def exit(user, e):
        pass

    @staticmethod
    def do(user):
        user.frame = (user.frame + IDLE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
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
        elif left_down(e):
            user.LR_way = 2
            user.dir = 1
        elif under_down(e):
            user.UD_way = 1
        elif above_down(e):
            user.UD_way = 2
        pass

    @staticmethod
    def exit(user, e):
        pass

    @staticmethod
    def do(user):
        user.frame = (user.frame + RUN_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if 0 + 50 <= user.x <= 1200 - 50:
            if user.LR_way == 1:
                user.x += user.RUN_SPEED_PPS * game_framework.frame_time
            elif user.LR_way == 2:
                user.x -= user.RUN_SPEED_PPS * game_framework.frame_time
        if 0 <= user.y <= 800:
            if user.UD_way == 1:
                user.y -= user.RUN_SPEED_PPS * game_framework.frame_time / 2
            elif user.UD_way == 2:
                user.y += user.RUN_SPEED_PPS * game_framework.frame_time / 2
        check_out_field(user)
        if user.RUN_SPEED_KMPH < 100:
            user.RUN_SPEED_KMPH += 0.1
            user.RUN_SPEED_PPS = (((user.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)
        pass

    @staticmethod
    def draw(user):
        if user.dir == 0:
            user.image.clip_draw(int(user.frame) * 35, user.action * 40, 35, 40, user.x, user.y, user.size, user.size)
        elif user.dir == 1:
            user.image.clip_composite_draw(int(user.frame) * 35, user.action * 40, 35, 40, 0, 'h', user.x, user.y,
                                           user.size, user.size)
        pass


class StateMachine:
    def __init__(self, user):
        self.user = user
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, above_down: Run, above_up: Run,
                   under_down: Run, under_up: Run},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, above_down: Idle, above_up: Idle,
                  under_down: Idle, under_up: Idle}
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

    def __init__(self):
        self.x, self.y = 400, 350
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.LR_way = 1
        self.UD_way = 1
        self.size = 75
        self.bounding_box_size = 40
        self.RUN_SPEED_KMPH = 20.0  # Km / Hour
        self.RUN_SPEED_PPS = (((self.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)
        if User.image == None:
            User.image = load_image('resource/red_hockey.png')
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
        return self.x - self.bounding_box_size, self.y - self.bounding_box_size, self.x + self.bounding_box_size, self.y

    def handle_collision(self, group, other):
        if group == 'user:puck':
            pass
        if group == 'user:field':
            if self.x - self.bounding_box_size <= 100:
                self.x = 100 + self.bounding_box_size
            elif self.x + self.bounding_box_size >= 1100:
                self.x = 1100 - self.bounding_box_size
            if self.y - self.bounding_box_size <= 50:
                self.y = 50 + self.bounding_box_size
            elif self.y >= 700:
                self.y = 700
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
