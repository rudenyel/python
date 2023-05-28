import enum
import time
import random
import pygame


def scale(position): return position * 10


FPS = 10
WIDTH = scale(72)
HEIGHT = scale(48)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

FRUITS = 20

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREEN = pygame.Color(0, 255, 0)
CORAL = pygame.Color(255, 127, 80)


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


class Artefact(pygame.sprite.Sprite):

    def __init__(self, color, rect_x, rect_y, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.color = color
        self.image = pygame.Surface((scale(1), scale(1)))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y


class Hero(Artefact, Motion):

    def __init__(self, color, rect_x, rect_y, *groups):
        Artefact.__init__(self, color, rect_x, rect_y, *groups)
        Motion.__init__(self)

    def update(self):
        if self._direction == Run.up:
            self.rect.y -= scale(1)
        if self._direction == Run.down:
            self.rect.y += scale(1)
        if self._direction == Run.left:
            self.rect.x -= scale(1)
        if self._direction == Run.right:
            self.rect.x += scale(1)
        if self.rect.x < 0 or self.rect.y < 0:
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
    for _ in range(FRUITS):
        random_x = random.randrange(1, (WIDTH // scale(1))) * scale(1) # noqa
        random_y = random.randrange(1, (HEIGHT // scale(1))) * scale(1) # noqa
        Artefact(GREEN, random_x, random_y, fruits_group)

    head_group = pygame.sprite.Group()
    head = Hero(CORAL, scale(10), scale(5), head_group)
    head.direction = Run.right

    body = list()
    body_group = pygame.sprite.Group()
    body.append(Artefact(head.color, head.rect.x - scale(1), head.rect.y, body_group)) # noqa
    body.append(Artefact(head.color, head.rect.x - scale(2), head.rect.y, body_group)) # noqa
    body.append(Artefact(head.color, head.rect.x - scale(3), head.rect.y, body_group)) # noqa

    all_sprites = pygame.sprite.Group()
    all_sprites.add(fruits_group)
    all_sprites.add(head_group)
    all_sprites.add(body_group)

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

        body.insert(0, Artefact(head.color, head.rect.x, head.rect.y, all_sprites, body_group)) # noqa
        all_sprites.update()

        if pygame.sprite.groupcollide(head_group, fruits_group, False, True): # noqa
            score += 1
            FPS += 1
        else:
            body[-1].kill()
            body.pop()

        if pygame.sprite.groupcollide(head_group, body_group, False, False):  # noqa
            game_over = True

        if head.direction == Run.out:
            game_over = True

        SCREEN.fill(BLACK)
        all_sprites.draw(SCREEN)

        if game_over:
            show_message(WHITE, 'arial', 18, f'Game over! Your score {score}')
        else:
            show_message(WHITE, 'arial', 18, f'Score {score}')

        pygame.display.flip()

        if game_over:
            time.sleep(5)
