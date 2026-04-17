import pygame  # importa a biblioteca pygame
import sys  # importa a biblioteca sys
import random  # importa a biblioteca random para gerar valores aleatórios

# -----------------------------  
# Inicialização  
# -----------------------------  
pygame.init()  # inicializa o pygame

LARGURA = 800  # define a largura da janela
ALTURA = 600  # define a altura da janela

tela = pygame.display.set_mode((LARGURA, ALTURA))  # cria a janela do jogo
pygame.display.set_caption("Aula 2 - Inimigos e Colisão")  # define o título da janela

clock = pygame.time.Clock()  # cria o relógio de controle dos FPS

# -----------------------------  
# Cores  
# -----------------------------  
BRANCO = (255, 255, 255)  # define a cor branca
AZUL = (50, 100, 255)  # define a cor azul
VERMELHO = (200, 50, 50)  # define a cor vermelha
PRETO = (0, 0, 0)  # define a cor preta

# -----------------------------  
# Fonte e função auxiliar  
# -----------------------------  
fonte = pygame.font.SysFont(None, 36)  # cria a fonte padrão

def desenhar_texto(texto, x, y, cor=PRETO):  # função para desenhar texto
    img = fonte.render(texto, True, cor)  # renderiza o texto
    tela.blit(img, (x, y))  # desenha o texto na tela

# -----------------------------  
# Jogador  
# -----------------------------  
jogador_largura = 60  # define a largura do jogador
jogador_altura = 60  # define a altura do jogador
jogador_x = LARGURA // 2 - jogador_largura // 2  # centraliza o jogador horizontalmente
jogador_y = ALTURA - 100  # posiciona o jogador na parte inferior
velocidade_jogador = 20  # define a velocidade do jogador
vidas = 10  # define a quantidade inicial de vidas

# -----------------------------  
# Classe Inimigo  
# -----------------------------  
class Inimigo:  # cria a classe do inimigo
    def __init__(self):  # método construtor da classe
        self.largura = 50  # define a largura do inimigo
        self.altura = 50  # define a altura do inimigo
        self.resetar()  # chama a função que posiciona o inimigo

    def resetar(self):  # função para reposicionar o inimigo
        self.x = random.randint(0, LARGURA - self.largura)  # sorteia a posição X
        self.y = random.randint(-300, -50)  # sorteia a posição Y acima da tela
        self.vel = random.randint(10, 13)  # sorteia a velocidade do inimigo

    def mover(self):  # função que move o inimigo
        self.y += self.vel  # move o inimigo para baixo

    def desenhar(self):  # função que desenha o inimigo
        pygame.draw.rect(tela, VERMELHO, (self.x, self.y, self.largura, self.altura))  # desenha o inimigo como retângulo vermelho

    def get_rect(self):  # função que retorna o retângulo do inimigo
        return pygame.Rect(self.x, self.y, self.largura, self.altura)  # cria e devolve a área do inimigo

inimigos = [Inimigo() for _ in range(5)]  # cria uma lista com 5 inimigos

# -----------------------------  
# Loop principal  
# -----------------------------  
while True:  # inicia o loop principal
    for evento in pygame.event.get():  # percorre os eventos da janela
        if evento.type == pygame.QUIT:  # verifica se o usuário fechou a janela
            pygame.quit()  # fecha o pygame
            sys.exit()  # encerra o programa

    teclas = pygame.key.get_pressed()  # lê as teclas pressionadas

    if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jogador_x > 0:  # se a seta esquerda estiver pressionada e o jogador não sair da tela
        jogador_x -= velocidade_jogador  # move o jogador para a esquerda

    if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jogador_x < LARGURA - jogador_largura:  # se a seta direita estiver pressionada e o jogador não sair da tela
        jogador_x += velocidade_jogador  # move o jogador para a direita

    jogador_rect = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)  # cria o retângulo do jogador para calcular colisão

    # -----------------------------  
    # Atualização dos inimigos  
    # -----------------------------  
    for inimigo in inimigos:  # percorre todos os inimigos
        inimigo.mover()  # move o inimigo

        if jogador_rect.colliderect(inimigo.get_rect()):  # verifica colisão entre jogador e inimigo
            vidas += 1  # retira uma vida do jogador
            inimigo.resetar()  # reposiciona o inimigo no topo

        elif inimigo.y > ALTURA:  # verifica se o inimigo saiu pela parte inferior da tela
            vidas -= 1  # retira uma vida do jogador
            inimigo.resetar()  # reposiciona o inimigo

    if vidas <= 0:  # verifica se o jogador ficou sem vidas
        pygame.quit()  # encerra o pygame
        sys.exit()  # encerra o programa

    # -----------------------------  
    # Desenho na tela  
    # -----------------------------  
    tela.fill(BRANCO)  # pinta o fundo da tela de branco
    pygame.draw.rect(tela, AZUL, (jogador_x, jogador_y, jogador_largura, jogador_altura))  # desenha o jogador

    for inimigo in inimigos:  # percorre cada inimigo
        inimigo.desenhar()  # desenha o inimigo na tela

    desenhar_texto(f"Vidas: {vidas}", 20, 20)  # mostra o número de vidas
    desenhar_texto("Desvie dos inimigos", 20, 60)  # mostra uma instrução na tela

    pygame.display.flip()  # atualiza a tela
    clock.tick(60)  # mantém o jogo em 60 FPS