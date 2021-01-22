"""A simple snake game for micro:bit chip"""

import time
import random

# pylint: disable = E0401
from microbit import (
    display,
    button_a,
    button_b,
    Image
)

# pylint: enable = E0401


N = 5  # row and column number in micro:bit


class Game:
    def __init__(self):
        self.blank_map = ["0"] * (N ** 2)
        self.food = [0, 0]  # food's position
        self.counter = 0
        self.finished = False

    def generate_food(self, snake):
        got_food = False
        while not got_food:
            self.food = [random.randint(0, N), random.randint(0, N)]
            if self.food not in snake.body:
                got_food = True

    def generate_image(self, graph):
        return Image(":".join(
            [
                graph[i: i + 5]
                for i in range(0, N * N, N)
            ]
        ))


class Snake:
    def __init__(self):
        self.snake.body = [[2, 2], [2, 3]]
        self.direction = 0


game = Game()
snake = Snake()

while game:
    # Button A make a left turn, Butten B make a right turn
    if button_a.was_pressed():
        snake.direction += 1
    elif button_b.was_pressed():
        snake.direction -= 1

    # Update snake body and food position
    map_arr = game.blank_map.copy()
    map_arr[food[1] * N + food[0]] = "5"
    for body in snake.body:
        map_arr[body[1] * N + body[0]] = "9"

    # Rendering the map
    display.show(game.generate_image(map_arr))

    # Take the direction action and update the snake body (eg per 0.5 sec)
    if game.counter % 25 == 0:
        for i in reversed(range(len(snake.body))):
            if i == len(snake.body) - 1:
                tail = snake.body[i]
                snake.body[i] = snake.body[i-1].copy()
            elif i == 0:
                if snake.direction % 4 == 0:
                    snake.body[i][1] = snake.body[i][1] - 1
                    if snake.body[i][1] < 0 or snake.body.count(snake.body[i]) >= 2:
                        game = False
                        break
                elif snake.direction % 4 == 1:
                    snake.body[i][0] = snake.body[i][0] - 1
                    if snake.body[i][0] < 0 or snake.body.count(snake.body[i]) >= 2:
                        game = False
                        break
                elif snake.direction % 4 == 2:
                    snake.body[i][1] = snake.body[i][1] + 1
                    if snake.body[i][1] >= 5 or snake.body.count(snake.body[i]) >= 2:
                        game = False
                        break
                elif snake.direction % 4 == 3:
                    snake.body[i][0] = snake.body[i][0] + 1
                    if snake.body[i][0] >= 5 or snake.body.count(snake.body[i]) >= 2:
                        game = False
                        break
                if snake.body[i] == game.food:
                    snake.body.append(tail)
                    game.generate_food()
            else:
                snake.body[i] = snake.body[i-1].copy()

    time.sleep(0.002)
    game.counter += 1
