import pygame
from entity import Entity


class Game:
    def __init__(self, fps, screen_resolution):
        self.fps = fps
        self.screen_resolution = screen_resolution

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_resolution)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.entity = Entity(pygame.Vector2(50, 0), color=pygame.color.Color(100, 100, 10), size=40)

        self.loop()

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.screen.fill('black')

            self.update()
            self.render()

            pygame.display.flip()
            self.dt = self.clock.tick(self.fps) / 1000

        pygame.quit()

    def update(self):
        self.entity.update(self.dt)

    def on_event(self, event):
        self._quit_event(event)
        self.entity.on_event(event)

    def render(self):
        self.entity.draw(self.screen)

    def reset(self):
        pass

    def _quit_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

