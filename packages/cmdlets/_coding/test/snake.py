# This app is made to run under crosshell so crosshell specific functions will be used through out the project.

# [Imports]
import random
try:
    import curses
except:
    if IsWindows() == True:
        os.system("python3 -m pip install windows_curses")
    else:
        os.system("python3 -m pip install curses")
    import curses


# [Main Code]

# Main screen function
def main(stdscr):
    # Clear the screen
    stdscr.clear()
    # Define screen/window
    screenHeight = 30
    screenWidth = 90
    win = curses.newwin(screenHeight + 1, screenWidth + 1, 0, 0)
    win.border()
    win.keypad(True)
    win.timeout(100)

    # Implement the sname
    start_x = int(screenWidth / 4)
    start_y = int(screenHeight / 2)

    snake = [
        (start_y, start_x),
        (start_y, start_x - 1),
        (start_y, start_x - 2)
    ]

    # Define out starting movement direction
    direction = curses.KEY_RIGHT

    # Starting food
    food = (int(screenHeight/2), int(screenWidth/2))
    win.addch(food[0],food[1], "O")

    while True:

        # Define new head
        new_head = None

        if snake[0][0] in (0, screenHeight) or snake[0][1] in (0, screenWidth):
            curses.endwin()
            print("GAME OVER (CollideWithWall)")
            quit()
        elif snake[0] in snake[1:]:
            curses.endwin()
            print("GAME OVER (CollideWithBody)")
            print(food)
            quit()

        key = win.getch()
        if key == -1:
            direction = direction
        else:
            direction = key

        if key == ord('q'):
            break
        if direction == curses.KEY_RIGHT:
            new_head = (snake[0][0], snake[0][1] + 1)
        elif direction == curses.KEY_LEFT:
            new_head = (snake[0][0], snake[0][1] - 1)
        elif direction == curses.KEY_UP:
            new_head = (snake[0][0] - 1, snake[0][1])
        elif direction == curses.KEY_DOWN:
            new_head = (snake[0][0] + 1, snake[0][1])

        snake.insert(0, new_head)

        # Check if snake ate food
        if snake[0] == food[0]:
            food = None
            while food is None:
                new_food = (random.randint(1, screenHeight - 1), random.randint(1, screenWidth - 1))

                # check that the position is free (no snake)
                if new_food in snake:
                    new_food = None
                else:
                    food = new_food
            win.addch(food[0], food[1], "O")

        tail = snake.pop()
        win.addch(tail[0], tail[1], " ")

        win.addch(new_head[0], new_head[1], curses.ACS_BLOCK)


# Init the function with the curses wrapper
curses.wrapper(main)