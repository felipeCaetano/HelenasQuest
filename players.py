"""
Classe que conterá todos os caracteres jogáveis.
"""
from typing import Any

import pygame

SCREEN_HEIGHT = 800

SPEED = 5
GRAVITY = 2


class Helena(pygame.sprite.Sprite):
    animation_steps = [8, 8, 7, 2, 4, 6, 2, 8]

    def __init__(self, sprites):
        super(Helena, self).__init__()
        self.hit = False
        self.update_time = pygame.time.get_ticks()
        self.offset = 30, 25
        self.flip = False
        self.alive = True
        self.attack_type = None
        self.jump = False
        self.vel_y = 0
        self.attacking = False
        self.running = None
        self.size = None
        self.health = 100
        self.mana = 0
        self.sprites = sprites
        self.image_scale = 2
        self.name = "Helena"
        self.images = self.load_images(self.sprites)
        self.frame_index = 0
        self.image = self.images['idle'][
            self.frame_index]  # pygame.Surface((50, 50))
        self.rect = pygame.Rect(10, 420, 116, 90)
        self.rect.x, self.rect.y = 10, 420

    def animate(self, animation_cooldown=50):
        action = 'idle'
        if self.running:
            action = 'run'
        elif self.jump:
            pass
        elif self.attacking:
            pass
        elif self.hit:
            pass
        elif not self.alive:
            pass
        else:
            action = 'idle'
        self.image = self.images[action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.images[action]):
            self.frame_index = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)
        self.handle_player(args[0])
        self.animate()

    def load_images(self, sprites):
        animation_dict = {}
        for x, animation_step in enumerate(self.animation_steps):
            animation_list = []
            for w_pointer in range(animation_step):
                action, img = list(sprites.items())[x]
                width, y = img.get_size()
                step_width = (width // animation_step)
                cut_img = img.subsurface(w_pointer * step_width, 0, step_width,
                                         190)
                animation_list.append(cut_img)
            animation_dict[action] = animation_list
        return animation_dict

    def select_image(self, action, num):
        self.image = self.images[action][num]
        return self.image

    def handle_player(self, surface=None, target=None):
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if not self.attacking and self.alive:
            if key[pygame.K_a]:
                dx = -SPEED
                self.running = True
                self.flip = True
            if key[pygame.K_d]:
                dx = SPEED
                self.running = True
                self.flip = False
            if key[pygame.K_w] and not self.jump:
                self.vel_y = -25
                self.jump = True
            if key[pygame.K_r] or key[pygame.K_t]:
                if key[pygame.K_r]:
                    self.attacking = True
                    self.attack_type = 1
                else:
                    self.attacking = True
                    self.attack_type = 2
                self.attack(surface)
                self.attacking = False
            # else:
            #     self.running = False
            #     self.jump = False
            #     self.attacking = False

        self.vel_y += GRAVITY
        dy += self.vel_y
        if self.rect.bottom + dy > SCREEN_HEIGHT - 220:
            self.vel_y = 0
            self.jump = False
            dy = SCREEN_HEIGHT - 220 - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, action=None, target=None):
        if self.attacking:
            if self.attack_type == 1:
                self.image = self.select_image('attack1', 0)
            else:
                self.image = self.select_image('attack2', 0)

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - self.offset[0] * self.image_scale,
                           self.rect.y - self.offset[1] * self.image_scale))
