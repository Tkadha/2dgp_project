from pico2d import *

import game_framework
import play_mode
import skill_select_mode
import title_mode


def init():
    global image
    global black
    global red
    global yellow
    global select
    global select_your
    global select_other
    global press_next
    global choice_1
    global choice_2
    global choice_3
    select = 0
    image = load_image('./resource/select_background.png')
    black = load_image('./resource/Black.png')
    red = load_image('./resource/Red.png')
    yellow = load_image('./resource/Yellow.png')
    select_your = load_image('./resource/select_1.png')
    select_other = load_image('./resource/select_2.png')
    press_next = load_image('./resource/press_next.png')
    choice_1 = load_image('./resource/1.png')
    choice_2 = load_image('./resource/2.png')
    choice_3 = load_image('./resource/3.png')

def finish():
    global image
    global black
    global red
    global yellow
    global select_your
    global select_other
    global press_next
    global choice_1
    global choice_2
    global choice_3
    del image
    del black
    del red
    del yellow
    del select_your
    del select_other
    del press_next
    del choice_1
    del choice_2
    del choice_3


def handle_events():
    global left
    global right
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            if select == 0:
                game_framework.change_mode(title_mode)
            else:
                select -= 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if select >= 2:
                play_mode.select_team(left, right)
                game_framework.change_mode(skill_select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            if select == 0:
                left = 'black'
                select += 1
            elif select == 1:
                if left != 'black':
                    right = 'black'
                    select += 1
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            if select == 0:
                left = 'red'
                select += 1
            elif select == 1:
                if left != 'red':
                    right = 'red'
                    select += 1
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            if select == 0:
                left = 'yellow'
                select += 1
            elif select == 1:
                if left != 'yellow':
                    right = 'yellow'
                    select += 1
            pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(600, 400)
    black.draw(300, 300, 250, 200)
    red.draw(600, 300, 250, 200)
    yellow.draw(900, 300, 250, 200)
    choice_1.draw(300,150)
    choice_2.draw(600,150)
    choice_3.draw(900,150)
    if select == 0:
        select_your.draw(600, 500)
        pass
    elif select == 1:
        select_other.draw(600, 500)
        pass
    elif select == 2:
        press_next.draw(600, 500, 400, 200)
        pass
    update_canvas()
