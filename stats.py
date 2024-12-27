import pygame

class Stats:
    def __init__(self, size, color, fonttype='Comic Sans MS'):
        if fonttype is None:
            self.font = pygame.font.get_default_font()
        else:
            self.font = pygame.font.SysFont(fonttype, size=size)

        self.size = size
        self.color = color

        self.generation = 0
        self.score = 0
        self.max_score = 0

    def draw(self, screen):
        generation_text = self.font.render(f'Generation: {self.generation}', True, self.color)
        score_text = self.font.render(f'Score: {self.score}', True, self.color)
        max_score_text = self.font.render(f'Max score: {self.max_score}', True, self.color)
        
        screen.blit(generation_text, generation_text.get_rect(left=0, top=0))
        screen.blit(score_text, score_text.get_rect(left=0,  top=50))
        screen.blit(max_score_text, max_score_text.get_rect(left=0,  top=100))
    
    def reset(self):
        self.score = 0