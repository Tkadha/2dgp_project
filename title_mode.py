from pico2d import *

import game_framework
import play_mode
import team_select_mode
def init():
    global image
    image = load_image('./resource/title.png')


def finish():
    global image
    del image


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(team_select_mode)

def update():
    pass

def draw():
    clear_canvas()
    image.draw(600, 400)
    update_canvas()
