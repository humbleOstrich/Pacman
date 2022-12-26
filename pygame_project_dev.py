import os
import sys
import pygame
pygame.font.init()


size = width, height = 1400, 700
WIDTH, HEIGHT = width, height
screen = pygame.display.set_mode(size)
map_width, map_height = 0, 0


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
    intro_text = ["Здесь", "",
                  "Будет заставка"]
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))  # добавить заставку
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    global map_width, map_height
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'x':
                platforms.append(Platform((x, y)))
            elif level[y][x] == '@':
                new_player = Player(x, y)
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


player_image = load_image('pacman.png', colorkey=-1)  # добавить анимацию игрока


class Platform(pygame.sprite.Sprite):

    def __init__(self, coords):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(coords[0] * 25, coords[1] * 25, 25, 25)
        self.rect.x = coords[0] * 25
        self.rect.y = coords[1] * 25

    def update(self):
        pygame.draw.rect(screen, pygame.Color("black"), (self.rect.x, self.rect.y, 25, 25))


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


def draw_rect(x, y, w, h):
    pygame.draw.rect(screen, pygame.Color('black'), (x, y, w, h))


pygame.display.set_caption('pacman')

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
platforms = []
FPS = 50
speed = 10
clock = pygame.time.Clock()
start_screen()
map_name = "level_7.txt"
player, level_x, level_y = generate_level(load_level(map_name))
text_map = load_level(map_name)
while True:
    move_up = True
    move_down = True
    move_left = True
    move_right = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            char = pygame.Rect(player.rect.x + speed, player.rect.y, 40, 40)
            for m in platforms:
                if char.colliderect(m):
                    move_right = False
                    break
            if move_right:
                player.move("right")
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            char = pygame.Rect(player.rect.x - speed, player.rect.y, 40, 40)
            for m in platforms:
                if char.colliderect(m):
                    move_left = False
                    break
            if move_left:
                player.move("left")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            char = pygame.Rect(player.rect.x, player.rect.y - speed, 40, 40)
            for m in platforms:
                if char.colliderect(m):
                    move_up = False
                    break
            if move_up:
                player.move("up")

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            char = pygame.Rect(player.rect.x, player.rect.y + speed, 40, 40)
            for m in platforms:
                if char.colliderect(m):
                    move_down = False
                    break
            if move_down:
                player.move("down")
    all_sprites.update()
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    screen.fill((255, 228, 181))
    clock.tick(FPS)
