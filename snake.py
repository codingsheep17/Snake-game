import pygame as py
import random
import sys
import os

# Initialize Pygame
py.init()

# Screen settings
screen_width = 450
screen_height = 400
screen = py.display.set_mode((screen_width, screen_height))
py.display.set_caption("Snake Game")

# Background music initiator (after initializing the display)
py.mixer.init()
py.mixer.music.load("bgsound.mp3")
py.mixer.music.play()

# Icon handling
try:
    icon_img = py.image.load("SNAKE GAME.png")  # Ensure the file name matches exactly
    py.display.set_icon(icon_img)
except FileNotFoundError:
    print("Error: 'SNAKE GAME.png' not found. Ensure it's in the same directory as your script.")

# Colors
white = (255, 255, 255)
Red = (255, 0, 0)
Black = (0, 0, 0)
Green = (0, 100, 0)
Cyan = (0, 255, 255)
Gray = (100, 100, 100)
pink = (255, 105, 180)

# Background image setting
bgimg = py.image.load("download.jfif")
bgimg = py.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Snake body
def plot_snake(screen, color, snk_list, snake_size):
    for x, y in snk_list:
        py.draw.rect(screen, color, [x, y, snake_size, snake_size])

# Screen text
def screen_text(text, color, x, y):
    text_screen = font.render(text, True, color)
    screen.blit(text_screen, [x, y])

# Score font text for screen
font = py.font.SysFont(None, 26)

# FPS system
fps = 60
clock = py.time.Clock()

# Welcome screen
def welcome():
    while True:
        screen.fill(Gray)
        screen.blit(bgimg, (0, 0))
        screen_text("Welcome to snake game", pink, 120, 300)
        screen_text("Press Enter to Play", pink, 140, 280)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()  # Quit Pygame properly when closing the game window
                sys.exit()  # Exit the program
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    game_loop()  # Start the game loop after the welcome screen
        py.display.update()
        clock.tick(fps)

# Game loop
def game_loop():
    # Snake variables
    snake_size = 20
    snake_x = 45
    snake_y = 55
    # Food
    food_size = snake_size
    food_x = random.randint(20, (screen_width - food_size))
    food_y = random.randint(20, (screen_height - food_size))
    # Score value dealing
    score = 0
    # Adding velocity of the snake
    velocity_x = 0
    velocity_y = 0
    # Events 
    exit_game = False
    game_over = False
    # If the score file doesn't exist
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    # High score reading and storing
    with open("hiscore.txt", 'r') as f:
        high_score = f.read()
    # Snake length increment
    snk_list = []
    snake_length = 1
    while True:
        # Game over handling
        if game_over:
            screen.fill(Gray)
            screen_text("Game over Press enter to continue", Black, 80, 170)
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()  # Exit immediately after quitting Pygame
                # If the user wants to restart the game after collision
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RETURN:
                        return  # End the game loop and go back to the welcome screen
        else:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()  # Exit immediately after quitting Pygame
                    break
                # Keys handling for snake
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RIGHT:
                        velocity_x = 3
                        velocity_y = 0
                    if event.key == py.K_LEFT:
                        velocity_x = -3
                        velocity_y = 0
                    if event.key == py.K_UP:
                        velocity_y = -3
                        velocity_x = 0
                    if event.key == py.K_DOWN:
                        velocity_y = 3
                        velocity_x = 0
                    if event.key == py.K_q:  # Cheat code
                        score += 5
            screen.fill(Black)
            # Snake velocities
            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                py.mixer.Sound("beep.mp3").play()
                score += 10
                screen_text("score " + str(score) + "               High score" + str(high_score), Cyan, 5, 5)
                snake_length += 5
                if score > int(high_score):
                    high_score = score
                    with open("hiscore.txt", 'w') as w:
                        w.write(str(high_score))
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
            # Dealing with wall collision
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                py.mixer.music.load("game_over.mp3")
                py.mixer.music.play()
            # Snake head
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            if len(snk_list) > snake_length:
                del snk_list[0]
            # Game over handling
            if head in snk_list[:-1]:
                game_over = True
                py.mixer.music.load("game_over.mp3")
                py.mixer.music.play()
            # Creating snake
            plot_snake(screen, Green, snk_list, snake_size)
            # Food attributes
            py.draw.rect(screen, Red, [food_x, food_y, 10, 10])
            # Score board
            screen_text("score: " + str(score) + "              High score: " + str(high_score), Cyan, 5, 5)
        # Display update after each change
        py.display.update()
        py.display.flip()
        # FPS dealing
        clock.tick(fps)

    # Quit Pygame properly (this line is just to make sure we don't call it prematurely)
    py.quit()
    sys.exit()

# Start the game
welcome()
