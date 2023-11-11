from pico2d import *

import game_framework
import game_world
from user_hockeyer import User
from field import Field
from hockeypuck import Puck

# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            user.handle_event(event)


def init():
    global running
    global world
    global field
    global user
    global puck
    running = True
    world = []

    field = Field()
    game_world.add_object(field, 0)
    user = User()
    game_world.add_object(user, 2)
    puck = Puck()
    game_world.add_object(puck, 1)

    game_world.add_collision_pair('user:puck',user,puck)


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    pass

def pause():
    pass

def resume():
    pass
