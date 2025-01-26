import curses
import pyfiglet
import time
import random

def userInputMain(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow text
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Cyan text
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Green text
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)     # Red text

    # Disable cursor and clear the screen
    curses.curs_set(0)
    stdscr.clear()

    def safe_addstr(y, x, text, width, color_pair=0):
        """Safely add text within the terminal boundaries."""
        if 0 <= y < height and 0 <= x < width:
            stdscr.addstr(y, x, text[:width - x], curses.color_pair(color_pair))

    # Get screen dimensions
    height, width = stdscr.getmaxyx()

    if height < 20 or width < 60:
        stdscr.addstr(0, 0, "Please resize your terminal (at least 20x60) and restart the program.", curses.color_pair(4))
        stdscr.refresh()
        stdscr.getch()
        return

    # Customize font size with pyfiglet fonts
    title_art = pyfiglet.figlet_format("EP SQUAD", font="standard")
    subtitle_art = pyfiglet.figlet_format("Physics Simulation", font="standard")
    prompt = "Please enter your name and press ENTER:"

    # Display the ASCII art for the title and subtitle
    title_lines = title_art.split("\n")
    subtitle_lines = subtitle_art.split("\n")

    start_y = height // 4 - len(title_lines) // 2
    for i, line in enumerate(title_lines):
        start_x = width // 2 - len(line) // 2
        safe_addstr(start_y + i, max(0, start_x), line, width, color_pair=1)  # Title in yellow

    subtitle_start_y = start_y + len(title_lines) + 2
    for i, line in enumerate(subtitle_lines):
        start_x = width // 2 - len(line) // 2
        safe_addstr(subtitle_start_y + i, max(0, start_x), line, width, color_pair=2)  # Subtitle in cyan

    # Display the prompt for input
    input_start_y = subtitle_start_y + len(subtitle_lines) + 2
    safe_addstr(input_start_y, width // 2 - len(prompt) // 2, prompt, width, color_pair=3)  # Prompt in green

    # Enable input and display user input
    curses.curs_set(1)
    curses.echo()
    stdscr.refresh()
    user_input = stdscr.getstr(input_start_y + 2, width // 2 - 10, 20).decode('utf-8')
    curses.curs_set(0)

    # Clear the screen for the next page
    stdscr.clear()

    # Show a welcome message using the input
    welcome_message = f"Welcome, {user_input}!"
    welcome_art = pyfiglet.figlet_format(welcome_message, font="big")
    welcome_lines = welcome_art.split("\n")
    for i, line in enumerate(welcome_lines):
        start_x = width // 2 - len(line) // 2
        start_y = height // 2 - len(welcome_lines) // 2 + i
        safe_addstr(start_y, max(0, start_x), line, width, color_pair=1)  # Welcome message in yellow

    prompt = "Press ENTER to proceed to the next page."
    safe_addstr(height - 2, width // 2 - len(prompt) // 2, prompt, width, color_pair=3)  # Prompt in green
    stdscr.refresh()
    stdscr.getch()

    # Clear the screen for the description page
    stdscr.clear()

    # Add title and subtitles to the description page
    desc_title = pyfiglet.figlet_format("Simulation Overview", font="standard")
    subtitle1 = pyfiglet.figlet_format("Simulation 1: Gravity and Collision", font="mini")
    subtitle2 = pyfiglet.figlet_format("Simulation 2: Kinetic Theory of Diffusion", font="mini")
    description1 = "In this simulation, we show collisions under different conditions of elasticity and motion for different values of the gravitational constant."
    description2 = "In the second simulation, we explain diffusion with the Kinetic Theory of Gases."

    # Display title
    title_lines = desc_title.split("\n")
    desc_start_y = height // 6 - len(title_lines) // 2
    for i, line in enumerate(title_lines):
        start_x = width // 2 - len(line) // 2
        safe_addstr(desc_start_y + i, max(0, start_x), line, width, color_pair=1)  # Title in yellow

    # Display subtitle1 and its content
    subtitle1_lines = subtitle1.split("\n")
    sub1_start_y = desc_start_y + len(title_lines) + 2
    for i, line in enumerate(subtitle1_lines):
        start_x = width // 2 - len(line) // 2
        safe_addstr(sub1_start_y + i, max(0, start_x), line, width, color_pair=2)  # Subtitle in cyan

    safe_addstr(sub1_start_y + len(subtitle1_lines) + 1, width // 2 - len(description1) // 2, description1, width, color_pair=3)  # Description in green

    # Display subtitle2 and its content
    subtitle2_lines = subtitle2.split("\n")
    sub2_start_y = sub1_start_y + len(subtitle1_lines) + 4
    for i, line in enumerate(subtitle2_lines):
        start_x = width // 2 - len(line) // 2
        safe_addstr(sub2_start_y + i, max(0, start_x), line, width, color_pair=2)  # Subtitle in cyan

    safe_addstr(sub2_start_y + len(subtitle2_lines) + 1, width // 2 - len(description2) // 2, description2, width, color_pair=3)  # Description in green

    curses.echo()
    user_command = stdscr.getstr(height - 3, width // 2 - 10, 20).decode('utf-8')
    curses.curs_set(0)

    safe_addstr(height - 2, width // 2 - len("Press ENTER to exit.") // 2, "Press ENTER to exit.", width, color_pair=3)  # Exit prompt in green
    stdscr.refresh()
    stdscr.getch()

def gravity(stdscr):
    # Turn off cursor and enable keypad input
    curses.curs_set(0)
    
    # Get terminal dimensions
    height, width = stdscr.getmaxyx()

    # Ball properties
    x = 5  # Initial x position
    y = height // 2  # Start in the middle of the screen
    vx = 3  # Initial horizontal velocity (faster movement)
    vy = 0  # Initial vertical velocity
    g = 1  # Acceleration due to gravity
    dt = 0.05  # Smaller time step for faster updates

    # Set non-blocking input
    stdscr.nodelay(1)

    # Main loop
    while True:
        # Check for user input to stop the simulation
        key = stdscr.getch()
        if key != -1:
            break

        # Clear the screen
        stdscr.clear()

        # Update position
        x += vx * dt
        y += vy * dt

        # Update vertical velocity due to gravity
        vy += g * dt

        # Check for collisions with boundaries
        if x <= 0:
            x = 0
            vx = -vx  # Reverse horizontal velocity
        elif x >= width - 1:
            x = width - 1
            vx = -vx

        if y >= height - 1:
            y = height - 1
            vy = -vy  # Reverse vertical velocity (elastic collision)
        elif y <= 0:
            y = 0
            vy = -vy

        # Draw the ball
        stdscr.addch(int(round(y)), int(round(x)), 'O')

        # Refresh the screen
        stdscr.refresh()

        # Pause to control frame rate
        time.sleep(dt)



class Particle:
    def __init__(self, x, y, dx, dy=0, symbol='o'):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.symbol = symbol

def motion(shape, start, end, stdscr, color_pair, partition, wall_1, wall_3):
    height, width = stdscr.getmaxyx()
    for i in shape:
        i.y += i.dy
        i.x += i.dx

    for i in shape:
        # Reflect off top and bottom edges
        if i.y <= 1 or i.y >= height - 2:
            i.dy *= -1

        # Reflect off left and right edges
        if i.x <= start or i.x >= end - 1:
            i.dx *= -1

        # Reflect off wall_1 and wall_3 if partition is removed
        if not partition:
            for wall in (wall_1, wall_3):
                for wall_particle in wall:
                    if i.x == wall_particle.x and i.y == wall_particle.y:
                        i.dx *= -1

    # Draw particles
    for i in shape:
        if 1 <= i.y < height - 1 and start <= i.x < end:
            stdscr.addch(i.y, i.x, i.symbol, curses.color_pair(color_pair))

def random_box(start, end, n, gas, stdscr):
    height, width = stdscr.getmaxyx()
    box = [Particle(random.choice(range(start, end)), random.choice(range(1, height - 1)),
                    random.choice([-1, 1]), random.choice([-1, 1]), gas) for _ in range(n)]
    return box

def draw_ui(stdscr, box1_count, box2_count, speed, partition):
    height, width = stdscr.getmaxyx()
    # Draw the status bar at the top
    status_bar = f" Box 1: {box1_count} particles | Box 2: {box2_count} particles | Speed: {speed}m/s | Partition: {'ON' if partition else 'OFF'} "
    stdscr.addstr(0, 0, status_bar[:width - 1], curses.color_pair(3))
    # Draw the instructions at the bottom
    instructions = "Controls: [P] Toggle Partition | [+] Increase Speed | [-] Decrease Speed | [Any other key] Exit"
    stdscr.addstr(height - 1, 0, instructions[:width - 1], curses.A_REVERSE)


def diffusionMain(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    speed = 100  # Initial speed in milliseconds
    stdscr.timeout(speed)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Particles in box1
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Particles in box2
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # UI elements

    height, width = stdscr.getmaxyx()

    # Create boxes and partition
    box1_count = 50
    box2_count = 50
    box1 = random_box(0, width // 2, box1_count, 'o', stdscr)
    box2 = random_box((width // 2) + 2, width, box2_count, 'o', stdscr)

    wall_1 = [Particle((width // 2) + 1, i, 0, 0, '|') for i in range(1, 4 * (height // 10))]
    wall_2 = [Particle((width // 2) + 1, i, 0, 0, '|') for i in range(4 * (height // 10), 6 * (height // 10))]
    wall_3 = [Particle((width // 2) + 1, i, 0, 0, '|') for i in range(6 * (height // 10), height - 1)]

    global partition
    partition = True

    while True:
        # Clear the screen
        stdscr.clear()

        # Draw UI
        draw_ui(stdscr, len(box1), len(box2), speed, partition)

        # Animate particles
        if partition:
            motion(box1, 0, width // 2, stdscr, 1, partition, wall_1, wall_3)
            motion(box2, (width // 2) + 2, width, stdscr, 2, partition, wall_1, wall_3)
        else:
            motion(box1, 0, width, stdscr, 1, partition, wall_1, wall_3)
            motion(box2, 0, width, stdscr, 2, partition, wall_1, wall_3)

        # Draw partition if enabled
        if partition:
            for i in wall_2:
                stdscr.addch(i.y, i.x, i.symbol, curses.color_pair(3))
        
        # Always draw wall_1 and wall_3
        for i in wall_1:
            stdscr.addch(i.y, i.x, i.symbol, curses.color_pair(3))
        for i in wall_3:
            stdscr.addch(i.y, i.x, i.symbol, curses.color_pair(3))

        # Refresh the screen
        stdscr.refresh()

        # Handle user input
        key = stdscr.getch()
        if key == ord('p'):
            partition = not partition  # Toggle partition
        elif key == ord('+'):
            speed = max(10, speed - 10)  # Increase speed
            stdscr.timeout(speed)
        elif key == ord('-'):
            speed += 10  # Decrease speed
            stdscr.timeout(speed)
        elif key != -1:
            break  # Exit on any other key

        # Small delay for smooth animation
        time.sleep(0.05)

curses.wrapper(userInputMain)
curses.wrapper(gravity)
curses.wrapper(diffusionMain)
