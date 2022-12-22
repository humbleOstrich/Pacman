import pygame
import sys
import button

pygame.init()

# window size
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# define game variables
tile_size = 25
gameover = False
speed = 10
# player = None
# fps
FPS = 60
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# load images
dead_img = pygame.image.load('data/img/player/88bdc0d7bc024ec6a225b1bd841a69ecly65tYX0FyZMF0I4-20.png').convert_alpha()
player_img = pygame.image.load('data/img/player/88bdc0d7bc024ec6a225b1bd841a69ecly65tYX0FyZMF0I4-0.png').convert_alpha()
start_img = pygame.image.load('data/img/btns/Play Button.png').convert_alpha()
exit_img = pygame.image.load('data/img/btns/Quit Button.png').convert_alpha()
info_img = pygame.image.load('data/img/btns/Info Square Button.png').convert_alpha()
resume_img = pygame.image.load('data/img/btns/Resume Button.png').convert_alpha()
menu_img = pygame.image.load('data/img/btns/Menu Button.png').convert_alpha()
home_img = pygame.image.load('data/img/btns/Home Square Button.png').convert_alpha()
tile_images = {
    'wall': pygame.image.load('data/img/walls/walls/image_part_001.png'),
    'empty': pygame.image.load('data/img/floor.png')
}
background = (255, 228, 181)
death_background = (255, 69, 0)
player_img = pygame.transform.scale(player_img, (25, 25))
coords_for_first_btn = (150, 80)
coords_for_second_btn = (150, 200)
coords_for_third_btn = (150, 320)


# func
def exit():
    pygame.quit()
    sys.exit()


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (SCREEN_WIDTH, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, SCREEN_HEIGHT))


# func
def start_screen():
    fon = pygame.transform.scale(pygame.image.load('data/img/floor.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        # create btns
        start_button = button.Button(coords_for_first_btn[0], coords_for_first_btn[1], start_img, 0.35)
        resume_button = button.Button(coords_for_second_btn[0], coords_for_second_btn[1], resume_img, 0.35)
        info_button = button.Button(410, 40, info_img, 0.3)
        exit_button = button.Button(coords_for_third_btn[0], coords_for_third_btn[1], exit_img, 0.35)
        if start_button.draw(screen):
            return
        if exit_button.draw(screen):
            exit()
        if info_button.draw(screen):
            print('здесь будет окно с правилами')
        if resume_button.draw(screen):
            print('здесь будет окно с результатами')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.flip()
        pygame.time.delay(FPS)


def end_screen():
    while True:
        screen.fill(death_background)
        start_button = button.Button(coords_for_first_btn[0], coords_for_first_btn[1], start_img, 0.35)
        resume_button = button.Button(coords_for_second_btn[0], coords_for_second_btn[1], resume_img, 0.35)
        info_button = button.Button(410, 40, info_img, 0.3)
        home_button = button.Button(410, 120, home_img, 0.3)
        exit_button = button.Button(coords_for_third_btn[0], coords_for_third_btn[1], exit_img, 0.35)
        if start_button.draw(screen):
            return
        if exit_button.draw(screen):
            exit()
        if info_button.draw(screen):
            print('здесь будет окно с правилами')
        if resume_button.draw(screen):
            print('здесь будет окно с результатами')
        if home_button.draw(screen):
            start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.flip()
        pygame.time.delay(FPS)


hero = None


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = str(tile_type)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


def load_level(filename):
    filename = "data/levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# def generate_level(level):
#     global map_width, map_height
#     new_player, x, y = None, None, None
#     for y in range(len(level)):
#         for x in range(len(level[y])):
#             if level[y][x] == '.':
#                 Tile('empty', x, y)
#             elif level[y][x] == '#' or level[y][x] == '/':
#                 Tile('wall', x, y)
#             elif level[y][x] == '@':
#                 Tile('empty', x, y)
#                 new_player = Player(x, y)
#     map_width = 50 * len(level[0])
#     map_height = 50 * len(level)
#     # вернем игрока, а также размер поля в клетках
#     return new_player, x, y


# all_sprites.add(hero)
# player_group.add(hero)

# class Player(pygame.sprite.Sprite):
#     def __init__(self, pos_x, pos_y):
#         super().__init__(player_group, all_sprites)
#         self.image = player_img
#         self.rect = self.image.get_rect().move(
#             tile_size * pos_x + 15, tile_size * pos_y + 5)
#         self.mask = pygame.mask.from_surface(self.image)
#         self.move(pos_x, pos_y)
#
#     def move(self, pos_x, pos_y):
#         dx = 0
#         dy = 0
#         key = pygame.key.get_pressed()
#         if key[pygame.K_RIGHT]:
#             dx += speed
#         if key[pygame.K_LEFT]:
#             pass
#         if key[pygame.K_UP]:
#             pass
#         if key[pygame.K_DOWN]:
#             pass
#         screen.blit(self.image, self.rect)
#         pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
#         self.rect.x += dx
#         self.rect.y += dy
#         screen.blit(self.image, self.rect)
#         pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


start_screen()
run = True
hero = None

text_map = load_level('lvl1.txt')
# player, level_x, level_y = generate_level(load_level('lvl1.txt'))
while run:
    screen.fill(background)
    # generate_level('data/')
    draw_grid()
    # hero = Player(0, 0)
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
