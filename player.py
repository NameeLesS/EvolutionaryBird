import pygame
import events


class Player(pygame.sprite.Sprite):
    def __init__(self, id, position, color, size, lift_strength=pygame.Vector2(0, -10)):
        super().__init__()
        self.id = id
        self.position = position
        self.color = color
        self.size = size
        self.gravity = 50
        self.lift_strength = lift_strength
        self.speed = pygame.Vector2(0, 0)
        
        self.image = pygame.Surface([size * 2, size * 2], pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            self.color,
            (size,size),
            self.size
        )
        self.rect = self.image.get_rect()

        # pygame.draw.rect(self.image, (255, 255, 255), self.rect, 5, 1)


    def update(self, dt):
        self._gravity_fall(dt)
        self.rect.center = self.position

    def on_event(self, event):
        self._handle_movement(event)

    def _gravity_fall(self, dt):
        self.speed += pygame.Vector2(0, self.gravity * dt)
        self.position += self.speed

    def _handle_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.speed = self.lift_strength.copy()

        if event.type == events.MOVEUP_EVENT:
            if event.id == self.id:
                self.speed = self.lift_strength.copy()
