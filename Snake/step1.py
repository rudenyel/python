import pygame
import time
import random


def scale(position): return position * 10


FPS = 15
WIDTH = scale(72)
HEIGHT = scale(48)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREEN = pygame.Color(0, 255, 0)
CORAL = pygame.Color(255, 127, 80)


def show_message(color, font, size, message):
    font = pygame.font.SysFont(font, size)
    surface = font.render(message, True, color)
    rect = surface.get_rect()
    SCREEN.blit(surface, rect)


if __name__ == '__main__':

    score = 0

    fruit = [
        random.randrange(1, (WIDTH // scale(1))) * scale(1),
        random.randrange(1, (HEIGHT // scale(1))) * scale(1)
    ]
    fruit_spawn = True

    direction = 'RIGHT'
    change_to = direction
    head = [scale(10), scale(5)]
    body = [
        [scale(9), scale(5)],
        [scale(8), scale(5)],
        [scale(7), scale(5)],
    ]

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
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        body.insert(0, list(head))
        if direction == 'UP':
            head[1] -= scale(1)
        if direction == 'DOWN':
            head[1] += scale(1)
        if direction == 'LEFT':
            head[0] -= scale(1)
        if direction == 'RIGHT':
            head[0] += scale(1)

        if head[0] == fruit[0] and head[1] == fruit[1]:
            score += 1
            FPS += 1
            fruit_spawn = False
        else:
            body.pop()

        if not fruit_spawn:
            fruit = [
                random.randrange(1, (WIDTH // scale(1))) * scale(1), # noqa
                random.randrange(1, (HEIGHT // scale(1))) * scale(1) # noqa
            ]
        fruit_spawn = True

        SCREEN.fill(BLACK)
        for part in body:
            pygame.draw.rect(SCREEN, CORAL, pygame.Rect(part[0], part[1], scale(1), scale(1))) # noqa
        pygame.draw.rect(SCREEN, GREEN, pygame.Rect(fruit[0], fruit[1], scale(1), scale(1))) # noqa

        if head[0] < 0 or head[0] >= WIDTH:
            game_over = True
        if head[1] < 0 or head[1] >= HEIGHT:
            game_over = True

        for block in body[1:]:
            if head[0] == block[0] and head[1] == block[1]:
                game_over = True

        if game_over:
            show_message(WHITE, 'arial', 18, f'Game over! Your score {score}')
        else:
            show_message(WHITE, 'arial', 18, f'Score {score}')

        pygame.display.flip()

        if game_over:
            time.sleep(5)
