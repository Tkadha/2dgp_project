import pico2d
import play_mode
import game_framework
canvas_width=1200
canvas_height=800

pico2d.open_canvas(canvas_width,canvas_height)
game_framework.run(play_mode)
pico2d.close_canvas()