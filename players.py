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
        self.action = 'idle'
        self.alive = True
        self.attack_cooldown = 20
        self.attack_type = None
        self.attacking = False
        self.fall = False
        self.flip = False
        self.hit = False
        self.jump = False
        self.running = None
        self.size = None
        self.health = 10
        self.frame_index = 0
        self.image_scale = 2
        self.mana = 10
        self.name = "Helena"
        self.offset = 80, 55
        self.vel_y = 0
        self.update_time = pygame.time.get_ticks()
        self.sprites = sprites
        self.images = self.load_images(self.sprites)
        self.image = self.images['idle'][
            self.frame_index]  # pygame.Surface((50, 50))
        self.rect = pygame.Rect(10, 420, 116, 90)
        self.rect.x, self.rect.y = 0, 500

    def animate(self, animation_cooldown=50):
        action = 'idle'
        if self.running:
            action = 'run'
            # self.update_animation(action)
        elif self.jump:
            action = 'jump'
            # self.update_animation(action)
        elif self.attacking:
            if self.attack_type == 1:
                action = 'attack1'
            elif self.attack_type == 2:
                action = 'attack2'
        elif self.hit:
            pass
        elif not self.alive:
            action = 'death'
        elif self.fall:
            action = 'fall'
        else:
            action = 'idle'
        self.update_animation(action)
        self.image = self.images[action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.images[action]):
            # self.frame_index = 0
            if not self.alive:
                self.frame_index = len(self.images[action]) - 1
            else:
                self.frame_index = 0
                if self.action == 'attack1' or self.action == 'attack2':
                    self.attacking = False
                    self.attack_cooldown = 20

    def update_animation(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)
        self.handle_player(args[0])
        if self.health <= 0:
            self.health = 0
            self.alive = False
        self.animate()

    def load_images(self, sprites):
        animation_dict = {}
        action = None
        for x, animation_step in enumerate(self.animation_steps):
            animation_list = []
            for w_pointer in range(animation_step):
                action, img = list(sprites.items())[x]
                width, y = img.get_size()
                step_width = (width // animation_step)
                cut_img = img.subsurface(w_pointer * step_width, 0, step_width,
                                         190)
                dest_img = pygame.Surface((cut_img.get_width() * 2, cut_img.get_height() * 2)).convert_alpha()
                cut_img = pygame.transform.scale2x(
                    cut_img, dest_img
                )
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
        self.running = False

        if not self.attacking and self.alive:
            if self.jump:
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = False
                    self.flip = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = False
                    self.flip = False
                if not key[pygame.K_w]:
                    self.fall = True
                    self.vel_y = 0
                    self.jump = False
                if key[pygame.K_r] or key[pygame.K_t]:
                    if key[pygame.K_r]:
                        self.attacking = True
                        self.attack_type = 1
                    else:
                        self.attacking = True
                        self.attack_type = 2
                    self.attack(surface)

            else:
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
                    self.fall = False
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attacking = True
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    else:
                        self.attack_type = 2
                    self.attack(surface)

        self.vel_y += GRAVITY
        dy += self.vel_y
        if self.rect.bottom + dy > SCREEN_HEIGHT - 100:
            self.vel_y = 0
            self.jump = False
            self.fall = False
            dy = SCREEN_HEIGHT - 100 - self.rect.bottom

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.mana >= 100:
            self.mana = 100
        if self.health <= 0:
            self.mana = 0

        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, action=None, target=None):
        if self.attacking:
            if self.mana > 0:
                self.mana -= 5 # or Skill Mana Cost
            else:
                self.attacking = False
        #     if self.attack_type == 1:
        #         self.image = self.select_image('attack1', 0)
        #     else:
        #         self.image = self.select_image('attack2', 0)

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - self.offset[0] * self.image_scale,
                           self.rect.y - self.offset[1] * self.image_scale))
