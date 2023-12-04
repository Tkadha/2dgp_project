from pico2d import *

import game_framework
import play_mode
import team_select_mode
import title_mode


def init():
    global image
    global press_next
    global choice
    global choice_1
    global choice_2
    global bgm
    global select
    global font
    font = load_font('ENCR10B.TTF', 40)
    select = 0
    image = load_image('./resource/select_background.png')
    press_next = load_image('./resource/press_next.png')
    choice=load_image('./resource/choice.png')
    choice_1 = load_image('./resource/1.png')
    choice_2 = load_image('./resource/2.png')
    bgm = load_music('./sound/pick.mp3')
    bgm.set_volume(32)


def finish():
    global image
    global press_next
    global choice
    global choice_1
    global choice_2
    del image
    del press_next
    del choice
    del choice_1
    del choice_2


def handle_events():
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            bgm.play()
            if select == 0:
                game_framework.change_mode(team_select_mode)
            else:
                select -= 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            bgm.play()
            if select >= 1:
                game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            if select == 0:
                bgm.play()
                play_mode.select_skill('SizeUp')
                select += 1
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            if select == 0:
                bgm.play()
                play_mode.select_skill('SpeedUp')
                select += 1


def update():
    pass


def draw():
    clear_canvas()
    image.draw(600, 400)
    choice_1.draw(350, 200)
    choice_2.draw(700, 200)
    font.draw(300,300,'SizeUp',(255, 255, 255))
    font.draw(600,300,'SpeedUp',(255, 255, 255))
    if select == 0:
        choice.draw(600, 500)
        pass
    elif select == 1:
        press_next.draw(600, 500, 400, 200)
        pass
    update_canvas()
