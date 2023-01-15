import os
import sqlite3
import sys
import time
import pygame
import random
pygame.init()
pygame.font.init()

size = width, height = 1400, 700
WIDTH, HEIGHT = width, height
screen = pygame.display.set_mode(size)
map_width, map_height = 0, 0
programIcon = pygame.image.load('data/icon_4.png')
pygame.display.set_icon(programIcon)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def generate_level(level, level_n):
    global map_width, map_height
    global screen_color
    new_player, x, y = None, None, None
    color = (0, 0, 0)
    if level_n == 1:
        color = (244, 137, 113)
        screen_color = (0, 0, 0)
        # (55, 31, 28)
    elif level_n == 2:
        color = (170, 240, 209)
        screen_color = (0, 0, 0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'x':
                platforms.append(Platform((x, y), color))
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == 'p':
                Point((x, y))
            elif level[y][x] == 'c':
                Point((x, y))
                c_points.append(CPoint((x, y), 0))
            elif level[y][x] == 'd':
                Point((x, y))
                c_points.append(CPoint((x, y), 2))
            elif level[y][x] == 'r':
                Point((x, y))
                c_points.append(CPoint((x, y), 1))
            elif level[y][x] == 'l':
                Point((x, y))
                c_points.append(CPoint((x, y), -1))
            elif level[y][x] == 'u':
                Point((x, y))
                c_points.append(CPoint((x, y), -2))
            elif level[y][x] == 'e':
                enemies.append(Enemy(x, y, red_ghost_img))
            elif level[y][x] == 'n':
                enemies.append(Enemy(x, y, pink_ghost_img))
            elif level[y][x] == 'm':
                enemies.append(Enemy(x, y, blue_ghost_img))
            elif level[y][x] == 'y':
                enemies.append(Enemy(x, y, yellow_ghost_img))
            elif level[y][x] == 'b':
                BigPoint((x, y))

    map_width = 50 * len(level[0])
    map_height = 50 * len(level)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def add_to_database(level, score):
    con = sqlite3.connect("results_db.sqlite")
    cur = con.cursor()
    cur.execute(f'INSERT INTO results(level,score) VALUES({level}, {score})')
    con.commit()
    con.close()


def get_from_database():
    con = sqlite3.connect("results_db.sqlite")
    cur = con.cursor()
    data = cur.execute(f'SELECT score FROM results').fetchall()
    max_value = max(map(lambda x: int(*x), data))
    con.close()
    return max_value


font1 = pygame.font.Font(None, 50)
font2 = pygame.font.SysFont("centuryschoolbookполужирный", 150)


def draw_str(line, font=font1):
    return font.render(str(line), True, (219, 215, 210))


pacman_copy = load_image("pacman0_copy.png")
player_img = [load_image('pacman0.png'), load_image('pacman1.png')]
red_ghost_img = [load_image('red1.png'), load_image('red2.png'), load_image('red3.png'), load_image('red4.png')]
pink_ghost_img = [load_image('pink1.png'), load_image('pink2.png'), load_image('pink3.png'), load_image('pink4.png')]
blue_ghost_img = [load_image('blue1.png'), load_image('blue2.png'), load_image('blue3.png'), load_image('blue4.png')]
yellow_ghost_img = [load_image('yellow1.png'), load_image('yellow2.png'), load_image('yellow3.png'),
                    load_image('yellow4.png')]
ghost_food = load_image('ghost_food.png')
logo = load_image('logo_4.png')
level_1_img = load_image('level_1.png')
level_2_img = load_image('level_2.png')
new_game_img = load_image('new_game.png')
test_level_img = load_image('test_l.png')


def ghost_anim(x, y, group):
    global ghost_animation_counter
    if ghost_animation_counter == 99:
        ghost_animation_counter = 0
    screen.blit(group[ghost_animation_counter // 30], (x, y))
    ghost_animation_counter += 1


def animation(x, y):
    global animation_counter
    if animation_counter == 19:
        animation_counter = 0
    screen.blit(player_img[animation_counter // 10], (x, y))
    animation_counter += 1


def flip_animation(direction):
    if direction == 'right':
        player_img[0] = pacman_copy
    if direction == 'left':
        player_img[0] = pygame.transform.flip(pacman_copy, True, False)
    if direction == 'down':
        player_img[0] = pygame.transform.rotate(pacman_copy, -90)
    if direction == 'up':
        player_img[0] = pygame.transform.rotate(pacman_copy, 90)


def spin_anim():
    pygame.mixer.music.stop()
    death_sound.play()
    for i in range(100):
        idle_screen()
        for enemy in enemies:
            ghost_anim(enemy.rect.x, enemy.rect.y, enemy.group)
        if i % 10 == 0:
            player_img[0] = pygame.transform.rotate(player_img[0], 90)

        pygame.display.flip()
        clock.tick(FPS)


def idle_screen():
    screen.fill(screen_color)
    all_sprites.update()

    screen.blit(player_img[0], (player.rect.x, player.rect.y))
    screen.blit(draw_str("Level: "), (10, 10))
    screen.blit(draw_str(level_n), (125, 10))
    screen.blit(draw_str("Score: "), (10, 60))
    screen.blit(draw_str(score), (125, 62))
    screen.blit(draw_str("High score: "), (10, 110))
    screen.blit(draw_str(high_score), (10, 160))
    screen.blit(draw_str("Lives left: "), (10, 210))

    for i in range(lives):
        screen.blit(pacman_copy, (10 + i * 50, 260))


class Button:
    def __init__(self, x, y, name):
        self.image = name
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Platform(pygame.sprite.Sprite):

    def __init__(self, coords, color):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(coords[0] * 25, coords[1] * 25, 25, 25)
        self.rect.x = coords[0] * 25
        self.rect.y = coords[1] * 25
        self.color = color

    def update(self):
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, 25, 25))


class Point(pygame.sprite.Sprite):

    def __init__(self, coords):
        super().__init__(all_sprites, point_group)
        self.rect = pygame.Rect(coords[0] * 25, coords[1] * 25, 10, 10)
        self.rect.x = coords[0] * 25
        self.rect.y = coords[1] * 25

    def update(self):
        pygame.draw.circle(screen, (219, 215, 210), (self.rect.x + 5, self.rect.y + 5), 5)


class CPoint(pygame.sprite.Sprite):

    def __init__(self, coords, forbidden_d):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(coords[0] * 25, coords[1] * 25, 25, 25)
        self.rect.x = coords[0] * 25
        self.rect.y = coords[1] * 25
        self.f_direction = forbidden_d

    def update(self):
        # pygame.draw.rect(screen, pygame.Color("red"), (self.rect.x, self.rect.y, 25, 25))
        pass


class BigPoint(pygame.sprite.Sprite):

    def __init__(self, coords):
        super().__init__(all_sprites, big_point_group)
        self.rect = pygame.Rect(coords[0] * 25, coords[1] * 25, 25, 25)
        self.rect.x = coords[0] * 25
        self.rect.y = coords[1] * 25

    def update(self):
        pygame.draw.circle(screen, (219, 215, 210), (self.rect.x + 12, self.rect.y + 12), 12)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.rect = pygame.Rect(25 * pos_x, 25 * pos_y, 50, 50)

    def move(self, direction, distance):

        if direction == "right":
            self.rect = self.rect.move(distance, 0)
        elif direction == "left":
            self.rect = self.rect.move(distance, 0)
        elif direction == "down":
            self.rect = self.rect.move(0, distance)
        elif direction == "up":
            self.rect = self.rect.move(0, distance)

    def update(self):
        screen.blit(player_img[0], (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group):
        super().__init__()
        self.w = 50
        self.h = 50
        self.rect = pygame.Rect(pos_x * 25, pos_y * 25, self.w, self.h)
        self.group = group
        routes = [1, -1, 2, -2]
        self.route = routes[random.randint(0, 3)]
        self.rect.x = pos_x * 25
        self.rect.y = pos_y * 25
        self.turn = -1
        self.status = True

    def move(self, direction, distance):
        if direction == 1:
            self.rect = self.rect.move(distance, 0)
        elif direction == -1:
            self.rect = self.rect.move(distance, 0)
        elif direction == 2:
            self.rect = self.rect.move(0, distance)
        elif direction == -2:
            self.rect = self.rect.move(0, distance)

    def update(self):
        screen.blit(ghost_food, (self.rect.x, self.rect.y))


screen_rect = (0, 0, width, height)
GRAVITY = 1


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particle_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 30
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def null_f(n, flag):
    global animation_counter
    global ghost_animation_counter
    global ghost_color_counter
    global lives
    global keys_pressed
    global edible_ghosts
    global high_score
    global level_n
    animation_counter = 0
    ghost_animation_counter = 0
    ghost_color_counter = 0
    keys_pressed = 20
    lives = 3
    edible_ghosts = 0
    high_score = get_from_database()
    for i in all_sprites:
        i.kill()
    for i in player_group:
        i.kill()
    for i in point_group:
        i.kill()
    for i in big_point_group:
        i.kill()
    if n == 1:
        level_n = 2
    elif n == 2:
        level_n = 1
    platforms.clear()
    c_points.clear()
    enemies.clear()
    player_img[0] = pacman_copy
    if flag:
        return game(True)
    else:
        return end_screen()


intro_song = pygame.mixer.Sound('data/sounds/intro.mp3')
death_sound = pygame.mixer.Sound('data/sounds/death_sound_2.mp3')
pygame.mixer.music.set_volume(1)
FPS = 50
clock = pygame.time.Clock()
routes = [1, -1, 2, -2]
ghost_coordinates = [(675, 275), (900, 275), (675, 400), (900, 400)]
player_speed = 6
enemy_speed = 5
enemy_size = 50
player_size = 50
particle_group = pygame.sprite.Group()
pygame.display.set_caption('pacman')


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
point_group = pygame.sprite.Group()
big_point_group = pygame.sprite.Group()
platforms = []
c_points = []
enemies = []
animation_counter = 0
ghost_animation_counter = 0
ghost_color_counter = 0

score = 0
level_n = 1
screen_color = (0, 0, 0)
player = None
keys_pressed = 20
lives = 3
high_score = get_from_database()
edible_ghosts = 0


def game(difficulty):
    global edible_ghosts
    global lives
    global score
    global keys_pressed
    global player
    global level_n

    map_name = f"levels/level_{level_n}.txt"
    player, level_x, level_y = generate_level(load_level(map_name), level_n)
    idle_screen()
    for enemy in enemies:
        ghost_anim(enemy.rect.x, enemy.rect.y, enemy.group)
    pygame.display.flip()
    clock.tick(FPS)
    intro_song.play()
    time.sleep(5)
    while True:
        move_up = True
        move_down = True
        move_left = True
        move_right = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if difficulty:
                    add_to_database(level_n, score)
                terminate()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            keys_pressed = 0
            flip_animation("right")
            char = pygame.Rect(player.rect.x + player_speed, player.rect.y, player_size, player_size)
            for p in platforms:
                if char.colliderect(p):
                    move_right = False
                    break
            if move_right:
                player.move("right", player_speed)
        if keys[pygame.K_a]:
            keys_pressed = 0
            flip_animation("left")
            char = pygame.Rect(player.rect.x - player_speed, player.rect.y, player_size, player_size)
            for p in platforms:
                if char.colliderect(p):
                    move_left = False
                    break
            if move_left:
                player.move("left", -player_speed)
        if keys[pygame.K_w]:
            keys_pressed = 0
            flip_animation("up")
            char = pygame.Rect(player.rect.x, player.rect.y - player_speed, player_size, player_size)
            for p in platforms:
                if char.colliderect(p):
                    move_up = False
                    break
            if move_up:
                player.move("up", -player_speed)
        if keys[pygame.K_s]:
            keys_pressed = 0
            flip_animation("down")
            char = pygame.Rect(player.rect.x, player.rect.y + player_speed, player_size, player_size)
            for p in platforms:
                if char.colliderect(p):
                    move_down = False
                    break
            if move_down:
                player.move("down", player_speed)

        if pygame.sprite.spritecollide(player, point_group, True):
            score += 1
        if len(point_group) == 0:
            if difficulty:
                return null_f(level_n, True)
            elif not difficulty:
                return null_f(level_n, False)
        if pygame.sprite.spritecollide(player, big_point_group, True):
            edible_ghosts = 200
            for en in enemies:
                en.status = False

        for enemy in enemies:
            if edible_ghosts <= 0:
                for en in enemies:
                    en.status = True
            if player.rect.colliderect(enemy):
                if enemy.status and difficulty:
                    lives -= 1
                    keys_pressed = 20
                    spin_anim()
                    player_img[0] = pacman_copy
                    player.rect.x = 250
                    player.rect.y = 50
                    for i, en in enumerate(enemies):
                        en.rect.x, en.rect.y = ghost_coordinates[i]
                        en.status = True

                    if lives <= 0:
                        add_to_database(level_n, score)
                        return null_f(level_n, False)
                elif not enemy.status:
                    enemy.status = True
                    enemy.rect.x = 675
                    enemy.rect.y = 275
                    score += 20
            if enemy.route == 1:
                mob = pygame.Rect(enemy.rect.x + enemy_speed, enemy.rect.y, enemy_size, enemy_size)
                for p in platforms:
                    if mob.colliderect(p):
                        possible_r = routes[random.randint(0, 3)]
                        while possible_r == -1 or possible_r == 1:
                            possible_r = routes[random.randint(0, 3)]
                        enemy.route = possible_r
                        break
                else:
                    enemy.move(1, enemy_speed)
            if enemy.route == -1:
                mob = pygame.Rect(enemy.rect.x - enemy_speed, enemy.rect.y, enemy_size, enemy_size)
                for p in platforms:
                    if mob.colliderect(p):
                        possible_r = routes[random.randint(0, 3)]
                        while possible_r == 1 or possible_r == -1:
                            possible_r = routes[random.randint(0, 3)]
                        enemy.route = possible_r
                        break
                else:
                    enemy.move(-1, -enemy_speed)
            if enemy.route == 2:
                mob = pygame.Rect(enemy.rect.x, enemy.rect.y + enemy_speed, enemy_size, enemy_size)
                for p in platforms:
                    if mob.colliderect(p):
                        possible_r = routes[random.randint(0, 3)]
                        while possible_r == -2 or possible_r == 2:
                            possible_r = routes[random.randint(0, 3)]
                        enemy.route = possible_r
                        break
                else:
                    enemy.move(2, enemy_speed)
            if enemy.route == -2:
                mob = pygame.Rect(enemy.rect.x, enemy.rect.y - enemy_speed, enemy_size, enemy_size)
                for p in platforms:
                    if mob.colliderect(p):
                        possible_r = routes[random.randint(0, 3)]
                        while possible_r == 2 or possible_r == -2:
                            possible_r = routes[random.randint(0, 3)]
                        enemy.route = possible_r
                        break
                else:
                    enemy.move(-2, -enemy_speed)
            if enemy.turn <= 0:
                for c in c_points:
                    if enemy.rect.x == c.rect.x and enemy.rect.y == c.rect.y or \
                            enemy.rect.x + enemy_size == c.rect.x + 25 and enemy.rect.y == c.rect.y:
                        possible_r = routes[random.randint(0, 3)]
                        while possible_r == c.f_direction or possible_r == -enemy.route:
                            possible_r = routes[random.randint(0, 3)]
                        enemy.route = possible_r
                        enemy.turn = 50
            enemy.turn -= 5

        idle_screen()

        for i in range(lives):
            screen.blit(pacman_copy, (10 + i * 50, 260))

        for enemy in enemies:
            if enemy.status:
                ghost_anim(enemy.rect.x, enemy.rect.y, enemy.group)
            elif not enemy.status:
                enemy.update()

        if keys_pressed < 20:
            animation(player.rect.x, player.rect.y)

        if keys_pressed >= 20:
            player_group.update()
        keys_pressed += 1
        edible_ghosts -= 1

        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    global level_n
    while True:
        screen.fill((0, 0, 0))
        screen.blit(logo, (150, 50))
        level_1_btn = Button(100, 400, level_1_img)
        level_2_btn = Button(550, 400, level_2_img)
        test_level_btn = Button(1000, 400, test_level_img)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if level_1_btn.draw():
            level_n = 1
            return game(True)
        if level_2_btn.draw():
            level_n = 2
            return game(True)
        if test_level_btn.draw():
            level_n = 2
            return game(False)
        pygame.display.flip()
        pygame.time.delay(FPS)


def end_screen():
    global score
    score = 0
    while True:
        screen.fill((0, 0, 0))
        text = draw_str("Game Over", font=font2)
        text2 = draw_str("[press space bar to restart]")
        text_rect = text.get_rect(center=(width / 2, 250))
        text2_rect = text2.get_rect(center=(width / 2, 450))
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return start_screen()
        particle_group.draw(screen)
        particle_group.update()
        pygame.display.flip()
        pygame.time.delay(FPS)


start_screen()
