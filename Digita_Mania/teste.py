import pygame
import sys
import constantes
from sprite import Bolha

class Game():
    def __init__(self):
        self.iniciar()

    def iniciar(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constantes.ALTURA, constantes.LARGURA))
        self.fundo_image()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("DigitaMania")
        self.gerenciar_sprite()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(constantes.PRETO)
            self.screen.blit(self.bg, (0, 0))

            self.bolhas.update()
            self.bolhas.draw(self.screen)
            
            # Desenha as letras dentro das bolhas
            for bolha in self.bolhas:
                self.screen.blit(bolha.texto, bolha.texto_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def fundo_image(self):
        self.bg = pygame.image.load(constantes.BG).convert()
        self.bg = pygame.transform.scale(self.bg, (constantes.ALTURA, constantes.LARGURA))

    def gerenciar_sprite(self):
        self.bolhas = pygame.sprite.Group()
        for _ in range(5):
            while True:
                nova_bolha = Bolha()
                if not pygame.sprite.spritecollideany(nova_bolha, self.bolhas):
                    self.bolhas.add(nova_bolha)
                    break

import pygame
import constantes
import random

class Bolha(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(constantes.BOLHA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constantes.ALTURA_BOLHA, constantes.LARGURA_BOLHA))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, constantes.LARGURA - self.rect.width)
        self.rect.y = random.randint(-constantes.ALTURA, 0)  # Bolhas começam acima da tela

        self.letra = random.choice(constantes.LETRAS)
        self.fonte = pygame.font.Font(constantes.FONTE, 29)
        self.texto = self.fonte.render(self.letra, True, (255, 0, 0))
        self.texto_rect = self.texto.get_rect()
        self.texto_rect.center = self.rect.center

    def update(self):
        self.rect.y += constantes.VELOCIDADE
        self.texto_rect.center = self.rect.center

        if self.rect.top > constantes.ALTURA:
            self.rect.x = random.randint(0, constantes.LARGURA - self.rect.width)
            self.rect.y = random.randint(-constantes.ALTURA, 0)
            self.texto_rect.center = self.rect.center

if __name__ == "__main__":
    Game()

