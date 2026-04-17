import pygame  # importa a biblioteca pygame para criação do jogo
import sys  # importa a biblioteca sys para encerrar o programa

# -----------------------------  
# Inicialização  
# -----------------------------  
pygame.init()  # inicializa os módulos principais do pygame

LARGURA = 800  # define a largura da janela
ALTURA = 600  # define a altura da janela

tela = pygame.display.set_mode((LARGURA, ALTURA))  # cria a janela do jogo
pygame.display.set_caption("Aula 1 - Movimento do Jogador")  # define o título da janela

clock = pygame.time.Clock()  # cria um relógio para controlar os FPS

# -----------------------------  
# Cores  
# -----------------------------  
BRANCO = (255, 255, 255)  # define a cor branca
AZUL = (50, 100, 255)  # define a cor azul
PRETO = (0, 0, 0)  # define a cor preta

# -----------------------------  
# Jogador  
# -----------------------------  
jogador_largura = 60  # define a largura do jogador
jogador_altura = 60  # define a altura do jogador
jogador_x = LARGURA // 2 - jogador_largura // 2  # posiciona o jogador no centro horizontal
jogador_y = ALTURA - 10 - jogador_altura  # posiciona o jogador na parte inferior da tela
velocidade = 20  # define a velocidade de movimento do jogador

# -----------------------------  
# Fonte e função auxiliar  
# -----------------------------  
fonte = pygame.font.SysFont(None, 36)  # cria uma fonte para mostrar texto na tela

def desenhar_texto(texto, x, y, cor=PRETO):  # função para desenhar texto na tela
    img = fonte.render(texto, True, cor)  # transforma o texto em imagem
    tela.blit(img, (x, y))  # desenha o texto na posição desejada

# -----------------------------  
# Loop principal  
# -----------------------------  
while True:  # inicia o loop principal do jogo
    for evento in pygame.event.get():  # percorre todos os eventos da janela
        if evento.type == pygame.QUIT:  # verifica se o usuário fechou a janela
            pygame.quit()  # encerra o pygame
            sys.exit()  # encerra o programa

    teclas = pygame.key.get_pressed()  # captura o estado atual das teclas do teclado

    if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jogador_x > 0:  # se a seta esquerda estiver pressionada e o jogador não saiu da tela
        jogador_x -= velocidade  # move o jogador para a esquerda

    if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jogador_x < LARGURA - jogador_largura:  # se a seta direita estiver pressionada e o jogador não saiu da tela
        jogador_x += velocidade  # move o jogador para a direita
    
    # Nao deixar jogador sair da tela
    #(verifique se a indentacao esta certa)
    if jogador_x < 0:
        jogador_x = 0
    elif jogador_x > LARGURA - jogador_altura:
        jogador_x = LARGURA - jogador_altura
    
    # -----------------------------  
    # Desenho na tela  
    # -----------------------------  
    tela.fill(BRANCO)  # pinta o fundo da tela de branco
    pygame.draw.rect(tela, AZUL, (jogador_x, jogador_y, jogador_largura, jogador_altura))  # desenha o jogador como um retângulo azul
    desenhar_texto("Use as setas ou as teclas 'a' e 'd' para mover", 20, 20)  # desenha uma instrução na tela

    pygame.display.flip()  # atualiza a tela com todos os desenhos feitos
    clock.tick(60)  # limita o jogo a 60 quadros por segundo, pausando a apresentatação caso necessário