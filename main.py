import pico2d
import play_mode

canvas_width=1200
canvas_height=800

pico2d.open_canvas(canvas_width,canvas_height)
play_mode.init()
# game loop
while play_mode.running:
    play_mode.handle_events()
    play_mode.update()
    play_mode.draw()
    pico2d.delay(0.1)

play_mode.finish()
# finalization code
pico2d.close_canvas()