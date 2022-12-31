import os
import sys
import pygame
import random
import sqlite3
import button

pygame.init()

size = width, height = 1500, 700
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


def add_to_database(level, score):
    con = sqlite3.connect("results_db.sqlite")
    cur = con.cursor()
    cur.execute(f'INSERT INTO results(level,score) VALUES({level}, {score})').fetchall()
    con.commit()
    con.close()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


player_image = load_image('img/pacman.png')  # добавить анимацию игрока
enemy_e_image = load_image('img/ghost.png')
enemy_n_image = load_image('img/ghost_2.png')
enemy_m_image = load_image('img/ghost_3.png')
enemy_y_image = load_image('img/ghost_4.png')


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
        pygame.draw.circle(screen, pygame.Color("black"), (self.rect.x + 18, self.rect.y + 18), 8)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            25 * pos_x, 25 * pos_y)

    def move(self, direction):

        if direction == "right":
            self.rect = self.rect.move(10, 0)
        elif direction == "left":
            self.rect = self.rect.move(-10, 0)
        elif direction == "down":
            self.rect = self.rect.move(0, 10)
        elif direction == "up":
            self.rect = self.rect.move(0, -10)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        super().__init__(enemy_group, all_sprites)
        self.image = name
        self.rect = self.image.get_rect().move(
            25 * pos_x, 25 * pos_y)
        self.route = 'right'

    def move(self, direction):
        if direction == "right":
            self.rect = self.rect.move(10, 0)
        elif direction == "left":
            self.rect = self.rect.move(-10, 0)
        elif direction == "down":
            self.rect = self.rect.move(0, 10)
        elif direction == "up":
            self.rect = self.rect.move(0, -10)


pygame.display.set_caption('pacman')

# player = None
gameover = False
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
point_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
platforms = []
points = []
enemies = []
FPS = 60
player_speed = 10
enemy_speed = 10
clock = pygame.time.Clock()
start_screen()
level = 8
once = 0
map_name = f"levels/level_{level}.txt"
player, level_x, level_y = generate_level(load_level(map_name))
text_map = load_level(map_name)
counter = 0
total_points = 10000
routes = ['right', 'left', 'down', 'up']
coords = [(1000, 250), (1025, 250), (975, 250)]

while True:
    print(gameover)
    move_up = True
    move_down = True
    move_left = True
    move_right = True

    if gameover is False:
        once = 0
        char = pygame.Rect(player.rect.x, player.rect.y, 60, 60)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                terminate()

            if keys[pygame.K_d]:
                char = pygame.Rect(player.rect.x + player_speed, player.rect.y, 60, 60)
                for m in platforms:
                    if char.colliderect(m):
                        move_right = False
                        break
                # for enemy in enemies:
                # if char.colliderect(enemy):
                #     gameover = True
                if move_right:
                    player.move("right")
            if keys[pygame.K_a]:
                char = pygame.Rect(player.rect.x - player_speed, player.rect.y, 60, 60)
                for m in platforms:
                    if char.colliderect(m):
                        move_left = False
                        break
                # for enemy in enemies:
                #     if char.colliderect(enemy):
                #         gameover = True
                if move_left:
                    player.move("left")
            if keys[pygame.K_w]:
                char = pygame.Rect(player.rect.x, player.rect.y - player_speed, 60, 60)
                for m in platforms:
                    if char.colliderect(m):
                        move_up = False
                        break
                # for enemy in enemies:
                #     if char.colliderect(enemy):
                #         gameover = True
                if move_up:
                    player.move("up")
            if keys[pygame.K_s]:
                char = pygame.Rect(player.rect.x, player.rect.y + player_speed, 60, 60)
                for m in platforms:
                    if char.colliderect(m):
                        move_down = False
                        break
                # for enemy in enemies:
                #     if char.colliderect(enemy):
                #         gameover = True
                if move_down:
                    player.move("down")
        if pygame.sprite.spritecollide(player, point_group, True):
            counter += 1

        if counter == total_points:
            gameover = True
            # level += 1

        for enemy in enemies:
            print(enemy)
            if char.colliderect(enemy):
                gameover = True
                print('enemy')
            if int(enemy.rect.x) + 35 in range(1015, 1035) and int(enemy.rect.y) + 35 in range(250, 270):
                possible_route = routes[random.randint(0, 3)]
                print(enemy.route)
                while possible_route == enemy.route:
                    possible_route = routes[random.randint(0, 3)]
                enemy.route = possible_route
                print(enemy.route)

            if enemy.route == 'right':
                mob = pygame.Rect(enemy.rect.x + enemy_speed, enemy.rect.y, 70, 70)
                for m in platforms:
                    if mob.colliderect(m):
                        enemy.route = routes[random.randint(0, 3)]
                        break
                else:
                    enemy.move('right')
            if enemy.route == 'left':
                mob = pygame.Rect(enemy.rect.x - enemy_speed, enemy.rect.y, 70, 70)
                for m in platforms:
                    if mob.colliderect(m):
                        enemy.route = routes[random.randint(0, 3)]
                        break
                else:
                    enemy.move('left')
            if enemy.route == 'down':
                mob = pygame.Rect(enemy.rect.x, enemy.rect.y + enemy_speed, 70, 70)
                for m in platforms:
                    if mob.colliderect(m):
                        enemy.route = routes[random.randint(0, 3)]
                        break
                else:
                    enemy.move('down')
            if enemy.route == 'up':
                mob = pygame.Rect(enemy.rect.x, enemy.rect.y - enemy_speed, 70, 70)
                for m in platforms:
                    if mob.colliderect(m):
                        enemy.route = routes[random.randint(0, 3)]
                        break
                else:
                    enemy.move('up')

    elif gameover is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if once == 0:
            add_to_database(level, counter)
            once += 1
            end_screen()

    all_sprites.update()
    pygame.draw.rect(screen, (255, 0, 0), (1015, 250, 10, 10))
    player_group.draw(screen)
    enemy_group.draw(screen)
    pygame.display.flip()
    screen.fill((255, 228, 181))
    clock.tick(FPS)
