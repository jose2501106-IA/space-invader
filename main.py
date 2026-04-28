import sys
import pygame

from GameClass import Game


WIDTH, HEIGHT = 800, 600
FPS = 60


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    icon = pygame.image.load('img/title_icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Space Invader')

    font = pygame.font.SysFont('comicsans', 30)

    game = Game(font, FPS, lives=5, window=window,
                screen_width=WIDTH, screen_height=HEIGHT, bullets=3)

    running = True
    while running:
        game.clock.tick(FPS)

        events = pygame.event.get()
        if game.escape(events):
            running = False
            break

        window.fill((0, 0, 0))
        game.draw_HUD()
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
