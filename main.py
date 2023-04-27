import time

import pygame

from npcs import Commander
from players import Helena
from studies.squares import Square

width, height = 1366, 800
BLACK = 0, 0, 0
WHITE = 255, 255, 255
HEALTH_COLOR = 217, 28, 44
YELLOW_COLOR = 255, 210, 28
MANA_COLOR = '#4d30bf'
MANA_BG = '#248539'
DIALOG_AREA = '#D46C22'

pygame.init()

time_interval = 1500  # 500 milliseconds == 0.1 seconds
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, time_interval)


def text_drop_shadow(font, text, color, dx, dy, shadow_color=(127, 127, 127),
                     alpha=127):
    text_size = font.size(text)
    surf = pygame.Surface(
        (text_size[0] + abs(dx), text_size[1] + abs(dy)), pygame.SRCALPHA)
    shadow_surf = font.render(text, True, shadow_color)
    shadow_surf.set_alpha(alpha)
    text_surf = font.render(text, True, color)
    surf.blit(shadow_surf, (max(0, dx), max(0, dy)))
    surf.blit(text_surf, (max(0, -dx), max(0, -dy)))
    return surf


class Game:
    show_dialog = True
    screen = pygame.display.set_mode((width, height))

    def __init__(self):
        self.scene = None
        self.helena = None
        self.font_big = None
        self.font_small = None
        self.font_smallest = None
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
        # self.background = self.load_images()['bg1']
        self.player_img = self.load_player_images()
        self.cog_button = self.load_images()['cog']
        self.all_sprites = pygame.sprite.Group()
        self.helena = Helena(self.player_img)
        self.msg_box = self.load_images()['box']
        self.chapter = 1
        self.npcs = pygame.sprite.Group()

    def load_fonts(self):
        self.font_small = pygame.font.SysFont('calibri', 25)
        self.font_big = pygame.font.Font('assets/fonts/turok.ttf', 75)
        self.font_smallest = pygame.font.Font('assets/fonts/turok.ttf', 20)

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
                Game.show_dialog = False
                if event.key == pygame.K_RETURN and self.game_intro_loop:
                    self.game_intro_loop = False
                    Game.show_dialog = True
            if event.type == timer_event and self.helena.health > 0:
                self.helena.mana += 1
                if self.helena.mana >= 100:
                    self.helena.mana = 100

    # def show_health_bar(cls, health, x, y):
    #     ratio = health / 100
    #     pygame.draw.rect(cls.screen, WHITE, (x - 2, y - 2, 202, 17))
    #     pygame.draw.rect(cls.screen, HEALTH_COLOR, (x, y, 200, 15))
    #     pygame.draw.rect(cls.screen, YELLOW_COLOR, (x, y, 200 * ratio, 15))
    #     text2 = cls.font_smallest.render("HP", True, BLACK)
    #     cls.screen.blit(text2, ((x // 2) - 6, y - 4))
    #
    # def show_mana_bar(self, mana, x, y):
    #     ratio = mana / 100
    #     pygame.draw.rect(self.screen, WHITE, (x - 2, y - 2, 202, 17))
    #     pygame.draw.rect(self.screen, MANA_BG, (x, y, 200, 15))
    #     pygame.draw.rect(self.screen, MANA_COLOR, (x, y, 200 * ratio, 15))
    #     font_smallest = pygame.font.Font('assets/fonts/turok.ttf', 18)
    #     text2 = font_smallest.render("MP", True, BLACK)
    #     self.screen.blit(text2, ((x // 2) - 6, y - 4))

    def show_dialog_bar(self, x, y, speaker, msg=None):
        if Game.show_dialog:
            self.screen.blit(self.msg_box, (x, self.height - 80))
            speaker_img = pygame.surface.Surface([70, 70])
            font_smallest = pygame.font.Font('assets/fonts/turok.ttf', 18)
            text2 = font_smallest.render(speaker.name, True, BLACK)
            message = font_smallest.render(msg, True, BLACK)
            self.screen.blit(text2, (x, y - 18))
            self.screen.blit(speaker_img, (x + 10, y + 5))
            self.screen.blit(message, (x + 85, y))

    # def update(self):
    #     self.screen.fill((255, 255, 255))
        # self.draw_background(self.background)
        # self.npcs.update()
        # self.npcs.draw(self.screen)
        # Game.show_health_bar(self.scene.helena.health, 28, 20)
        # self.show_mana_bar(self.helena.mana, 28, 40)
        # self.scene.run()
        # self.show_dialog_bar(130, self.height - 80, self.helena,
        #                      msg="O que houve aqui?")
        # self.helena.update(self.screen)
        # self.helena.draw(self.screen)
        # self.show_dialog_bar(980, self.height - 80, self.scene.npc, msg="Princesa! O alto magistrado requer sua presença")

    def show_intro(self):
        self.screen.fill((255, 255, 255))
        # text = self.font_big.render("Helena's Quest", True, (0, 0, 0))
        text = text_drop_shadow(
            self.font_big, "Helena's Quest", (0, 0, 0), -15, 10)
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
                self.create_chapter(self.chapter)
                self.handle_events()
                # self.update()
                self.scene.run()
            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()

    def load_images(self):
        images = {
            'bg1': pygame.image.load(
                "assets/img/backgrounds/castle.png").convert_alpha(),
            'box': pygame.image.load(
                "assets/img/icons/box.png").convert_alpha(),
            'cog': pygame.image.load(
                "assets/img/icons/cog_btn.png").convert_alpha(),
        }
        return images

    def create_chapter(self, chapter):
        if chapter == 1:
            self.scene = Chapter_1(self.screen, self.msg_box, self.helena, self.font_smallest, self.clock)
            # Game.scene = self.scene
            # self.set_background(self.scene.bg)


