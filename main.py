import pygame
from pygame.locals import *
pygame.init()

import random

# TODO: make bomb explosion physics and animation

SCREEN_SIZE = 832, 480
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
TARGET_FPS = 60

BLOCK_SIZE = 32  # 8xSomething
WIDTH_IN_BLOCKS = SCREEN_WIDTH // BLOCK_SIZE
HEIGHT_IN_BLOCKS = SCREEN_HEIGHT // BLOCK_SIZE

BRICK_SPRITE_PATH = "data/brick.png"
BOMB_SPRITE_PATH = "data/bomb.png"


class Field:
    """
        |F F F F F F F
        |F T F F T F F
        |F T T F T T F
        |T T T T T T T
    x   --------------
        y
    """
    def __init__(self, size):
        self.width, self.height = size
        self.blocks = [[None for _ in range(self.height)] for _ in range(self.width)]

    def set_starting_blocks(self):
        for x in range(self.width):
            random_gap = random.randint(self.height // 2, (self.height * 2) // 3 - 1)
            print(random_gap)
            for y in range(self.height - 1, random_gap, -1):
                self.blocks[x][y] = True

    def get_top_blocks(self):
        blocks = [None for _ in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                if self.blocks[x][y]:
                    blocks[x] = (x, y)
                    break
        return blocks


class Bomb:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.y = y
        self.y_velocity = 200

        self.life_timer = 3000  # in ms
        self.dropped = False

    def update(self, frame_time_s):
        self.y += self.y_velocity * frame_time_s
        self.rect.y = self.y

        if self.dropped:
            self.life_timer -= frame_time_s * 1000

        if self.life_timer < 0:
            # TODO: remove self from bombs
            pass

    def check_collision(self, field):
        obstacle = field.get_top_blocks()[self.rect.x]
        if self.y > (obstacle[1] - 1) * BLOCK_SIZE:
            self.dropped = True
            self.y = (obstacle[1] - 1) * BLOCK_SIZE
            self.rect.y = self.y


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("You Are a Bomb")
        self.display_surface = pygame.display.set_mode(SCREEN_SIZE)
        self.is_running = False

        self.field = Field((WIDTH_IN_BLOCKS, HEIGHT_IN_BLOCKS))
        self.field.set_starting_blocks()

        self.bombs = []

        self.BRICK_SPRITE = pygame.image.load(BRICK_SPRITE_PATH).convert()
        self.BRICK_SPRITE = pygame.transform.scale(self.BRICK_SPRITE,
                                                   (BLOCK_SIZE, BLOCK_SIZE))
        self.BOMB_SPRITE = pygame.image.load(BOMB_SPRITE_PATH).convert_alpha()
        self.BOMB_SPRITE = pygame.transform.scale(self.BOMB_SPRITE,
                                                  (BLOCK_SIZE, BLOCK_SIZE))

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            frame_time_s = frame_time_ms / 1000.

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_d:
                        self.spawn_bomb()

            for bomb in self.bombs:
                bomb.update(frame_time_s)
                bomb.check_collision(self.field)

            self.display_surface.fill("white")
            for x in range(self.field.width):
                for y in range(self.field.height):
                    if self.field.blocks[x][y]:
                        self.display_surface.blit(self.BRICK_SPRITE, (x * BLOCK_SIZE, y * BLOCK_SIZE))
            for bomb in self.bombs:
                self.display_surface.blit(self.BOMB_SPRITE,
                                          (bomb.rect.x * BLOCK_SIZE,
                                           bomb.rect.y))
                # TODO: make life timer text
            pygame.display.update()

    def terminate(self):
        self.is_running = False

    def spawn_bomb(self):
        random_x = random.randint(0, self.field.width)
        self.bombs.append(Bomb(random_x, 0))


if __name__ == "__main__":
    Game().run()


