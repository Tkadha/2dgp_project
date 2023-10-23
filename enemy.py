from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT



class Idle:

    @staticmethod
    def enter(enemy, e):
        pass

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        pass

    @staticmethod
    def draw(enemy):
        pass



class Run:

    @staticmethod
    def enter(enemy, e):
        pass

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        pass

    @staticmethod
    def draw(enemy):
        pass



class StateMachine:
    def __init__(self, enemy):
        self.enemy = enemy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
        }

    def start(self):
        self.cur_state.enter(self.enemy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.enemy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.enemy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.enemy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.enemy)





class User_char:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.face_dir = 1
        self.image = load_image('')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