class Chapter_1:
    def __init__(self, screen, msg_box, helena, font_smallest, clock):
        self.font_smallest = font_smallest
        self.clock = clock
        self.background = None
        self.foward_key = False
        self.game = Game
        self.bg = 'bg1'
        self.screen = screen
        self.npc = Commander(1000, 600)
        self.helena = helena
        self.msg_box = msg_box
        self.show_dialog = True
        self.npcs = pygame.sprite.Group()
        self.npcs.add(self.npc)
        self.set_background(self.bg)
        self.running = True

    def draw_background(self, background):
        self.screen.blit(background, [0, 0])
        # pygame.display.update()

    def set_background(self, background):
        self.background = Game.load_images(self.game)[background]

    def show_dialog_bar(self, x, y, speaker, msg=None):
        if self.show_dialog:
            self.screen.blit(self.msg_box, (x, height - 80))
            speaker_img = pygame.surface.Surface([70, 70])
            font_smallest = pygame.font.Font('assets/fonts/turok.ttf', 18)
            text2 = font_smallest.render(speaker.name, True, BLACK)
            message = font_smallest.render(msg, True, BLACK)
            self.screen.blit(text2, (x, y - 18))
            self.screen.blit(speaker_img, (x + 10, y + 5))
            self.screen.blit(message, (x + 85, y))

    def show_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, WHITE, (x - 2, y - 2, 202, 17))
        pygame.draw.rect(self.screen, HEALTH_COLOR, (x, y, 200, 15))
        pygame.draw.rect(self.screen, YELLOW_COLOR, (x, y, 200 * ratio, 15))
        text2 = self.font_smallest.render("HP", True, BLACK)
        self.screen.blit(text2, ((x // 2) - 6, y - 4))

    def show_mana_bar(self, mana, x, y):
        ratio = mana / 100
        pygame.draw.rect(self.screen, WHITE, (x - 2, y - 2, 202, 17))
        pygame.draw.rect(self.screen, MANA_BG, (x, y, 200, 15))
        pygame.draw.rect(self.screen, MANA_COLOR, (x, y, 200 * ratio, 15))
        font_smallest = pygame.font.Font('assets/fonts/turok.ttf', 18)
        text2 = font_smallest.render("MP", True, BLACK)
        self.screen.blit(text2, ((x // 2) - 6, y - 4))

    def run(self):
        print("fui chamado")
        # while self.running:
        self.update()
        self.handle_events()
        self.show_dialog_bar(130, height - 80, self.helena,
                             "O que houve aqui?")
        self.handle_events()
        self.show_dialog_bar(self.npc.rect.x, height - 80, self.npc,
                             "Princesa! O alto magistrado requer sua presença")
        pygame.display.update()
        self.clock.tick(30)

    def update(self):
        self.screen.fill((255, 255, 255))
        self.draw_background(self.background)
        self.npcs.update()
        self.npcs.draw(self.screen)
        self.show_health_bar(self.helena.health, 28, 20)
        self.show_mana_bar(self.helena.mana, 28, 40)
        # Game.update(self.game)
        # self.scene.run()
        # self.show_dialog_bar(130, self.height - 80, self.helena,
        #                      msg="O que houve aqui?")
        self.helena.update(self.screen)
        self.helena.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_r or event.key == pygame.K_t:
                    print("scene events")
                    self.show_dialog = not self.show_dialog
                    print(self.show_dialog)
                    return True


Game().run()
