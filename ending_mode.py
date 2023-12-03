from pico2d import *

import game_framework
import title_mode


def init():
    global background
    global bgm
    background = load_image('./resource/ending.png')
    bgm = load_music('./sound/ending.mp3')
    bgm.set_volume(32)
    bgm.play()


def finish():
    global background
    del background


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(title_mode)

def update():
    pass

def draw():
    clear_canvas()
    background.draw(600, 400)
    update_canvas()
