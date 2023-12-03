from pico2d import *

import game_framework
import title_mode


def init():
    global background
    global bgm
    global font
    font = load_font('ENCR10B.TTF', 200)
    background = load_image('./resource/ending.png')
    bgm = load_music('./sound/ending.mp3')
    bgm.set_volume(32)
    bgm.play()


def score(left, right):
    global left_score
    global right_score
    left_score = left
    right_score = right

def vic_char(image):

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
            bgm.stop()
            game_framework.change_mode(title_mode)


def update():
    pass


def draw():
    clear_canvas()
    background.draw(600, 400)
    font.draw(200, 400, f'{left_score}', (255, 255, 255))
    font.draw(850, 400, f'{right_score}', (255, 255, 255))
    update_canvas()
