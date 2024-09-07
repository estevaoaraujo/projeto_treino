import pygame
import sys 
import constantes
from sprite import Bolha


class Game():
    def __init__(self):
        self.iniciar()

    def iniciar(self):
        pygame.init()                                                                    # Inicializa todas as funções do Pygame
        self.screen = pygame.display.set_mode((constantes.ALTURA, constantes.LARGURA))   # Cria a janela do jogo com o tamanho especificado 
        self.fundo_image()                                                               # Cria imagem de fundo 
        self.clock = pygame.time.Clock()                                                 # Controle do FPS
        pygame.display.set_caption("DigitaMania")                                        # Define o título da janela do jogo
        self.gerenciar_sprite()

        running = True                                                                          
        while running:                                                                   # Loop principal do jogo
            # Verifica os eventos do jogo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # RENDER SEU JOGO AQUI
            self.screen.fill(constantes.PRETO)                                           # Preenche a janela com a cor de fundo
            self.screen.blit(self.bg, (0, 0))                                            # Desenha a imagem na tela 

            self.bolhas.update()                                                         # para atualizar todos os sprites no grupo. Este método é usado para mover os sprites, atualizar suas animações, etc
            self.bolhas.draw(self.screen)                                                # Para desenhar todos os sprites do grupo na tela.
            self.aparece_bolhas_na_tela()

            pygame.display.flip()                                                        # Atualiza o conteúdo da janela        
            self.clock.tick(60)                                                          # limits FPS to 60

        pygame.quit()
        sys.exit()  

    def fundo_image(self):
        self.bg = pygame.image.load(constantes.BG).convert()                                  # convert ajuda na adqueção da imagem
        self.bg = pygame.transform.scale(self.bg, (constantes.ALTURA, constantes.LARGURA))     # Redimensiona a imagem                                                           

    def gerenciar_sprite(self):
        self.bolhas = pygame.sprite.Group()                                              # Grupo para armazenar as bolhas
        for _ in range(5):                                                               # Criar 10 bolhas
            bolha = Bolha()
            self.bolhas.add(bolha)

    def aparece_bolhas_na_tela(self):
        for bolha in self.bolhas:
            self.screen.blit(bolha.image, bolha.rect)
            self.screen.blit(bolha.texto, bolha.texto_rect)

       