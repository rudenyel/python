import enum
import time
import random
import pygame


FPS = 10
STEP = 10
WIDTH = 72 * STEP
HEIGHT = 48 * STEP
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
CORAL = pygame.Color(255, 127, 80)


class Artefact(pygame.sprite.Sprite):

    def __init__(self, color, rect_x, rect_y, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.color = color
        self.image = pygame.Surface((STEP, STEP))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y


@enum.unique
class Run(enum.Enum):
    standup = 0
    up = 1
    down = 2
    left = 3
    right = 4
    out = 5


class Motion(object):
    def __init__(self):
        self._direction = Run.standup

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value == Run.up and self._direction != Run.down:
            self._direction = Run.up
        if value == Run.down and self._direction != Run.up:
            self._direction = Run.down
        if value == Run.left and self._direction != Run.right:
            self._direction = Run.left
        if value == Run.right and self._direction != Run.left:
            self._direction = Run.right
        if value == Run.standup:
            self._direction = Run.standup
        if value == Run.out:
            self._direction = Run.out


class Hero(Artefact, Motion):

    def __init__(self, color, rect_x, rect_y, *groups):
        Artefact.__init__(self, color, rect_x, rect_y, *groups)
        Motion.__init__(self)

    def update(self):
        if self._direction == Run.up:
            self.rect.y -= STEP
        if self._direction == Run.down:
            self.rect.y += STEP
        if self._direction == Run.left:
            self.rect.x -= STEP
        if self._direction == Run.right:
            self.rect.x += STEP
        if self.rect.x <= 0 or self.rect.y <= 0:
            self.direction = Run.out
        if self.rect.x >= WIDTH:
            self.direction = Run.out
        if self.rect.y >= HEIGHT:
            self.direction = Run.out


def show_message(color, font, size, message):
    font = pygame.font.SysFont(font, size)
    surface = font.render(message, True, color)
    rect = surface.get_rect()
    SCREEN.blit(surface, rect)


if __name__ == '__main__':

    score = 0

    fruits_group = pygame.sprite.Group()
    for _ in range(10):
        random_x = random.randrange(1, (WIDTH // STEP)) * STEP
        random_y = random.randrange(1, (HEIGHT // STEP)) * STEP
        Artefact(GREEN, random_x, random_y, fruits_group)

    snake_group = pygame.sprite.Group()
    head = Hero(CORAL, 100, 50, snake_group)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(fruits_group)
    all_sprites.add(snake_group)

    pygame.init()
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    running = True
    game_over = False
    while running and not game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    head.direction = Run.up
                if event.key == pygame.K_DOWN:
                    head.direction = Run.down
                if event.key == pygame.K_LEFT:
                    head.direction = Run.left
                if event.key == pygame.K_RIGHT:
                    head.direction = Run.right
        all_sprites.update()

        if pygame.sprite.groupcollide(snake_group, fruits_group, False, True):
            score += 1

        if head.direction == Run.out:
            game_over = True

        SCREEN.fill(BLACK)
        all_sprites.draw(SCREEN)
        if game_over:
            show_message(WHITE, 'arial', 18, f'Game over! Your score {score}')
            pygame.display.flip()
            time.sleep(5)
        else:
            show_message(WHITE, 'arial', 18, f'Score {score}')
            pygame.display.flip()
