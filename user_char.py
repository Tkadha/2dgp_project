# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN


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


class Idle:

    @staticmethod
    def enter(user, e):
        user.action = 3
        user.frame = 0
        user.speed = 15
        user.LR_way, user.UD_way = 0, 0
        pass

    @staticmethod
    def exit(user, e):
        pass

    @staticmethod
    def do(user):
        user.frame = (user.frame + 1) % 2
        pass

    @staticmethod
    def draw(user):
        if user.dir == 0:
            user.image.clip_draw(user.frame * 35, user.action * 40, 35, 40, user.x, user.y, 75, 75)
        elif user.dir == 1:
            user.image.clip_draw(35 + user.frame * 35, user.action * 40, -35, 40, user.x, user.y, 75, 75)

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
        user.frame = (user.frame + 1) % 4
        if user.LR_way == 1:
            user.x += user.speed
        elif user.LR_way == 2:
            user.x -= user.speed
        if user.UD_way == 1:
            user.y -= user.speed - 5
        elif user.UD_way == 2:
            user.y += user.speed + 5
        if user.speed <= 30:
            user.speed += 5
        pass

    @staticmethod
    def draw(user):
        if user.dir == 0:
            user.image.clip_draw(user.frame * 35, user.action * 40, 35, 40, user.x, user.y, 75, 75)
        elif user.dir == 1:
            user.image.clip_draw(35 + user.frame * 35, user.action * 40, -35, 40, user.x, user.y, 75, 75)
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
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.speed = 15
        self.LR_way = 1
        self.UD_way = 1
        if User.image == None:
            User.image = load_image('red_hockey.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
