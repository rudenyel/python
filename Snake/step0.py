import pygame

SCALE = 10
def scale_x(value): return value * SCALE
def scale_y(value): return value * SCALE


FPS = 15
WIDTH = scale_x(72)
HEIGHT = scale_y(48)
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
            pygame.Rect(scale_x(10),scale_y(5), scale_x(1), scale_y(1))) # noqa
        pygame.display.flip()
