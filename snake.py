"""A simple snake game for micro:bit chip"""

import time
import random
from collections import namedtuple

from microbit import display, button_a, button_b, Image



# GAME SETTINGS

# Map constant
COL_LEN = 5  # row and column number in micro:bit
MAP_LEN = COL_LEN ** 2

# Point in Map, data structure
point = namedtuple('point', ['x', 'y'])

# Image: LED opacity settings.
LIGHT, MEDIUM, DENSE = "0", "5", "9"

# CLOCK: clock delay time and frequency
CLOCK = 0.002  # Period 2 ms
FRAME = 50  # How fast the snake goes


"Game manager that keeps the game's status"
class Game:
    def __init__(self):
        self.map = [LIGHT] * (COL_LEN ** 2)
        self.food = point(0, 0)  # food's position
        self.frame = 0
        self.finished = False

    def generate_food(self, snake_body):
        while 1:
            new_food = point(random.randint(0, COL_LEN - 1), random.randint(0, COL_LEN - 1))
            if not snake_body.count(new_food):
                self.food = new_food
                break


"""Snake object that describe the snake's body and current moving direction"""
class Snake:
    def __init__(self):
        self.body = [point(2, 2), point(2, 3)]
        self.direction = 0


"""Helper function that generates the string for Image input"""
def generate_image(current_map):
    graph = "".join(current_map)
    return Image(":".join([graph[i: i + COL_LEN] for i in range(0, MAP_LEN, COL_LEN)]))


# GAME!

game = Game()
snake = Snake()

while 1:
    if not game.finished:
        # Button A make a left turn, Butten B make a right turn
        if button_a.was_pressed():
            snake.direction += 1
        elif button_b.was_pressed():
            snake.direction -= 1

        # copy current game's map as current_map
        current_map = game.map.copy()

        # mark the current game's food position as MEDIUM in the map
        current_map[game.food.y * COL_LEN + game.food.x] = MEDIUM

        # mark snake's body as DENSE in the map
        for body in snake.body:
            current_map[body.y * COL_LEN + body.x] = DENSE

        # Rendering the map
        display.show(generate_image(current_map))

        # Take the direction action and update the snake body (eg per 0.5 sec)
        if game.frame % FRAME == 0:
            # avoid overflow
            game.frame = 0

            # Taking out snake's head, tail and middle
            head = snake.body[0]
            tail = snake.body[-1]
            middle = snake.body[1:-1]
            new_body = snake.body[:-1]
            x, y = head

            if snake.direction % 4 == 0:
                # avoid overflow
                snake.direction = 0
                new_head = point(x, y - 1)  # UP
                if new_head.y < 0 or snake.body.count(new_head) >= 2:
                    game.finished = True
            elif snake.direction % 4 == 1:
                new_head = point(x - 1, y)  # LEFT
                if new_head.x < 0 or snake.body.count(new_head) >= 2:
                    game.finished = True
            elif snake.direction % 4 == 2:
                new_head = point(x, y + 1)  # DOWN
                if new_head.y >= COL_LEN or snake.body.count(new_head) >= 2:
                    game.finished = True
            elif snake.direction % 4 == 3:
                new_head = point(x + 1, y)  # RIGHT
                if new_head.x >= COL_LEN or snake.body.count(new_head) >= 2:
                    game.finished = True

            if game.finished:
                break

            # Add new head to new_body
            new_body.insert(0, new_head)

            # Add tail if the snake gets the food
            if new_head == game.food:
                new_body.append(tail)
                # generate game's new food
                game.generate_food(new_body)

            # finally replace snake whole body with new_body
            snake.body = new_body.copy()

    time.sleep(CLOCK)
    game.frame += 1
