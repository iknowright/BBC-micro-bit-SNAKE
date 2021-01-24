# Micro:Bit Game - Snake
A simple snake game running on micro:bit chip.

## Game feature
The snake is intialized with length of *2*, where its body coordinates are *(2, 3), (2, 3)* and running on a *5 x 5* LED map on the microbit chip. The food location is randomly assigned to the coordinate which is not a part of snake's body. The game is over when the snake hits the wall *(out of bounce)* or crash with its own body.

#### LED brightness on items [0, 9]:
0 stands for LED off.
- Snake's body: 9
- food: 5

#### Movement:
- Button A: LEFT TURN
- Button B: RIGHT TURN

## Demo video
{%youtube 5GJvIAlbfU0 %}


## How it works
This project is done by python. You can flash the code to the chip either from [web](https://python.microbit.org/v/2) or via pip package `uflash`.

### Flash the code (offline, pip)

To install needed package:
`pip install uflash`

To flash the python script to the chip
`uflash snake.py`

### Implementation
#### Libraries
```=python
import time
import random
from collections import namedtuple

from microbit import display, button_a, button_b, Image

```
- The `microbit` library is exclusively for microbit chip, which is used for control of display (LED) and buttons (`button_a`, `button_b`), other than that, `Image` class is for creating a object as input of display function.
- `random` library is used for randomly generate new food on map
- `time` is used for game clock and game frame (refresh rate on snake's movement).
- `collections`' `namedtuple` is used for improvement of *tuple* readability.

#### GAME SETTINGS

```=python
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
```
- `COL_LEN` - length of LED columns, in microbit, it is *5*.
- `MAP_LEN` - squared of `COL_LEN`. Althought we can treat LED map as *5 x 5* matrix, but in this project, I will transform 2-D array to 1-D array representation, in which, length of *25*.
- `point` - named tuple, we can now refer object's *0-index* as *x*, and *1-index* as *y*.
- `LIGHT`, `MEDIUM`, `DENSE` - Opagueness of the LED light in a point. Scale from *1* to *9*.
- `CLOCK` - also treat as game period, is *2 ms*.
- `FRAME` - *50* frames, in every *50* frames, snake moves *1* step.

#### Game object
Game manager that keeps the game's status.
```=python
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
```

#### Snake object
Snake object that describe the snake's body and current moving direction.
```=python
class Snake:
    def __init__(self):
        self.body = [point(2, 2), point(2, 3)]
        self.direction = 0
```

- direction - stores current snake's head moving direction.
- body - stores snake's body (list of coordinates)

#### Generate image function
Once we have our map, we can ask micro bit LED to render current map.
```=python
def generate_image(current_map):
    graph = "".join(current_map)
    return Image(":".join([graph[i: i + COL_LEN] for i in range(0, MAP_LEN, COL_LEN)]))
```
This function return `Image` object which can then be called as input of `display` method.

#### Game logics
```=python
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

```

1. The snake game logic starts with instantiate both `game` and `snake` objects. Now we have our init game status (map status and food position).
2. We have a huge `while` block to keep our game running endlessly. In every loop, there is a 2 ms delay as game's frame period.
3. Inside each loop, we have to keep tracking chip's A and B keys, determine the direction of the snake head movement. Press A for a left turn, whereas press B for a right turn.
4. As the game going in the frame, we need to render the snake's body and food in the map. After that, `display` is called to actually show the LED output to the chip.
5. There is a `if-clause` to check if the current's game frame is *50*, so the snake can move its head to next position. By doing so, it means in our game, the snake moves at a speed of *1 step/s*, obtained by *2 ms  50 frames*
6. Before we are deciding on where the snake head is moving, we roll the snake body array by *1* ahead. For example 2nd position of the body will be overwritten to 1st position's value, the 3rd will be overwritten to the 2nd postion's value and so on.
7. Unlike 6. snake head has no previous body position to allocate to, so we have to determine the current direction of snake movement, and asssign the new value to snake head.
    - 0: UP - (x, y) to (x, y - 1)
    - 1: LEFT - (x, y) to (x - 1, y)
    - 2: DOWN - (x, y) to (x, y + 1)
    - 3: RIGHT - (x, y) to (x + 1, y)
8. Inside every direction movement, we will have another `if-clause` to check whether the snake is hitting the wall *(0 =< x < 5, 0 =< y < 5)*, and head is not hitting its own body *(`newhead` position should not already in part of its body)*.
9. Now we almost have all the logics done, but hey! What about the snake's food? Don't worry, we can say that the snake has gotten its food when `new_head`'s position is `game.food`'s position. After that to to increase the snake length by *1*, we simply keep the last snake tail position and append it to the snake body.
10. Remenber to call `game.generate_food` function to let the game generate new food position, and keep in mind new food position should not be any position that snake body already pocessesed.
11. Boom! Now the game is done. Enjoy.

## Contributor
Chai-Shi, Chang