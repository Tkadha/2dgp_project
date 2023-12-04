from pico2d import *

import game_framework
import play_mode
import team_select_mode


def init():
    global image
    global bgm
    image = load_image('./resource/pause.png')
    bgm = load_music('./sound/pick.mp3')
    bgm.set_volume(32)


def finish():
    global image
    del image


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            game_framework.pop_mode()

def update():
    pass

def draw():
    image.draw(600, 400)
    update_canvas()

def pause():
    pass


def resume():
    pass
