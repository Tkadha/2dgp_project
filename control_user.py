from pico2d import *

import game_world
from user_char import User
from field import Field


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            user.handle_event(event)


def reset_world():
    global running
    global world
    global Field
    global user

    running = True
    world = []

    Field = Field()
    game_world.add_object(Field, 0)
    user = User()
    game_world.add_object(user, 1)


def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)
# finalization code
close_canvas()
