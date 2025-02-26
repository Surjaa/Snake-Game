import pygame
import random
import sys

pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Determine screen size dynamically or use fixed size for desktop
info = pygame.display.Info()
if sys.platform in ['win32', 'darwin']:  # Checks if the OS is Windows or MacOS
    dis_width = min(800, info.current_w)  # Caps the width at 800 for desktops
    dis_height = min(600, info.current_h)  # Caps the height at 600 for desktops
else:
    # Mobile and other platforms use breakpoints
    screen_width = info.current_w
    if screen_width <= 480:
        dis_width = 320
        dis_height = 480
    elif screen_width <= 640:
        dis_width = 481
        dis_height = 640
    elif screen_width <= 768:
        dis_width = 641
        dis_height = 768
    else:
        dis_width = 769
        dis_height = 1024

dis = pygame.display.set_mode((dis_width, dis_height), pygame.RESIZABLE)
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 25
snake_speed = 15

# Font settings
font_style = pygame.font.SysFont("bahnschrift", 25)

# Load sounds
eat_sound = pygame.mixer.Sound('eat.wav')
game_over_sound = pygame.mixer.Sound('gameover.wav')

# Load the food image
food_img = pygame.image.load('images/snake_food.png')
food_img = pygame.transform.scale(food_img, (snake_block, snake_block))

# Obstacle setup
num_obstacles = 5
obstacles = []
last_update_time = pygame.time.get_ticks()
update_interval = 20000


def create_obstacles():
    global obstacles
    obstacles.clear()
    for _ in range(num_obstacles):
        obstacle = pygame.Rect(random.randint(0, dis_width - 30), random.randint(0, dis_height - 30), 30, 30)
        while any(obstacle.colliderect(ob) for ob in obstacles):
            obstacle = pygame.Rect(random.randint(0, dis_width - 30), random.randint(0, dis_height - 30), 30, 30)
        obstacles.append(obstacle)


create_obstacles()


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.ellipse(dis, blue, [x[0], x[1], snake_block, snake_block])


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def game_intro():
    intro = True
    while intro:
        dis.fill(black)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Snake Game", largeText)
        TextRect.center = ((dis_width / 2), (dis_height / 3))
        dis.blit(TextSurf, TextRect)

        play_button = pygame.Rect(dis_width / 2 - 50, dis_height / 2, 100, 50)
        pygame.draw.rect(dis, green, play_button)
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects("Play", smallText)
        textRect.center = (play_button.centerx, play_button.centery)
        dis.blit(textSurf, textRect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse):
                    intro = False
            if event.type is pygame.QUIT:
                pygame.quit()
                sys.exit()

                
def place_food():
    global foodx, foody
    food_placed = False
    while not food_placed:
        foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
        food_rect = pygame.Rect(foodx, foody, snake_block, snake_block)
        food_placed = True
        for ob in obstacles:
            if ob.colliderect(food_rect):
                food_placed = False
                break


place_food()                


def gameLoop():
    global last_update_time
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_list = [[x1, y1]]
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
            elif event.type == pygame.FINGERDOWN:
                if event.x < 0.5:
                    if event.dx < 0:
                        x1_change = -snake_block
                        y1_change = 0
                    else:
                        x1_change = snake_block
                        y1_change = 0
                else:
                    if event.dy < 0:
                        y1_change = -snake_block
                        x1_change = 0
                    else:
                        y1_change = snake_block
                        x1_change = 0

        x1 += x1_change
        y1 += y1_change

        # Wrap the snake around the edges
        x1 %= dis_width
        y1 %= dis_height

        dis.fill(black)
        dis.blit(food_img, (foodx, foody))
        for ob in obstacles:
            pygame.draw.rect(dis, red, ob)
        our_snake(snake_block, snake_list)
        pygame.display.update()

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check collision with the snake itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            pygame.mixer.Sound.play(eat_sound)
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            length_of_snake += 1

        for ob in obstacles:
            if ob.collidepoint(snake_head[0] + snake_block // 2, snake_head[1] + snake_block // 2):
                pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        clock.tick(snake_speed)


game_intro()
gameLoop()
