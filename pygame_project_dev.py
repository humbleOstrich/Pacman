import os
import sqlite3
import sys
import pygame
import random
import button

pygame.font.init()

size = width, height = 1400, 700
WIDTH, HEIGHT = width, height
screen = pygame.display.set_mode(size)
map_width, map_height = 0, 0

start_img = pygame.image.load('data/img/btns/Play Button.png').convert_alpha()
exit_img = pygame.image.load('data/img/btns/Quit Button.png').convert_alpha()
info_img = pygame.image.load('data/img/btns/Info Square Button.png').convert_alpha()
resume_img = pygame.image.load('data/img/btns/Resume Button.png').convert_alpha()
menu_img = pygame.image.load('data/img/btns/Menu Button.png').convert_alpha()
home_img = pygame.image.load('data/img/btns/Home Square Button.png').convert_alpha()
death_background = (255, 69, 0)

coords_for_first_btn = ((width // 2) - 150, 80)
coords_for_second_btn = ((width // 2) - 150, 200)
coords_for_third_btn = ((width // 2) - 150, 320)


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


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('data/img/floor.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        # create btns
        start_button = button.Button(coords_for_first_btn[0], coords_for_first_btn[1], start_img, 0.35)
        resume_button = button.Button(coords_for_second_btn[0], coords_for_second_btn[1], resume_img, 0.35)
        info_button = button.Button(width // 2 + 200, 40, info_img, 0.3)
        exit_button = button.Button(coords_for_third_btn[0], coords_for_third_btn[1], exit_img, 0.35)
        if start_button.draw(screen):
            global gameover
            gameover = False
            global counter
            counter = 0

            return
        if exit_button.draw(screen):
            terminate()
        if info_button.draw(screen):
            print('здесь будет окно с правилами')
        if resume_button.draw(screen):
            print('здесь будет окно с результатами')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        pygame.time.delay(FPS)


def generate_level(level):
    global map_width, map_height
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'x':
                platforms.append(Platform((x, y)))
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == 'p':
                points.append(Point((x, y)))
            elif level[y][x] == 'c':
                points.append(Point((x, y)))
                c_points.append(CPoint((x, y), 0))
            elif level[y][x] == 'd':
                points.append(Point((x, y)))
                c_points.append(CPoint((x, y), 2))
            elif level[y][x] == 'r':
                points.append(Point((x, y)))
                c_points.append(CPoint((x, y), 1))
            elif level[y][x] == 'l':
                points.append(Point((x, y)))
                c_points.append(CPoint((x, y), -1))
            elif level[y][x] == 'u':
                points.append(Point((x, y)))
                c_points.append(CPoint((x, y), -2))
            elif level[y][x] == 'e':
                enemies.append(Enemy(x, y, enemy_e_image))
            elif level[y][x] == 'n':
                enemies.append(Enemy(x, y, enemy_n_image))
            elif level[y][x] == 'm':
                enemies.append(Enemy(x, y, enemy_m_image))
            elif level[y][x] == 'y':
                enemies.append(Enemy(x, y, enemy_y_image))
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
    cur.execute(f'INSERT INTO results(level,score) VALUES({level}, {score})').fetchall()
    con.commit()
    con.close()


def end_screen():
    while True:
        screen.fill(death_background)
        start_button = button.Button(coords_for_first_btn[0], coords_for_first_btn[1], start_img, 0.35)
        resume_button = button.Button(coords_for_second_btn[0], coords_for_second_btn[1], resume_img, 0.35)
        info_button = button.Button(width // 2 + 200, 40, info_img, 0.3)
        home_button = button.Button(width // 2 + 200, 120, home_img, 0.3)
        exit_button = button.Button(coords_for_third_btn[0], coords_for_third_btn[1], exit_img, 0.35)
        if start_button.draw(screen):
            # gameover = False
            global gameover
            gameover = False
            global counter
            map_name = f"levels/level_{level}.txt"
            global player
            global level_x
            global level_y
            # all_sprites.kill()
            for player in player_group:
                player.kill()
                player_group.remove(player)
                del player
            for point in point_group:
                point.kill()
                point.remove()
                del point
                points.clear()
            for enemy in enemy_group:
                enemy.remove()
                enemy.kill()
                enemy_group.remove(enemy)
                enemies.clear()
                del enemy

            player, level_x, level_y = generate_level(load_level(map_name))
            counter = 0
            screen.fill((255, 228, 181))

            return
        if exit_button.draw(screen):
            terminate()
        if info_button.draw(screen):
            print('здесь будет окно с правилами')
        if resume_button.draw(screen):
            print('здесь будет окно с результатами')
        if home_button.draw(screen):
            start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        pygame.time.delay(FPS)


def animation(x, y):
    global animation_counter
    if animation_counter == 19:
        animation_counter = 0
    screen.blit(player_img[animation_counter // 10], (x, y))
    animation_counter += 1


pacman_copy = load_image("pacman0_copy.png")


def flip_animation(direction):
    if direction == 'right':
        player_img[0] = pacman_copy
    if direction == 'left':
        player_img[0] = pygame.transform.flip(pacman_copy, True, False)
    if direction == 'down':
        player_img[0] = pygame.transform.rotate(pacman_copy, -90)
    if direction == 'up':
        player_img[0] = pygame.transform.rotate(pacman_copy, 90)


player_image = load_image('pacman.png')  # добавить анимацию игрока
enemy_e_image = load_image('ghost_1.png')
enemy_n_image = load_image('ghost_2.png')
enemy_m_image = load_image('ghost_3.png')
enemy_y_image = load_image('ghost_4.png')
player_img = [load_image('pacman0.png'), load_image('pacman1.png')]


class Platform(pygame.sprite.Sprite):

    def __init__(self, coords):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(coords[0] * 25, coords[1] * 25, 25, 25)
        self.rect.x = coords[0] * 25
        self.rect.y = coords[1] * 25

    def update(self):
        pygame.draw.rect(screen, pygame.Color("black"), (self.rect.x, self.rect.y, 25, 25))


class Point(pygame.sprite.Sprite):

    def __init__(self, coords):
        super().__init__(all_sprites, point_group)
        self.rect = pygame.Rect(coords[0] * 25, coords[1] * 25, 16, 16)
        self.rect.x = coords[0] * 25
        self.rect.y = coords[1] * 25

    def update(self):
        pygame.draw.circle(screen, pygame.Color("black"), (self.rect.x + 8, self.rect.y + 8), 8)


class CPoint(pygame.sprite.Sprite):

    def __init__(self, coords, forbidden_d):
        super().__init__(all_sprites, c_point_group)
        self.rect = pygame.Rect(coords[0] * 25, coords[1] * 25, 5, 5)
        self.rect.x = coords[0] * 25
        self.rect.y = coords[1] * 25
        self.f_direction = forbidden_d

    def update(self):
        pygame.draw.rect(screen, pygame.Color("red"), (self.rect.x, self.rect.y, 5, 5))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        # self.image = player_image
        # self.rect = self.image.get_rect().move(
        #     25 * pos_x, 25 * pos_y)
        self.rect = pygame.Rect(25 * pos_x, 25 * pos_y, 60, 60)

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
        screen.blit(player_img[animation_counter // 10], (self.rect.x, self.rect.y))
        # animation(self.rect.x, self.rect.y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        super().__init__(enemy_group, all_sprites)
        self.image = name
        self.rect = self.image.get_rect().move(
            25 * pos_x, 25 * pos_y)
        self.route = 1

    def move(self, direction, distance):
        if direction == 1:
            self.rect = self.rect.move(distance, 0)
        elif direction == -1:
            self.rect = self.rect.move(distance, 0)
        elif direction == 2:
            self.rect = self.rect.move(0, distance)
        elif direction == -2:
            self.rect = self.rect.move(0, distance)


pygame.display.set_caption('pacman')

player = None
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
point_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
c_point_group = pygame.sprite.Group()
platforms = []
points = []
c_points = []
enemies = []
animation_counter = 0
FPS = 50
player_speed = 10
enemy_speed = 5
clock = pygame.time.Clock()
start_screen()
level = 8
once = 0
map_name = f"levels/level_{level}.txt"
player, level_x, level_y = generate_level(load_level(map_name))
text_map = load_level(map_name)
counter = 0
total_points = 10000
routes = [1, -1, 2, -2]
gameover = False
keys_pressed = 20

while True:
    move_up = True
    move_down = True
    move_left = True
    move_right = True
    keys_pressed += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        keys_pressed = 0
        flip_animation("right")
        char = pygame.Rect(player.rect.x + player_speed, player.rect.y, 60, 60)
        for m in platforms:
            if char.colliderect(m):
                move_right = False
                break
        if move_right:
            player.move("right", player_speed)
    if keys[pygame.K_a]:
        keys_pressed = 0
        flip_animation("left")
        char = pygame.Rect(player.rect.x - player_speed, player.rect.y, 60, 60)
        for m in platforms:
            if char.colliderect(m):
                move_left = False
                break
        if move_left:
            player.move("left", -player_speed)
    if keys[pygame.K_w]:
        keys_pressed = 0
        flip_animation("up")
        char = pygame.Rect(player.rect.x, player.rect.y - player_speed, 60, 60)
        for m in platforms:
            if char.colliderect(m):
                move_up = False
                break
        if move_up:
            player.move("up", -player_speed)
    if keys[pygame.K_s]:
        keys_pressed = 0
        flip_animation("down")
        char = pygame.Rect(player.rect.x, player.rect.y + player_speed, 60, 60)
        for m in platforms:
            if char.colliderect(m):
                move_down = False
                break
        if move_down:
            player.move("down", player_speed)

    if pygame.sprite.spritecollide(player, point_group, True):
        counter += 1
    if counter == total_points:
        gameover = True

    for enemy in enemies:
        if player.rect.colliderect(enemy):
            gameover = True
        if enemy.route == 1:
            mob = pygame.Rect(enemy.rect.x + enemy_speed, enemy.rect.y, 70, 70)
            for m in platforms:
                if mob.colliderect(m):
                    possible_r = routes[random.randint(0, 3)]
                    while possible_r == -1 or possible_r == 1:
                        possible_r = routes[random.randint(0, 3)]
                    enemy.route = possible_r
                    break
            else:
                enemy.move(1, enemy_speed)
        if enemy.route == -1:
            mob = pygame.Rect(enemy.rect.x - enemy_speed, enemy.rect.y, 70, 70)
            for m in platforms:
                if mob.colliderect(m):
                    possible_r = routes[random.randint(0, 3)]
                    while possible_r == 1 or possible_r == -1:
                        possible_r = routes[random.randint(0, 3)]
                    enemy.route = possible_r
                    break
            else:
                enemy.move(-1, -enemy_speed)
        if enemy.route == 2:
            mob = pygame.Rect(enemy.rect.x, enemy.rect.y + enemy_speed, 70, 70)
            for m in platforms:
                if mob.colliderect(m):
                    possible_r = routes[random.randint(0, 3)]
                    while possible_r == -2 or possible_r == 2:
                        possible_r = routes[random.randint(0, 3)]
                    enemy.route = possible_r
                    break
            else:
                enemy.move(2, enemy_speed)
        if enemy.route == -2:
            mob = pygame.Rect(enemy.rect.x, enemy.rect.y - enemy_speed, 70, 70)
            for m in platforms:
                if mob.colliderect(m):
                    possible_r = routes[random.randint(0, 3)]
                    while possible_r == 2 or possible_r == -2:
                        possible_r = routes[random.randint(0, 3)]
                    enemy.route = possible_r
                    break
            else:
                enemy.move(-2, -enemy_speed)
        # if pygame.sprite.spritecollide(enemy, c_point_group, False):
        #     for m in c_points:
        #         if enemy.rect.colliderect(m):
        #             possible_r = routes[random.randint(0, 3)]
        #             while possible_r == m.f_direction:
        #                 possible_r = routes[random.randint(0, 3)]
        #             enemy.route = possible_r
        #             enemy.move(enemy.route, 5)
        for point in c_points:
            if point.rect.x == enemy.rect.x + 35:
                if point.rect.y == enemy.rect.y + 35:
                    pr = routes[random.randint(0, 3)]
                    while pr == point.f_direction:
                        pr = routes[random.randint(0, 3)]
                    enemy.route = pr
                    enemy.move(enemy.route, 10)
                    break
    if gameover:
        if once == 0:
            add_to_database(level, counter)
            once += 1
        end_screen()
        terminate()
    screen.fill((255, 228, 181))
    all_sprites.update()
    if keys_pressed < 20:
        animation(player.rect.x, player.rect.y)

    if keys_pressed >= 20:
        player_group.update()

    enemy_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
