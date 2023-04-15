import time

import pygame

from players import Helena

width, height = 1200, 860
BLACK = 0, 0, 0
WHITE = 255, 255, 255

pygame.init()


class Game:
    def __init__(self, ):
        self.helena = None
        self.font_big = None
        self.font_small = None
        self.show_text = True
        self.game_loop = True
        self.game_intro_loop = True
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Helena's Quest")
        self.clock = pygame.time.Clock()
        self.load_fonts()
        self.load_sounds()
        self.player_img = self.load_player_images()
        self.cog_button = self.load_images()['cog']
        self.all_sprites = pygame.sprite.Group()
        self.helena = Helena(self.player_img)
        # self.all_sprites.add(self.helena)

    def load_fonts(self):
        self.font_small = pygame.font.SysFont('calibri', 25)
        self.font_big = pygame.font.Font('assets/fonts/turok.ttf', 75)

    def load_sounds(self):
        pass

    def load_player_images(self):
        return {
            'attack1': pygame.image.load(
                "assets/img/wizard/Attack1.png").convert_alpha(),
            'attack2': pygame.image.load(
                "assets/img/wizard/Attack2.png").convert_alpha(),
            'death': pygame.image.load(
                "assets/img/wizard/Death.png").convert_alpha(),
            'fall': pygame.image.load(
                'assets/img/wizard/Fall.png').convert_alpha(),
            'hit': pygame.image.load(
                "assets/img/wizard/Hit.png").convert_alpha(),
            'idle': pygame.image.load(
                "assets/img/wizard/Idle.png").convert_alpha(),
            'jump': pygame.image.load(
                "assets/img/wizard/Jump.png").convert_alpha(),
            'run': pygame.image.load(
                "assets/img/wizard/Run.png").convert_alpha(),
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.game_intro_loop:
                    # print("Tecla Enter pressionada!")
                    self.game_intro_loop = False

    def update(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.helena.image, [25, (self.height // 2) + 90])

    def show_intro(self):
        self.screen.fill((255, 255, 255))
        text = self.font_big.render("Helena's Quest", True, (0, 0, 0))
        self.font_small.set_underline(True)
        text2 = self.font_small.render("Press Enter", True, BLACK)
        self.screen.blit(text, (self.width // 2, self.height // 2))
        if self.show_text:
            self.screen.blit(text2, (self.width // 2, (self.height // 2) + 90))
        self.screen.blit(self.cog_button, (1056, 800))

    def run(self):
        while self.game_loop:
            if self.game_intro_loop:
                self.show_intro()
                self.handle_events()
                self.show_text = not self.show_text
                self.clock.tick(5)
            else:
                self.handle_events()
                self.update()
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def load_images(self):
        images = {
            'cog': pygame.image.load(
                "assets/img/icons/cog_btn.png").convert_alpha(),
        }
        return images


Game().run()
