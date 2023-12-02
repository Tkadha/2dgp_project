import math

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import play_mode
from behavior_tree import BehaviorTree, Action, Condition, Sequence, Selector

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
IDLE_FRAMES_PER_ACTION = 2
RUN_FRAMES_PER_ACTION = 4
SHOOT_FRAMES_PER_ACTION = 6


class Ai:
    image = None

    def load_image(self, image):
        if Ai.image is None:
            if image == 'black':
                self.image = load_image('./resource/black_hockey.png')
            elif image == 'yellow':
                self.image = load_image('./resource/yellow_hockey.png')
            elif image == 'red':
                self.image = load_image('./resource/red_hockey.png')

    def __init__(self, x=None, y=None, LR=None, image=None):
        self.x, self.y = x, y
        self.frame = 0
        self.action = 3
        self.dir = LR
        self.face_dir = 1
        self.size = 75
        self.bounding_box_size = 25
        self.load_image(image)
        self.max_speed = 100
        self.speed_increase = 0.1
        self.RUN_SPEED_KMPH = 15.0  # Km / Hour
        self.RUN_SPEED_PPS = (((self.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)
        self.speed = self.RUN_SPEED_PPS
        self.state = 'IDLE'
        self.have_puck = False
        self.shoot = False
        self.build_behavior_tree()

    def update(self):
        if self.state == 'IDLE':
            self.action = 3
            self.frame = (
                                 self.frame + IDLE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % IDLE_FRAMES_PER_ACTION
        elif self.state == 'RUN':
            self.action = 2
            self.frame = (
                                 self.frame + RUN_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % RUN_FRAMES_PER_ACTION
        elif self.state == 'SHOOT':
            self.action = 1
            self.frame = (
                                     self.frame + SHOOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SHOOT_FRAMES_PER_ACTION
        self.bt.run()
        pass

    def draw(self):
        if self.state == 'IDLE' or self.state == 'RUN':
            if self.face_dir == 0:
                self.image.clip_draw(int(self.frame) * 35, self.action * 40, 35, 40, self.x, self.y, self.size,
                                     self.size)
            elif self.face_dir == 1:
                self.image.clip_composite_draw(int(self.frame) * 35, self.action * 40, 35, 40, 0, 'h', self.x, self.y,
                                               self.size, self.size)
        elif self.state == 'SHOOT':
            if self.face_dir == 0:
                if self.frame < 4:
                    self.image.clip_draw(int(self.frame) * 35, self.action * 40, 35, 38, self.x, self.y, self.size,
                                         self.size)
                else:
                    self.image.clip_draw(int(self.frame - 3) * 40 + 3 * 35, self.action * 40, 35, 38, self.x, self.y,
                                         self.size, self.size)
            elif self.face_dir == 1:
                if self.frame < 4:
                    self.image.clip_composite_draw(int(self.frame) * 35, self.action * 40, 35, 38, 0, 'h', self.x,
                                                   self.y,
                                                   self.size, self.size)
                else:
                    self.image.clip_composite_draw(int(self.frame - 3) * 40 + 3 * 35, self.action * 40, 35, 38, 0, 'h',
                                                   self.x, self.y,
                                                   self.size, self.size)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.bounding_box_size, self.y - self.bounding_box_size - 10, self.x + self.bounding_box_size, self.y

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'ai:puck':
            pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = self.RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time / 2
        if math.cos(self.dir) > 0:
            self.face_dir = 0
        else:
            self.face_dir = 1

    def is_have_puck(self):
        if self.have_puck:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_near_post(self, r):
        for o in game_world.objects[0]:
            if o == play_mode.our_goalpost:
                px, py = o.x, o.y
                break
        if self.distance_less_than(px, py, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def shoot_puck(self):
        self.state = 'SHOOT'
        self.shoot = True
        return BehaviorTree.SUCCESS

    def is_shooting(self):
        if self.shoot:
            if self.frame + 1 >= SHOOT_FRAMES_PER_ACTION:
                self.state = 'IDLE'
                self.have_puck = False
                self.shoot = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def move_forward(self, r=0.5):
        for o in game_world.objects[0]:
            if o == play_mode.our_goalpost:
                px, py = o.x, o.y + 60
        self.move_slightly_to(px, py)
        if self.distance_less_than(px, py, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_near_enemy(self, r):
        for o in game_world.objects[2]:
            if o == play_mode.user:
                px, py = o.x, o.y
        if self.distance_less_than(px, py, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def avoid_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = self.RUN_SPEED_PPS
        self.x -= self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y -= self.speed * math.sin(self.dir) * game_framework.frame_time
        if math.cos(self.dir) > 0:
            self.face_dir = 1
        else:
            self.face_dir = 0

    def avoid_enemy(self, r = 0.5):
        self.state = 'RUN'
        for o in game_world.objects[2]:
            if o == play_mode.user:
                px, py = o.x, o.y
        self.avoid_slightly_to(px, py)
        if self.distance_less_than(px, py, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def is_near_puck(self, r):
        for puck in game_world.objects[1]:
            px, py = puck.x, puck.y
        if self.distance_less_than(px, py, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_the_puck(self, r=0.5):
        self.state = 'RUN'
        for puck in game_world.objects[1]:
            px, py = puck.x, puck.y
        self.move_slightly_to(px, py)
        if self.distance_less_than(px, py, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass


    def build_behavior_tree(self):
        a1 = Action('Move to puck', self.move_to_the_puck)
        c1 = Condition('근처에 공이 있는가', self.is_near_puck, 20)
        root = SEQ_move_to_puck = Sequence('공을 추적', c1, a1)

        a2 = Action('Move to forward', self.move_forward)
        c2 = Condition('공을 가지고 있는가', self.is_have_puck)
        c3 = Condition('골대와 가까운가', self.is_near_post, 8)
        a3 = Action('슛', self.shoot_puck)
        SEQ_shoot = Sequence('shooting', c2, c3, a3)
        a4 = Action('슈팅 중', self.is_shooting)

        c4 = Condition('근처에 적이 있는가',self.is_near_enemy,5)
        a5 = Action('회피',self.avoid_enemy)
        a6 = Action('전진',self.move_forward)
        SEQ_avoid=Sequence('적과 가까우면 피하기',c4,a5)
        SEL_avoid_or_forward=Selector('회피 또는 전진',SEQ_avoid,a6)
        SEQ_have_puck=Sequence('공을 가진 채 이동',c2,SEL_avoid_or_forward)
        root = SEL_move = Selector("공을 가지고 전진 또는 공을 추적", SEQ_have_puck, SEQ_move_to_puck)
        root = Selector('shoot or move', a4, SEQ_shoot, SEL_move)



        self.bt = BehaviorTree(root)
        pass
