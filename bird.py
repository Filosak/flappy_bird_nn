import random

class Bird:
    def __init__(self):
        self.possition = [100, random.randint(300,600)]
        self.velocity = 0
        self.distance_traveled = 0

    def new_bird_pos(self):
        self.possition[1] += self.velocity * 15

class Walls:
    def __init__(self, screen_height, initial_pos):
        self.up_pos = self.create_pos("up", initial_pos, screen_height)
        self.down_pos = self.create_pos("down", initial_pos, screen_height)
        self.passed = False
        self.middle = self.up_pos[3] + 150

    def create_pos(self, direction, initial_pos, screen_h):
        if direction == "up":
            return [initial_pos, 0, 200, random.randint(10, 500)]

        else:
            return [initial_pos, self.up_pos[3] + 300, 200, screen_h - self.up_pos[3] + 300]
    
    def move(self, screen_width, screen_height):
        if self.up_pos[0] <= -800 or self.down_pos[0] <= -800:
            self.passed = False

            self.up_pos = self.create_pos("up", screen_width, screen_height)
            self.down_pos = self.create_pos("down", screen_width, screen_height)
            self.middle = self.up_pos[3] + 150
            return
        
        self.up_pos[0] -= 8
        self.down_pos[0] -= 8