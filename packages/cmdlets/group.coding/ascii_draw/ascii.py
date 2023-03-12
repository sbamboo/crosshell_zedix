import os
import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Get terminal size
    height, width = stdscr.getmaxyx()

    # Draw outer border
    stdscr.border()

    # Define drawing area dimensions
    drawing_area_height = height - 4
    drawing_area_width = width - 2

    # Draw character selector box
    character_selector_box = curses.newwin(drawing_area_height, 5, 2, 1)
    character_selector_box.box()
    character_selector_box.addstr(1, 2, "Characters")

    # Define character selector options
    characters = ['.', ':', ';', '"', '¤', '#', '@', '░', '▒', '▓', '█']

    # Draw character selector options
    for i, char in enumerate(characters):
        character_selector_box.addstr(i + 2, 2, char)

    # Set default current character
    current_character = characters[0]

    # Draw current character indicator
    stdscr.addstr(height - 2, 2, "Cur: " + current_character)

    # Draw drawing area
    drawing_area = curses.newwin(drawing_area_height, drawing_area_width, 2, 7)
    drawing_area.keypad(True)
    drawing_area.nodelay(True)

    # Set default drawing character
    drawing_character = current_character

    # Main loop
    while True:
        # Refresh screen
        stdscr.refresh()

        # Get mouse events
        try:
            _, mouse_x, mouse_y, _, _ = curses.getmouse()
        except curses.error:
            # Mouse events not supported
            pass

        # Check if mouse is in character selector box
        if 1 <= mouse_x <= 5 and 2 <= mouse_y <= drawing_area_height + 1:
            # Get selected character
            selected_index = mouse_y - 2
            current_character = characters[selected_index]

            # Update current character indicator
            stdscr.addstr(height - 2, 2, "Cur: " + current_character)

            # Set drawing character to selected character
            drawing_character = current_character

        # Check if mouse is in drawing area
        elif 7 <= mouse_x <= drawing_area_width + 6 and 2 <= mouse_y <= drawing_area_height + 1:
            # Get position in drawing area
            pos_x = mouse_x - 7
            pos_y = mouse_y - 2

            # Draw character at position
            drawing_area.addstr(pos_y, pos_x, drawing_character)

            # Save to file
            with open('drawing.txt', 'a') as f:
                f.write(f"{drawing_character} {pos_x} {pos_y}\n")

        # Handle keyboard input
        key = drawing_area.getch()
        if key == ord('q'):
            # Quit program
            break

    # End program
    curses.endwin()

if __name__ == '__main__':
    # Setup curses
    if os.name == 'nt':
        os.environ['TERM'] = 'xterm'
    curses.wrapper(main)
