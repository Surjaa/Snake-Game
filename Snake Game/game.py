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

# Game display dimensions
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
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
update_interval = 20000  # 20000 milliseconds (20 seconds)

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
        TextRect.center = ((dis_width / 2), (dis_height / 2))
        dis.blit(TextSurf, TextRect)

        pygame.draw.rect(dis, green, [150, 450, 100, 50])
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects("Play", smallText)
        textRect.center = ((150 + (100 / 2)), (450 + (25)))
        dis.blit(textSurf, textRect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
                    intro = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def gameLoop():
    global last_update_time
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = [[x1, y1]]
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
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > update_interval:
            create_obstacles()
            last_update_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
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
            pygame.draw.rect(dis, red, ob)  # Draw each obstacle
        our_snake(snake_block, snake_List)
        pygame.display.update()

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > length_of_snake:
            del snake_List[0]

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(eat_sound)
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            length_of_snake += 1

        for ob in obstacles:
            if ob.collidepoint(snake_Head[0] + snake_block // 2, snake_Head[1] + snake_block // 2):
                pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        clock.tick(snake_speed)

game_intro()
gameLoop()
