
from math import *
import random

class GameOverError(Exception):
    pass


class Board:
    def __init__(self):
        self.width = 1.0
        self.height = 1.0
        self.snake = Snake(0.5, 0.5)
        self.length = 0
        
    def get_length(self):
        return self.length
        
    def get_candy(self):
        return Candy(random.random(),random.random())

    def eat_candy(self, num):
        self.length += num
    
    def move_snake(self, time):
        posw, posh = self.snake.get_pos()
        if posw < self.width and posw > 0 and posh < self.height and posh > 0:
            self.snake.move(time)
        else:
            raise GameOverError

    def get_pos(self):
        posw, posh = self.snake.get_pos()
        fracw = posw
        frach = posh
        return fracw, frach

    def left(self, time):
        dirc = 180
        self.to_dirc(dirc, time)

    def up(self, time):
        dirc = 270
        self.to_dirc(dirc, time)

    def right(self, time):
        dirc = 0
        self.to_dirc(dirc, time)

    def down(self, time):
        dirc = 90
        self.to_dirc(dirc, time)

    def to_dirc(self, dirc, time):
        current_dirc = self.snake.get_dirc()
        if current_dirc > 180 and dirc == 0:
                dirc = 360
        if current_dirc < 90 and dirc == 270:
            dirc = -90
        if current_dirc > 270 and dirc == 90:
            dirc = 450
        closer_speed = dirc - current_dirc
        new_dirc = current_dirc + closer_speed * time * 10
        if new_dirc > 360:
            new_dirc -= 360 
        if new_dirc < 0:
            new_dirc += 360 
        self.snake.change_dirc(new_dirc)

    def get_snake_angle(self):
        return self.snake.get_dirc()


class Snake:
    def __init__(self, posw, posh , dirc = 225, speed = 0.3):
        self.posw = posw
        self.posh = posh
        self.dirc = dirc
        self.speed = speed

    def go_up(self, time):
        self.dirc += dirc

    def move(self, time):
        distance = time * self.speed
        self.posw += cos(self.get_radians()) * distance
        self.posh += sin(self.get_radians()) * distance

    def get_radians(self):
        return radians(self.dirc)

    def get_speed(self):
        return self.speed

    def get_pos(self):
        return self.posw, self.posh

    def get_dirc(self):
        return self.dirc

    def change_dirc(self, d):
        self.dirc = d

class Candy:
    def __init__(self, posw, posh):
        self.posw = posw
        self.posh = posh

    def get_pos(self):
        return self.posw, self.posh


if __name__ == '__main__':
    gb = Board()
    print(gb.snake.get_pos())
    gb.move_snake(7.5)
    print(gb.snake.get_pos())
