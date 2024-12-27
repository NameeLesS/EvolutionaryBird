import pygame
import numpy as np
import itertools
from player import Player
from wall import Walls
from stats import Stats


class Game:
    def __init__(self, fps, screen_resolution):
        self.fps = fps
        self.screen_resolution = pygame.Vector2(screen_resolution)
        self.players_group = pygame.sprite.Group()
        self.player_id_generator = itertools.count()
        self.stats = None
        self.player_scores = []
        self.distance_travelled = 0 # Meassured in number of frames rendered

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_resolution)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        
        self.stats = Stats(30, (255, 255, 255))
        self.reset()

        self.loop()

    def loop(self):
        while self.running:
            self.distance_travelled += 1
            for event in pygame.event.get():
                self.on_event(event)

            self.screen.fill('black')

            self.update()
            self.render()

            pygame.display.flip()
            self.dt = self.clock.tick(self.fps) / 1000

        pygame.quit()

    def update(self):
        self.players_group.update(self.dt)
        self.walls.update(self.dt)
        self.stats.score = self.walls.score
        self._on_wall_collision()

    def on_event(self, event):
        self._quit_event(event)
        
        for player in self.players_group:
            player.on_event(event)

    def render(self):
        self.players_group.draw(self.screen)
        self.walls.draw(self.screen)
        self.stats.draw(self.screen)

    def reset(self):
        self.walls = Walls(self.screen_resolution, pygame.Vector2(5, 0), 600, pygame.color.Color(10, 100, 50))
        self.distance_travelled = 0
        self.player_id_generator = itertools.count()
        self.player_scores.clear()
        self.stats.reset()

    def _quit_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def _on_wall_collision(self):
        for player in self.players_group:
            collide_wall = pygame.sprite.spritecollide(player, self.walls.walls_group, False)
            collide_boundaries = player.position.y > self.screen_resolution.y or player.position.y < 0
            if collide_wall or collide_boundaries:
                self.player_scores.append([player.id, self.distance_travelled])
                player.kill()


class GameWrapper(Game):
    def __init__(self, fps, screen_resolution):
        super().__init__(fps, screen_resolution)
        self._events = []

    def loop(self):
        self.distance_travelled += 1
        self._send_events()

        for event in pygame.event.get():
            self.on_event(event)

        self.screen.fill('black')

        self.update()
        self.render()

        pygame.display.flip()
        self.dt = self.clock.tick(self.fps) / 1000
        
        return self._is_game_over(), self._get_wall_distances()

    def create_players(self, n):
        players = []
        for i in range(n):
            player = Player(next(self.player_id_generator), pygame.Vector2(50, np.random.randint(0, 500)), color=pygame.color.Color(np.random.random_integers(0, 255, 3)), size=40)
            self.players_group.add(player)
            players.append(player)

        return players
    
    def add_event(self, event):
        self._events.append(event)

    def _send_events(self):
        for event in self._events:
            pygame.event.post(event)

        self._events.clear()
    
    def _get_wall_distances(self):
        lower_wall = self.walls.walls[1]
        lower_wall_position = lower_wall.position
        hole_center_position = (lower_wall_position.x + (self.walls.width / 2), lower_wall_position.y - (self.walls.hole_padding / 2))

        distances = []
        for player in self.players_group:
            distance = [abs(player.position.x - hole_center_position[0]), abs(player.position.y - hole_center_position[1])]
            standardized_x = (distance[0] - ((0 + self.walls.space + self.walls.width) / 2)) / np.sqrt((self.walls.space + self.walls.width)**2 / 12)
            standardized_y = (distance[1] - ((0 + self.screen_resolution.y) / 2)) / np.sqrt(self.screen_resolution.y**2 / 12)
            distance = [standardized_x, standardized_y]
            distances.append([player.id, distance])
        
        return distances

    def _is_game_over(self):
        if not len(self.players_group):
            return True
        