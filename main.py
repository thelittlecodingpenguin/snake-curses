import curses
import random
import os
import pickle
import pprint
import sys
import time

curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
curses.start_color()
curses.curs_set(0)
curses.mousemask(1)
win.nodelay(1)
scores = []
secs = 0

CRED = '\33[31m'
CGREEN = '\33[32m'
CYELLOW = '\33[33m'
CBLUE = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE = '\33[36m'
CWHITE = '\33[37m'


def prints(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)


def collision(guy, fruit) -> False or True:
    counter = 0
    while counter < len(guy):
        if guy[counter] == fruit:
            return True
        counter += 1
    return False


prints("Press the up key to continue 🐍")
time.sleep(2)
while True:
    ky = win.getch()
    if ky == curses.KEY_UP:
        break
    else:
        continue

running = True
curses.start_color()

if curses.has_colors() == True:
    curses.use_default_colors()
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)

ESC = 27
keys = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]

win.border(0)
while running:
    snake = [(4, 10), (4, 9), (4, 8)]
    food = (10, 20)

    fruits = [
        "🍇", "🍈", "🍉", "🍊", "🍌", "🍍", "🍎", "🍏", "🍑", "🍒", "🍓", "🍅", "🍆", "🌽",
        "🍄", "🌰", "🥥", "🥑", "🥒", "🍋", "🥭"
    ]

    win.addch(food[0], food[1], random.choice(fruits))
    score = 0
    try:
        highscore = pkl = open("score.pkl", "rb")
        score = pickle.load(pkl)
        int(pprint.pprint(highscore))
        pkl.close()
        saved = True
    except:
        highscore = 0
        saved = False

    key = curses.KEY_DOWN

    while key != ESC:
        win.refresh()
        win.addstr(0, 2, 'Score: ' + str(score) + ' ', curses.color_pair(1))
        win.addstr(0, 13, "Highscore: " + str(highscore) + " ",
                   curses.color_pair(2))
        if score > highscore:
            if saved != True:
                highscore = score
            else:
                score = 0
        win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)

        prev_key = key
        event = win.getch()
        key = event if event != -1 else prev_key

        if key not in keys:
            key = prev_key

        y = snake[0][0]
        x = snake[0][1]

        # Check for key presses
        if key == curses.KEY_DOWN:
            y += 1
            #source = audio.play_file("snakehit2.mp3")
            #source.paused = not source.paused
        elif key == curses.KEY_UP:
            y -= 1
            #source = audio.play_file("snakehit2.mp3")
            #source.paused = not source.paused
        elif key == curses.KEY_LEFT:
            x -= 1
            #source = audio.play_file("snakehit2.mp3")
            #source.paused = not source.paused
        elif key == curses.KEY_RIGHT:
            x += 1
            #source = audio.play_file("snakehit2.mp3")
            #source.paused = not source.paused

        snake.insert(0, (y, x))
        # Check the arena boundary collision
        if y == 0:
            break
        if y == 19:
            break
        if x == 0:
            break
        if x == 59:
            break

        # Check for self collision
        elif snake[0] in snake[1:]:
            break

        # Check the food collision
        elif collision(snake, food) == True:
            score += 1
            food = ()
            while food == ():
                food = (random.randint(1, 18), random.randint(1, 58))
                if food in snake:
                    food = ()
                win.refresh()
            win.addch(food[0], food[1], random.choice(fruits))
            win.refresh()
        else:
            last = snake.pop()
            win.addch(last[0], last[1], ' ')
        win.addch(snake[0][0], snake[0][1], '•', curses.COLOR_BLUE)
        time.sleep(1)
        secs += 1

    curses.endwin()

    os.system("clear")
    prints("You died ")
    prints(f"Final score = {score}")
    prints(f" Final highscore = {highscore}")
    output = open("score.pkl", "wb")
    pickle.dump(highscore, output)
    output.close()
    rscore = score

    again = str(input(" \nPlay again? (y/n)\n>>> ")).lower().strip()
    if again != "y":
        break
    else:
        os.system("clear")
        highscore = rscore
        score = 0
        curses.endwin()
        win = curses.newwin(20, 60, 0, 0)
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        win.border(0)
        win.nodelay(1)
        continue
