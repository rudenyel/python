import pygame


def scale(position): return position * 10


FPS = 15
WIDTH = scale(72)
HEIGHT = scale(48)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        SCREEN.fill(BLACK)
        pygame.draw.rect(
            SCREEN,
            WHITE,
            pygame.Rect(scale(10),scale(5), scale(1), scale(1))) # noqa
        pygame.display.flip()
