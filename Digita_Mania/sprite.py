import pygame
import constantes
import random

class Bolha(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(constantes.BOLHA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constantes.ALTURA_BOLHA, constantes.LARGURA_BOLHA))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(-80, constantes.ALTURA)
        self.rect.y = -80

        self.letra = random.choice(constantes.LETRAS)                      # Seleciona uma letra aleatória para exibir dentro da bolha
        self.fonte = pygame.font.Font(constantes.FONTE, 29)                # Configurações de fonte para a letra
        self.texto = self.fonte.render(self.letra, True, (255, 0, 0))
        self.texto_rect = self.texto.get_rect()
        self.texto_rect.center = self.rect.center


    def update(self):
        self.rect.y += constantes.VELOCIDADE
        self.texto_rect.center = self.rect.center
        self.texto_rect.y += constantes.VELOCIDADE

        if self.rect.top > constantes.ALTURA:
            self.rect.x = random.randint(0, constantes.LARGURA - self.rect.width)
            self.rect.y = 0
            self.rect.y = -self.rect.height
            self.texto_rect.center = self.rect.center
            self.texto_rect.y = self.rect.y



           