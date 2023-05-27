import pygame

FPS = 15
STEP = 10
WIDTH = 72 * STEP
HEIGHT = 48 * STEP
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
        pygame.draw.rect(SCREEN, WHITE, pygame.Rect(100, 50, STEP, STEP))
        pygame.display.flip()
