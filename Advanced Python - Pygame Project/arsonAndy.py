import pygame
import math
import random
from pygame.locals import *

pygame.init()
#Basic Variables
screen_width = 800
screen_height = 600
clock = pygame.time.Clock()
fps = 60
start_time = pygame.time.get_ticks()
total_time = 600000
margin = 50
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arson Andy')

#Game/text variables
current_level = 1
score = 0
font_title = pygame.font.SysFont('Algerian', 100)
font_title_small = pygame.font.SysFont('Algerian', 30)
font = pygame.font.SysFont('Constantia', 30)
TITLE_SCREEN = 0
PLAYING = 1
GAME_OVER = 2
VICTORY_SCREEN = 3
game_state = TITLE_SCREEN
TILE_SIZE = 25

#UI colors
bg = (44, 42, 42)
white = (255, 255, 255)
steel = (227, 217, 217)
red = (198, 18, 18)
black = (0, 0, 0)

def parse_layout(layout_data):
    objects = []
    for y, row in enumerate(layout_data):
        for x, tile in enumerate(row):
            x_pos = x * TILE_SIZE
            y_pos = y * TILE_SIZE + margin
            if tile == '=':
                objects.append(building(x_pos, y_pos))
            elif tile in '0123':
                objects.append(road(x_pos, y_pos, int(tile)))
            elif tile == '*':
                objects.append(grass(x_pos, y_pos))
            elif tile == ' ':
                continue  #Empty space
    return objects

def parse_objects(object_data):
    start_position = None
    gas_cans = []
    for y, row in enumerate(object_data):
        for x, char in enumerate(row):
            x_pos = x * TILE_SIZE
            y_pos = y * TILE_SIZE + margin
            if char == '%':
                start_position = (x_pos, y_pos)
            elif char == '$':
                gas_cans.append(gasCan(x_pos, y_pos))
    if start_position is None:
        raise ValueError("Start position '%' not found in object data.")
    return start_position, gas_cans

def read_level_layout(current_level):
    path = f'levels/lvl{current_level}.txt'
    with open(path, 'r') as file:
        lines = [line.rstrip() for line in file]
        max_length = max(len(line) for line in lines)
        return [line.ljust(max_length) for line in lines]

def read_level_objects(current_level):
    path = f'levels/lvl{current_level}obj.txt'
    with open(path, 'r') as file:
        lines = [line.rstrip() for line in file]
        max_length = max(len(line) for line in lines)
        return [line.ljust(max_length) for line in lines]

def load_current_level(current_level):
    global level_objects, current_buildings, gas_cans, p1, mazda

    layout_data = read_level_layout(current_level)
    object_data = read_level_objects(current_level)
    
    #Parse layout to create level objects
    level_objects = parse_layout(layout_data)
    current_buildings = [obj for obj in level_objects if isinstance(obj, building)]
    
    #Parse object data to set up additional game objects
    start_position, gas_cans = parse_objects(object_data)
    if start_position is not None:
        p1 = player(*start_position)
        mazda = car(*start_position)  #Initialize the car at the player's starting position
    else:
        raise ValueError("No start position found in the level object data.")

    return start_position

def draw_board():
    screen.fill(bg)
    pygame.draw.rect(screen, steel, (0, 0, screen_width, margin))
    pygame.draw.rect(screen, red, (0, 0, screen_width, margin), width=5)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def draw_title():
    screen.fill(bg)
    draw_text('ARSON ANDY', font_title, red, 100, 75)
    draw_text("Andy has grown tired of this world, take his shitty mazda", font, steel, 30, 225)
    draw_text("and burn down the entire town before time runs out!", font, steel, 60, 275)
    draw_text('Press SPACE to use flamethrower', font, steel, 200, 350)
    draw_text('Press arrow keys or WASD to move', font, steel, 200, 400)
    draw_text('Press F to enter/exit vehicle', font, steel, 200, 450)
    draw_text('Press SPACE to start', font_title_small, steel, 225, 525)

