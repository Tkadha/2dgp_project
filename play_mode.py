from pico2d import *

import game_framework
import game_world
import title_mode
from user_hockey_player import User
from field import Field
from hockeypuck import Puck
from ai import Ai
from our_goalpost import Our_Goalpost
from enemy_goalpost import Enemy_Goalpost


# Game object class here

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            user.handle_event(event)


def select_team(l, r):
    global left
    global right
    left = l
    right = r
    pass


def init():
    global running
    global world
    global field
    global user
    global puck
    global ai
    global our_goalpost
    global enemy_goalpost
    global left
    global right
    running = True
    world = []

    field = Field()
    game_world.add_object(field, 0)
    our_goalpost = Our_Goalpost()
    enemy_goalpost = Enemy_Goalpost()
    game_world.add_object(our_goalpost, 0)
    game_world.add_object(enemy_goalpost, 0)

    user = User(left)
    game_world.add_object(user, 2)
    puck = Puck()
    game_world.add_object(puck, 1)

    ai = Ai(800, 400, 1, right)
    game_world.add_object(ai, 2)

    game_world.add_collision_pair('user:puck', user, puck)
    game_world.add_collision_pair('ai:puck', ai, puck)
    game_world.add_collision_pair('user:field', user, field)
    game_world.add_collision_pair('puck:field', puck, field)
    game_world.add_collision_pair('puck:post', puck, our_goalpost)
    game_world.add_collision_pair('puck:post', None, enemy_goalpost)
    game_world.add_collision_pair('user:post', user, our_goalpost)
    game_world.add_collision_pair('user:post', None, enemy_goalpost)
    game_world.add_collision_pair('ai:field', ai, field)
    game_world.add_collision_pair('ai:post', ai, our_goalpost)
    game_world.add_collision_pair('ai:post', None, enemy_goalpost)


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    for layer in game_world.objects:
        for o in layer:
            layer.remove(o)
    pass


def pause():
    pass


def resume():
    pass
