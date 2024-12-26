import pygame


class Entity:
    def __init__(self, position, color, size, lift_speed=pygame.Vector2(0, -20)):
        self.position = position
        self.color = color
        self.size = size
        self.gravity = 30
        self.lift_speed = lift_speed
        self.speed = pygame.Vector2(0, 0)

    def update(self, dt):
        self._gravity_fall(dt)

    def draw(self, screen):
        pygame.draw.circle(screen, color=self.color, center=self.position, radius=self.size)

    def on_event(self, event):
        self._handle_movement(event)

    def _gravity_fall(self, dt):
        self.speed += pygame.Vector2(0, self.gravity * dt)
        self.position += self.speed

    def _handle_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.speed = self.lift_speed.copy()
