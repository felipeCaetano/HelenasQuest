import pygame


class NPC(pygame.sprite.Sprite):
    """
    Npc class game
    """
    def __init__(self, x, y):
        super(NPC, self).__init__()
        self.image = pygame.Surface((50, 150))
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.name = "Npc"


class HighMagister(NPC):
    pass


class Commander(NPC):
    def __init__(self, x, y):
        super(Commander, self).__init__(x, y)
        self.name = "Commander Will"
        self.dialog = True
