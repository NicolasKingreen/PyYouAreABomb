import pygame
from pygame.locals import *
pygame.init()

import random

SCREEN_SIZE = 832, 480
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
TARGET_FPS = 60

BLOCK_SIZE = 32
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
            random_gap = random.randint(self.height // 3, (self.height * 2) // 3 - 1)
            for y in range(self.height - 1, random_gap, -1):
                self.blocks[x][y] = True


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("You Are a Bomb")
        self.display_surface = pygame.display.set_mode(SCREEN_SIZE)
        self.is_running = False

        self.field = Field((WIDTH_IN_BLOCKS, HEIGHT_IN_BLOCKS))
        self.field.set_starting_blocks()

        self.BRICK_SPRITE = pygame.image.load(BRICK_SPRITE_PATH).convert()
        self.BRICK_SPRITE = pygame.transform.scale(self.BRICK_SPRITE,
                                                   (self.BRICK_SPRITE.get_width() * 4,
                                                    self.BRICK_SPRITE.get_height() * 4))
        self.BOMB_SPRITE = pygame.image.load(BOMB_SPRITE_PATH).convert_alpha()

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()

            self.display_surface.fill("white")
            for x in range(self.field.width):
                for y in range(self.field.height):
                    if self.field.blocks[x][y]:
                        self.display_surface.blit(self.BRICK_SPRITE, (x * BLOCK_SIZE, y * BLOCK_SIZE))
            pygame.display.update()

    def terminate(self):
        self.is_running = False


if __name__ == "__main__":
    Game().run()


