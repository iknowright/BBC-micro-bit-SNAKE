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

while game:
    # Button A make a left turn, Butten B make a right turn
    if button_a.was_pressed():
        current_direction += 1
    elif button_b.was_pressed():
        current_direction -= 1

    # Rendering the map per delay (eg per 0.05)
    map_arr = blank_map.copy()
    map_arr[food[1]*5 + food[0]] = "5"
    for body in snake_body:
        map_arr[body[1]*5 + body[0]] = "9"
    the_map = "".join(map_arr)
    the_map = the_map[:5] + ':' + the_map[5:10] + ':' + the_map[10:15] + ':' + the_map[15:20] + ':' + the_map[20:] 
    the_map = Image(the_map)
    display.show(the_map)

    # Take the direction action and update the snake body (eg per 0.5 sec)
    if counter % 25 == 0:
        for i in reversed(range(len(snake_body))):
            if i == len(snake_body) - 1:
                tail = snake_body[i]
                snake_body[i] = snake_body[i-1].copy()
            elif i == 0:
                if current_direction % 4 == 0:
                    snake_body[i][1] = snake_body[i][1] - 1
                    if snake_body[i][1] < 0 or snake_body.count(snake_body[i]) >= 2:
                        game = False
                        break
                elif current_direction % 4 == 1:
                    snake_body[i][0] = snake_body[i][0] - 1
                    if snake_body[i][0] < 0 or snake_body.count(snake_body[i]) >= 2:
                        game = False
                        break
                elif current_direction % 4 == 2:                        
                    snake_body[i][1] = snake_body[i][1] + 1
                    if snake_body[i][1] >= 5 or snake_body.count(snake_body[i]) >= 2:
                        game = False
                        break
                elif current_direction % 4 == 3:                
                    snake_body[i][0] = snake_body[i][0] + 1             
                    if snake_body[i][0] >= 5 or snake_body.count(snake_body[i]) >= 2:
                        game = False
                        break
                if snake_body[i] == food:
                    snake_body.append(tail)
                    generate_food()
            else:
                snake_body[i] = snake_body[i-1].copy()
    time.sleep(0.002)
    counter += 1