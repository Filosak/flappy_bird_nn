import pygame
import numpy as np
from bird import Bird, Walls

class game_class:
    def __init__(self, population, networks):
        pygame.init()
        pygame.font.init()

        self.population = population
        self.networks = networks
        self.screen = pygame.display.set_mode((700, 1000))
        self.font = pygame.font.Font("projekt/font.TTF", 60)

    def draw(self, new_walls_pos):
        self.screen.fill((255,255,255))

        bird_circles = []
        for bird in self.birds:
            bird_circles.append(pygame.draw.circle(self.screen, (0,0,0), bird.possition, 30))
        
        rectangles = self.create_rectangles(new_walls_pos)
        for rect in rectangles:
            pygame.draw.rect(self.screen, (0,255,0), rect)
        
        return rectangles, bird_circles

    def move_objects(self):
        for wall in self.walls:
            wall.move(1000, 700)

        if self.walls[self.curr_wall].up_pos[0] < -100:
            self.curr_wall += 1

            if self.curr_wall > 2:
                self.curr_wall = 0

        for bird in self.birds:
            bird.new_bird_pos()
            bird.distance_traveled += 8

    def create_rectangles(self, new_walls_pos):
        rectangles = []
        for pos in new_walls_pos:
            rectangles.append(pygame.Rect(pos.up_pos[0], pos.up_pos[1], pos.up_pos[2], pos.up_pos[3]))
            rectangles.append(pygame.Rect(pos.down_pos[0], pos.down_pos[1], pos.down_pos[2], pos.down_pos[3]))
        return rectangles
    
    def reset(self):
        self.screen.fill((255, 255, 255))
        self.run = True
        self.activate = 0

        self.birds = []
        for i in range(self.population):
            self.birds.append(Bird())

        self.walls = [Walls(700, 1000), Walls(700, 1000 + 600), Walls(700, 1000 + 1200)]
        self.curr_wall = 0

        self.auto_move = pygame.USEREVENT + 1
        pygame.time.set_timer(self.auto_move, 1000 // 60)
    
    
    def feedforward(self):
        move_list = []
        for i, bird in enumerate(self.birds):
            data = np.array([
                            (self.walls[self.curr_wall].middle - self.birds[i].possition[1]) / 100,
                            (self.walls[self.curr_wall].up_pos[0] + 200 - self.birds[i].possition[0]) / 1000
                            ])
            move_list.append(self.one_forward(data, i))
        return move_list

    def one_forward(self, data, i):
        return self.networks[i].predict(data) > 0.5

    def start(self):
        self.reset()
        data_to_return = {}
        died = 1

        while self.run:
            for event in pygame.event.get():
                if event.type == self.auto_move:

                    if self.activate % 2 == 0:
                        move_list = self.feedforward()
                    self.activate += 1

                    for i, bird in enumerate(self.birds):
                        if move_list[i] == True:
                            bird.velocity = -1
 
                    for bird in self.birds:
                        bird.velocity = round(min(1.5, bird.velocity + 0.06), 2)

                    self.move_objects()
                    rectangles, bird_circles = self.draw(self.walls)

                    removed = 0
                    for i, bird_circle in enumerate(bird_circles):
                        flag = False

                        if bird.possition[1] > 1030 or bird.possition[1] < 30:
                            flag = True
                        else:
                            for rect in rectangles:
                                if rect.colliderect(bird_circle):
                                    flag = True
                        
                        if flag == True:
                            data_to_return[f"{died}"] = [
                                            self.networks[i - removed],
                                            self.birds[i - removed].distance_traveled,
                                            round(abs(self.walls[self.curr_wall].middle - self.birds[i - removed].possition[1])),
                                            ]
                            
                            del self.birds[i - removed]
                            del self.networks[i - removed]
                            removed += 1
                            died += 1

                    if not self.birds:
                        self.run = False
                
                pygame.display.update()
        return data_to_return