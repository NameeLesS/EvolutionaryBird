import pygame
from entity import Entity
from wall import Walls


class Game:
    def __init__(self, fps, screen_resolution):
        self.fps = fps
        self.screen_resolution = pygame.Vector2(screen_resolution)

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_resolution)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.entity = Entity(pygame.Vector2(50, 0), color=pygame.color.Color(100, 100, 10), size=40)
        self.walls = Walls(self.screen_resolution, pygame.Vector2(5, 0), 400, pygame.color.Color(10, 100, 50))

        self.entity_group = pygame.sprite.Group(self.entity)


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
        self.entity_group.update(self.dt)
        self.walls.update(self.dt)

        for entity in self.entity_group:
            collide = pygame.sprite.spritecollide(entity, self.walls.walls_group, False)
            if collide:
                entity.kill()
                del self.entity


    def on_event(self, event):
        self._quit_event(event)
        
        for entity in self.entity_group:
            entity.on_event(event)

    def render(self):
        self.entity_group.draw(self.screen)
        self.walls.draw(self.screen)

    def reset(self):
        pass

    def _quit_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

