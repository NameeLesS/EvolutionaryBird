import pygame
import numpy as np


class Wall:
    def __init__(self, position, speed, color, screen_resolution, redundant_walls, hole_size=50, width=50, hole_padding=100):
        """
        hole_size: Size of the empty space between two walls
        width: Width of the wall
        hole_padding: Maximum level at which the hole will be generated, e.g for hole_padding 100 range of heights at which the hole will be rendered [hole_padding, screen_resolution.y - hole_padding]
        """
        self.position = position
        self.speed = speed
        self.color = color
        self.hole_size = hole_size
        self.hole_padding = hole_padding
        self.width = width
        self.screen_resolution = screen_resolution
        self.redundant_walls = redundant_walls
        self.wall = self._get_random_wall()


    def update(self, dt):
        self._move_wall(dt)
        self._on_maximum_position_reached()

    def draw(self, screen):
        for rect in self.wall:
            pygame.draw.rect(screen, color=self.color,  rect=rect)

    def on_event(self, event):
        pass

    def _get_random_wall(self):
        max_height = self.screen_resolution.y - self.hole_size
        random_split = np.random.randint(self.hole_padding, max_height - self.hole_padding)

        wall = [
            pygame.Rect(self.position.x, 0, self.width, random_split),
            pygame.Rect(self.position.x, random_split + self.hole_size, self.width, max_height - random_split)
        ]

        return wall

    def _move_wall(self, dt):
        self.position -= self.speed
        
        for wall in self.wall:
            wall.left = self.position.x
        
    def _on_maximum_position_reached(self):
        if self.position.x < 0:
            self.redundant_walls.append(0)


class Walls:
    def __init__(self, screen_resolution, speed, space, color, hole_size=150, width=100, hole_padding=100):
        """
        space: Size of the free space between next walls
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
        self.score = 0

    def update(self, dt):
        self._remove_redundant_walls()
        
        for wall in self.walls:
            wall.update(dt)

    def draw(self, screen):
        for wall in self.walls:
            wall.draw(screen)

    def on_event(self, event):
        for wall in self.walls:
            wall.on_event(event)

    def _remove_redundant_walls(self):
        for i in range(len(self.redundant_walls)):
            del self.walls[0]
            self._add_wall()
            self.score += 1
        
        self.redundant_walls.clear()

    def _add_wall(self):
        last_position = self.walls[-1].position
        position = pygame.Vector2(last_position.x + (self.width + self.space))
        self.walls.append(Wall(position=position, speed=self.speed, color=self.color, screen_resolution=self.screen_resolution,
                redundant_walls=self.redundant_walls, hole_size=self.hole_size, width=self.width, hole_padding=self.hole_padding))

    def _initialize_walls(self):
        max_width = self.screen_resolution.x
        num_walls = np.ceil(max_width / (self.width + self.space)).astype(int)
        walls = []

        for i in range(1, num_walls + 1):
            position = pygame.Vector2((self.width + self.space) * i)
            walls.append(Wall(position=position, speed=self.speed, color=self.color, screen_resolution=self.screen_resolution,
                redundant_walls=self.redundant_walls, hole_size=self.hole_size, width=self.width, hole_padding=self.hole_padding))
        return walls
