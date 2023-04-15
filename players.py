"""
Classe que conterá todos os caracteres jogáveis.
"""
import pygame


class Helena:
    animation_steps = [8, 8, 7, 2, 4, 6, 2, 8]

    def __init__(self, sprites):
        self.size = None
        self.sprites = sprites
        self.image_scale = 2
        self.name = "Helena"
        self.images = self.load_images(self.sprites)
        self.image = self.images['idle'][0]#pygame.Surface((50, 50))
        # self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

    def load_images(self, sprites):
        animation_dict = {}
        for x, animation_step in enumerate(self.animation_steps):
            animation_list = []
            for w_pointer in range(animation_step):
                action, img = list(sprites.items())[x]
                width, y = img.get_size()
                step_width = (width // animation_step)
                cut_img = img.subsurface(w_pointer*step_width, 0, step_width, 190)
                animation_list.append(cut_img)
            animation_dict[action] = animation_list
        return animation_dict

    def select_image(self, action, num):
        return self.image
