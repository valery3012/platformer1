import pygame
from BlockClass import Block
from WindowClass import Window
from CoinsClass import Coin

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE = 50

window = Window(WIDTH, HEIGHT)
clock = pygame.time.Clock()


# --- ГРАВЕЦЬ ---
player = pygame.Rect(100, 400, 50, 50)
speed = 5
vel_x = 0
vel_y = 0
gravity = 0.5
jump_power = -12
on_ground = False

# --- КАРТИНКИ ---
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))

block_img = pygame.image.load("block.png").convert_alpha()
block_img = pygame.transform.scale(block_img, (TILE, TILE))

coin_img = pygame.image.load("coin.png").convert_alpha()

spike_img = pygame.image.load("spike.png").convert_alpha()
spike_img = pygame.transform.scale(spike_img, (50, 25))

bg = pygame.image.load("background.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# --- КАМЕРА ---
scroll_x = 0
MAP_WIDTH = 3200

# --- РІВЕНЬ ---
ground = [(x, 550) for x in range(0, 3200, 50)]

platforms = [
    (300,450),(350,450),(400,450),
    (700,400),(750,400),(800,400),
    (1100,400),(1150,400),(1200,400),
    (1500,420),(1550,420),
    (1800,380),(1850,380),(1900,380),

    (2200,420),(2250,420),(2300,420),
    (2500,370),(2550,370),(2600,370),
    (2800,320),(2850,320),(2900,320)
]

pillars = [
(500,500),(500,450),
(1300,500),(1300,450),(1300,400)
]

boxes = [
(200,500),(900,500),(1600,500)
]

spikes_pos = [
    (600, 527),
    (1000, 527),
    (1370, 527),
    (2100, 527),
    (2700, 527)
]

coins_pos = [
    (250, 500),
    (600, 420),
    (1000, 350),
    (1400, 420),
    (1750, 350)
]

coins = [Coin(x, y, coin_img) for x, y in coins_pos] 

level_blocks = ground + platforms + pillars + boxes
blocks = [Block(x, y, TILE, block_img) for x, y in level_blocks]
spikes = [Block(x, y, TILE, spike_img) for x, y in spikes_pos]

coin_count = 0
font = pygame.font.SysFont("Arial", 30)

# --- ГРА ---
run = True
while run:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # =========================
    # РУХ ПО X
    # =========================
    vel_x = 0

    if keys[pygame.K_a]:
        vel_x = -speed
    if keys[pygame.K_d]:
        vel_x = speed

    player.x += vel_x

    for block in blocks:
        if player.colliderect(block.rect):
            if vel_x > 0:
                player.right = block.rect.left
            elif vel_x < 0:
                player.left = block.rect.right

    # =========================
    # СТРИБОК
    # =========================
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_power
        on_ground = False

    # =========================
    # ГРАВІТАЦІЯ
    # =========================
    vel_y += gravity
    player.y += vel_y

    on_ground = False

    for block in blocks:
        if player.colliderect(block.rect):

            if vel_y > 0:
                player.bottom = block.rect.top
                vel_y = 0
                on_ground = True

            elif vel_y < 0:
                player.top = block.rect.bottom
                vel_y = 0

    for coin in coins:
        if not coin.collected and player.colliderect(coin.rect):
            coin.collected = True
            coin_count += 1

    for spike in spikes:
        if player.colliderect(spike.rect):
            print("Game Over")
            run = False

    # =========================
    # КАМЕРА
    # =========================
    scroll_x = player.x - WIDTH // 2

    if scroll_x < 0:
        scroll_x = 0
    if scroll_x > MAP_WIDTH - WIDTH:
        scroll_x = MAP_WIDTH - WIDTH

    # =========================
    # МАЛЮВАННЯ
    # =========================
    window.screen.blit(bg, (0, 0))

    for block in blocks:
        block.draw(window.screen, scroll_x)

    for coin in coins:
        coin.draw(window.screen, scroll_x)

    for spike in spikes:
        spike.draw(window.screen, scroll_x)

    window.screen.blit(player_img, (player.x - scroll_x, player.y))

    text = font.render(f"Coins: {coin_count}", True, (255, 255, 255))
    window.screen.blit(text, (20, 20))

    window.update()

pygame.quit()