def draw_game_over():
    screen.fill(bg)
    draw_text('GAME OVER', font_title, red, screen_width // 2 - 250, screen_height // 2 - 100)
    draw_text('Press SPACE to play again', font_title_small, steel, screen_width // 2 - 190, screen_height // 2)
    draw_text('Press ESC to quit', font_title_small, steel, screen_width // 2 - 120, screen_height // 2 + 50)

def draw_victory():
    screen.fill(bg)
    draw_text('YOU WIN!', font_title, red, 200, 100)
    draw_text('I never much liked this place anyways!', font_title_small, steel, 100, 300)
    draw_text('Press SPACE to play again', font_title_small, steel, screen_width // 2 - 190, screen_height // 2 + 50)
    draw_text('Press ESC to quit', font_title_small, steel, screen_width // 2 - 120, screen_height // 2 + 100)

def draw_objects(screen, objects):
    for obj in objects:
        obj.draw(screen)

def all_buildings_burned(buildings):
    return all(building.state == 'burned' for building in buildings)

def check_collision(rect, buildings):
    for building in buildings:
        if building.has_collision() and rect.colliderect(building.rect):
            return True
    return False

class road:
    def __init__(self, x, y, rotation):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.rotation = rotation
        #Load and rotate the road image based on rotation
        self.image = pygame.image.load('assets/road.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, rotation * 90)
        self.image = self.scale_image(self.image, 1.2)

    def scale_image(self, image, scale):
        width, height = image.get_size()
        return pygame.transform.scale(image, (int(width * scale), int(height * scale)))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class grass():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grassNum = random.randint(0,2)
        self.image = pygame.image.load(f'assets/grass{self.grassNum}.png').convert_alpha()
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class car():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.angle = 0
        self.image = pygame.image.load('assets/mazda.png').convert_alpha()
        #Scaling asset to half size
        original_width, original_height = self.image.get_size()
        scaled_width, scaled_height = original_width // 2, original_height // 2
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        self.original_image = self.image
        self.rect = Rect(self.x, self.y, 26, 46)

    def move(self, buildings, gas_cans):
        key = pygame.key.get_pressed()
        temp_rect = self.rect.copy()

        if (key[pygame.K_UP] or key[pygame.K_w]) and self.rect.top > margin:
            self.angle = 0
            temp_rect.move_ip(0, -1 * self.speed)
        elif (key[pygame.K_DOWN] or key[pygame.K_s]) and self.rect.bottom < screen_height:
            self.angle = 180
            temp_rect.move_ip(0, self.speed)
        elif (key[pygame.K_LEFT] or key[pygame.K_a]) and self.rect.left > 0:
            self.angle = 90
            temp_rect.move_ip(-1 * self.speed, 0)
        elif (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.rect.right < screen_width:
            self.angle = -90
            temp_rect.move_ip(self.speed, 0)
        
        if not check_collision(temp_rect, buildings):
            self.rect = temp_rect
            self.check_gas_can_collision(gas_cans, p1)

    def check_gas_can_collision(self, gas_cans, player):
        for can in gas_cans:
            if self.rect.colliderect(can.rect):
                gas_cans.remove(can)
                player.fuel = 100

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

class gasCan():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE*2, TILE_SIZE*2)
        self.image = pygame.image.load('assets/gas_can.png').convert_alpha()
        self.image = self.scale_image(self.image, 0.5)

    def scale_image(self, image, scale):
        width, height = image.get_size()
        return pygame.transform.scale(image, (int(width * scale), int(height * scale)))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.angle = 0
        self.fuel = 100
        self.driving = True
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.flame_image = pygame.image.load('assets/player_flamethrower.png').convert_alpha()
        self.rect = Rect(self.x, self.y, 7, 12)
        self.last_direction = 'right'
        self.is_flaming = False

    def move(self, buildings, gas_cans):
        key = pygame.key.get_pressed()
        temp_rect = self.rect.copy()

        if (key[pygame.K_UP] or key[pygame.K_w]) and self.rect.top > margin:
            self.angle = 0
            temp_rect.move_ip(0, -1 * self.speed)
        elif (key[pygame.K_DOWN] or key[pygame.K_s]) and self.rect.bottom < screen_height:
            self.angle = 180
            temp_rect.move_ip(0, self.speed)
        elif (key[pygame.K_LEFT] or key[pygame.K_a]) and self.rect.left > 0:
            self.angle = 90
            temp_rect.move_ip(-1 * self.speed, 0)
        elif (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.rect.right < screen_width:
            self.angle = -90
            temp_rect.move_ip(self.speed, 0)
        
        if not check_collision(temp_rect, buildings):
            self.rect = temp_rect
            self.check_gas_can_collision(gas_cans)

    def check_gas_can_collision(self, gas_cans):
        for can in gas_cans:
            if self.rect.colliderect(can.rect):
                gas_cans.remove(can)
                self.fuel = 100

    def enter_car(self, car):
        self.driving = True
        self.rect = car.rect

    def exit_car(self, car):
        self.driving = False
        self.rect = pygame.Rect(car.rect.x, car.rect.y, self.rect.width, self.rect.height)

    def use_flamethrower(self, car, buildings, screen):
        #Check if the player is close enough to the car and has enough fuel
        player_pos = pygame.Vector2(self.rect.center)
        car_pos = pygame.Vector2(car.rect.center)
        distance_to_car = player_pos.distance_to(car_pos)

        if distance_to_car <= 200 and self.fuel > 0:
            self.is_flaming = True
            #Deplete fuel over time (1 fuel per 0.5 seconds)
            self.fuel -= 0.1  # Adjust as needed for balance

            #Define the flamethrower range and size
            flamethrower_length = 75
            flamethrower_width = 10

            #Calculate the direction vector based on the player's facing direction
            if self.angle == 0:  # Facing up
                direction = pygame.Vector2(0, -1)
            elif self.angle == 180:  # Facing down
                direction = pygame.Vector2(0, 1)
            elif self.angle == 90:  # Facing left
                direction = pygame.Vector2(-1, 0)
            elif self.angle == -90:  # Facing right
                direction = pygame.Vector2(1, 0)
            #elif self.angle == 45:  # Facing up-right
                #direction = pygame.Vector2(1, -1).normalize()
            #elif self.angle == 135:  # Facing down-right
                #direction = pygame.Vector2(1, 1).normalize()
            #elif self.angle == -135:  # Facing down-left
                #direction = pygame.Vector2(-1, 1).normalize()
            #elif self.angle == -45:  # Facing up-left
                #direction = pygame.Vector2(-1, -1).normalize()
            else:
                direction = pygame.Vector2(0, 0)

            # Calculate the end position of the flamethrower effect
            end_pos = player_pos + direction * flamethrower_length

            #Draw the flamethrower effect as a line
            pygame.draw.line(screen, (255, 69, 0), player_pos, end_pos, flamethrower_width)

            #Detect and start burning buildings in the flamethrower's path
            for building in buildings:
                #Create a rect for the line collision detection
                flamethrower_rect = pygame.Rect(player_pos.x, player_pos.y, flamethrower_width, flamethrower_length)
                flamethrower_rect.center = player_pos + direction * (flamethrower_length / 2)
                flamethrower_rect.size = (abs(end_pos.x - player_pos.x), flamethrower_width) if direction.x != 0 else (flamethrower_width, abs(end_pos.y - player_pos.y))
                flamethrower_rect.size = flamethrower_rect.size or (flamethrower_length, flamethrower_width)

                if flamethrower_rect.colliderect(building.rect):
                    building.start_burning()
        else:
            self.is_flaming = False


    def draw(self, screen):
        if not self.driving:
            if self.is_flaming:
                image = self.flame_image
            else:
                image = self.image
            rotated_image = pygame.transform.rotate(image, self.angle)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, new_rect.topleft)


class building():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE * 2, TILE_SIZE * 2)
        self.state = 'intact'  # 'intact', 'burning', 'burned'
        self.burn_start_time = None
        self.last_flip_time = pygame.time.get_ticks()
        self.flipped = False

        self.intact_image = pygame.image.load('assets/building.png').convert_alpha()
        self.burning_image = pygame.image.load('assets/burning_building.png').convert_alpha()
        self.burned_image = pygame.image.load('assets/burned_building.png').convert_alpha()
        self.burned_image = self.scale_image(self.burned_image, 0.5)

    def scale_image(self, image, scale):
        width, height = image.get_size()
        return pygame.transform.scale(image, (int(width * scale), int(height * scale)))

    def start_burning(self):
        if self.state == 'intact':
            self.state = 'burning'
            self.burn_start_time = pygame.time.get_ticks()
            global score
            score += 100

    def update(self):
        if self.state == 'burning':
            elapsed_time = pygame.time.get_ticks() - self.burn_start_time
            if elapsed_time >= 3000:
                self.state = 'burned'
            #Check to see if it's time to flip the image
            current_time = pygame.time.get_ticks()
            if current_time - self.last_flip_time >= 500:  # 0.5 seconds
                self.burning_image = pygame.transform.flip(self.burning_image, True, False)
                self.last_flip_time = current_time

    def draw(self, screen):
        if self.state == 'intact':
            screen.blit(self.intact_image, self.rect.topleft)
        elif self.state == 'burning':
            screen.blit(self.burning_image, self.rect.topleft)
        elif self.state == 'burned':
            screen.blit(self.burned_image, self.rect.topleft)

    def has_collision(self):
        return self.state != 'burned'

#Initialize car and player
mazda = car(0, 0)
p1 = player(0, 0)

run = True
while run:
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, total_time - elapsed_time)
    minutes = remaining_time // 60000
    seconds = (remaining_time % 60000) // 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if p1.driving:
                    p1.exit_car(mazda)
                else:
                    player_pos = pygame.Vector2(p1.rect.center)
                    car_pos = pygame.Vector2(mazda.rect.center)
                    distance = player_pos.distance_to(car_pos)
                    if distance <= 25:
                        p1.enter_car(mazda)
            if event.key == pygame.K_SPACE:
                if game_state == TITLE_SCREEN:
                    game_state = PLAYING
                    start_time = pygame.time.get_ticks()
                    start_position = load_current_level(current_level)
                    p1 = player(*start_position)
                    mazda = car(*start_position)
                elif game_state == GAME_OVER:
                    game_state = PLAYING
                    score = 0
                    p1.fuel = 100
                    start_position = load_current_level(current_level)
                    p1 = player(*start_position)
                    mazda = car(*start_position)
                    start_time = pygame.time.get_ticks()
                elif game_state == PLAYING and not p1.driving:  #Use flamethrower when space is pressed
                    p1.is_flaming = True
                elif game_state == VICTORY_SCREEN:
                    game_state = PLAYING
                    score = 0
                    current_level = 1
                    p1.fuel = 100
                    start_position = load_current_level(current_level)
                    p1 = player(*start_position)
                    mazda = car(*start_position)  # Update the car's position
                    start_time = pygame.time.get_ticks()
            if event.key == pygame.K_ESCAPE:
                if game_state == GAME_OVER or game_state == VICTORY_SCREEN:
                    run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE: #Stop the flamethrower when the space key is released
                p1.is_flaming = False

    if game_state == TITLE_SCREEN:
        draw_title()
    elif game_state == PLAYING:
        if remaining_time <= 0:
            game_state = GAME_OVER
        draw_board()
        draw_objects(screen, level_objects)
        for obj in level_objects:
            if isinstance(obj, building):
                obj.update()  #Update building state
            obj.draw(screen)
        if all_buildings_burned(current_buildings):
            current_level += 1
            if current_level > 3:
                game_state = VICTORY_SCREEN
            else:
                start_position = load_current_level(current_level)
                p1 = player(*start_position)
                mazda = car(*start_position)

        for can in gas_cans:
            can.draw(screen)

        draw_text('ARSON ANDY', font_title_small, black, 10, 10)
        draw_text('SCORE: ' + str(score), font_title_small, black, (screen_width - 210), 10)
        draw_text('FUEL: ' + str(round(p1.fuel, 1)), font_title_small, black, 225, 10)
        draw_text(f'TIME: {minutes:01}:{seconds:02}', font_title_small, black, 400, 10)
        
        p1.move(current_buildings, gas_cans)
        p1.draw(screen)

        if p1.driving:
            mazda.move(current_buildings, gas_cans)
        elif p1.is_flaming:
            p1.use_flamethrower(mazda, current_buildings, screen)

        # Draw a line between the car and the player if within flamethrower range
        mazda.draw(screen)
        player_pos = pygame.Vector2(p1.rect.center)
        car_pos = pygame.Vector2(mazda.rect.center)
        distance = player_pos.distance_to(car_pos)
        if distance <= 200 and not p1.driving:
            pygame.draw.line(screen, black, player_pos, car_pos, 2)

    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == VICTORY_SCREEN:
        draw_victory()

    pygame.display.update()
    clock.tick(fps)
pygame.quit()
