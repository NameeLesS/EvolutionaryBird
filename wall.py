import pygame
import numpy as np


class WallSprite(pygame.sprite.Sprite):
    def __init__(self, position, height, speed, color, redundant_walls, width=50):
        super().__init__()
        self.position = position
        self.speed = speed
        self.redundant_walls = redundant_walls

        self.image = pygame.Surface([width, height])
        pygame.draw.rect(
            self.image,
            color,
            pygame.Rect(0, 0, width, height),
        )
        self.rect = self.image.get_rect()
        self.rect.left = self.position.x
        self.rect.top = self.position.y

    def update(self, dt):
        self._move_wall(dt)
        self._on_maximum_position_reached()

    def _move_wall(self, dt):
        self.position -= self.speed
        self.rect.left = self.position.x
        self.rect.top = self.position.y
        
    def _on_maximum_position_reached(self):
        if self.position.x < 0:
            self.redundant_walls.append(0)


class Walls:
    def __init__(self, screen_resolution, speed, space, color, hole_size=250, width=50, hole_padding=100):
        """
        space: Size of the free space between next walls
        hole_size: Size of the empty space between two walls
        width: Width of the wall
        hole_padding: Maximum level at which the hole will be generated, e.g for hole_padding 100 range of heights at which the hole will be rendered [hole_padding, screen_resolution.y - hole_padding]
        """
        self.screen_resolution = screen_resolution
        self.speed = speed
        self.space = space
        self.color = color
        self.hole_size = hole_size
        self.width = width
        self.hole_padding = hole_padding
        self.redundant_walls = []
        self.walls = self._initialize_walls()
        self.walls_group = pygame.sprite.Group(*self.walls)
        self.score = 0

    def update(self, dt):
        self._remove_redundant_walls()
        self.walls_group.update(dt)

    def draw(self, screen):
        self.walls_group.draw(screen)

    def _remove_redundant_walls(self):
        for i in range(len(self.redundant_walls) // 2):
            self.walls[0].kill()
            self.walls[1].kill()
            del self.walls[0]
            del self.walls[0]
            self._add_wall()
            self.score += 1
        
        self.redundant_walls.clear()

    def _add_wall(self):
        last_position = self.walls[-1].position
        position = pygame.Vector2(last_position.x + (self.width + self.space))
        walls = self._create_random_wall(position)
        self.walls.extend(walls)
        self.walls_group.add(walls)

    def _initialize_walls(self):
        max_width = self.screen_resolution.x
        num_walls = np.ceil(max_width / (self.width + self.space)).astype(int)
        walls = []

        for i in range(1, num_walls + 1):
            position = pygame.Vector2((self.width + self.space) * i)
            walls.extend(self._create_random_wall(position))
        return walls

    def _create_random_wall(self, position):
        max_height = self.screen_resolution.y - self.hole_size
        random_split = np.random.randint(self.hole_padding, max_height - self.hole_padding)

        position_upper = pygame.Vector2(position.x, 0)
        position_lower = pygame.Vector2(position.x, random_split + self.hole_size)

        wall = [
            WallSprite(position=position_upper, height=random_split, speed=self.speed, color=self.color, redundant_walls=self.redundant_walls, width=self.width),
            WallSprite(position=position_lower, height=(max_height - random_split), speed=self.speed, color=self.color, redundant_walls=self.redundant_walls, width=self.width)
        ]

        return wall
