from game import GameWrapper
import events
import pygame


class BirdEvolution:
    def __init__(self):
        pass




game = GameWrapper(fps=60, screen_resolution=(3000, 1500))
players = game.create_players(10)
game.init()

is_over = False
while True:
    is_over, distances = game.loop()

    if is_over:
        print(game.player_score)
        game.reset()
        players = game.create_players(10)
    # for player in players:
        # game.add_event(pygame.event.Event(events.MOVEUP_EVENT, id=player.id))


print('s')

