# Add your Python code here. E.g.
from microbit import *

import time
import random

# global initialization
blank_map = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
food = [0, 0]
default_body = [[2, 2], [2, 3]]
snake_body = default_body.copy()
current_direction = 0
counter = 0
game = True


def generate_food():
    got_food = False
    while not got_food:
        food[0] = random.randint(0,4)
        food[1] = random.randint(0,4)
        if food not in snake_body:
            got_food = True

def default_setting():
    snake_body = default_body.copy()
    current_direction = 0
    generate_food()
    game = True
    counter = 0

default_setting()

while game:
    if button_a.was_pressed():
        current_direction += 1
    elif button_b.was_pressed():
        current_direction -= 1

    map_arr = blank_map.copy()
    map_arr[food[1]*5 + food[0]] = "9"
    for body in snake_body:
        map_arr[body[1]*5 + body[0]] = "9"
    the_map = "".join(map_arr)
    the_map = the_map[:5] + ':' + the_map[5:10] + ':' + the_map[10:15] + ':' + the_map[15:20] + ':' + the_map[20:] 
    the_map = Image(the_map)
    display.show(the_map)
    if counter % 10 == 0:
        if current_direction % 4 == 0: # up
            for i in reversed(range(len(snake_body))):
                if i == len(snake_body) - 1:
                    tail = snake_body[i]
                if i == 0:
                    if snake_body[i][1] - 1 < 0:
                        game = False
                        break
                    snake_body[i][1] = snake_body[i][1] - 1
                    print(snake_body[i])
                    if snake_body[i] == food:
                        snake_body.append(tail)
                        generate_food()
                else:
                    snake_body[i] = snake_body[i-1].copy()
                    print(snake_body[i])
        elif current_direction % 4 == 1: # left
            for i in reversed(range(len(snake_body))):
                if i == len(snake_body) - 1:
                    tail = snake_body[i]
                if i == 0:
                    if snake_body[i][0] - 1 < 0:
                        game = False
                        break
                    snake_body[i][0] = snake_body[i][0] - 1
                    if snake_body[i] == food:
                        snake_body.append(tail)
                        generate_food()
                else:
                    snake_body[i] = snake_body[i-1].copy()
        elif current_direction % 4 == 2: # down  
            for i in reversed(range(len(snake_body))):
                if i == len(snake_body) - 1:
                    tail = snake_body[i]
                if i == 0:
                    if snake_body[i][1] + 1 >= 5:
                        game = False
                        break
                    snake_body[i][1] = snake_body[i][1] + 1
                    if snake_body[i] == food:
                        snake_body.append(tail)
                        generate_food()
                else:
                    snake_body[i] = snake_body[i-1].copy()
        elif current_direction % 4 == 3: # right
            for i in reversed(range(len(snake_body))):
                if i == len(snake_body) - 1:
                    tail = snake_body[i]
                if i == 0:
                    if snake_body[i][0] + 1 >= 5:
                        game = False
                        break
                    snake_body[i][0] = snake_body[i][0] + 1
                    if snake_body[i] == food:
                        snake_body.append(tail)
                        generate_food()
                else:
                    snake_body[i] = snake_body[i-1].copy()

    time.sleep(0.05)
    counter += 1
