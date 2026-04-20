import pygame  # importa a biblioteca pygame
import sys  # importa a biblioteca sys
import random  # importa a biblioteca random

# -----------------------------  
# Inicialização  
# -----------------------------  
pygame.init()  # inicializa os módulos do pygame
pygame.mixer.init()  # inicializa o sistema de áudio

# Música de fundo  
pygame.mixer.music.load("assets/musica_fundo.ogg")  # carrega a música de fundo
pygame.mixer.music.set_volume(0.4)  # define o volume da música
pygame.mixer.music.play(-1)  # toca a música em loop infinito

# Efeito do tiro  
som_tiro = pygame.mixer.Sound("assets/tiro.wav")  # carrega o som do tiro
som_tiro.set_volume(0.6)  # define o volume do som do tiro

LARGURA = 800  # define a largura da janela
ALTURA = 600  # define a altura da janela

tela = pygame.display.set_mode((LARGURA, ALTURA))  # cria a janela do jogo
pygame.display.set_caption("Jogo com Sprites, Tiros e Timer")  # define o título da janela

clock = pygame.time.Clock()  # cria um relógio para controlar os FPS

# -----------------------------  
# Cores  
# -----------------------------  
BRANCO = (255, 255, 255)  # define a cor branca
PRETO = (0, 0, 0)  # define a cor preta
VERMELHO = (200, 50, 50)  # define a cor vermelha
AZUL = (50, 100, 255)  # define a cor azul
AMARELO = (255, 220, 0)  # define a cor amarela

# -----------------------------  
# Fontes  
# -----------------------------  
fonte = pygame.font.SysFont(None, 36)  # cria a fonte padrão
fonte_titulo = pygame.font.SysFont(None, 64)  # cria uma fonte maior para títulos

# -----------------------------  
# Carregar imagens  
# -----------------------------  
jogador_img = pygame.image.load("assets/jogador.png").convert_alpha()  # carrega a imagem do jogador com transparência
inimigo_img = pygame.image.load("assets/inimigo.png").convert_alpha()  # carrega a imagem do inimigo com transparência
fundo_img = pygame.image.load("assets/fundo.png").convert()  # carrega a imagem de fundo

# Escalas  
jogador_largura = 60  # define a largura do jogador
jogador_altura = 60  # define a altura do jogador
inimigo_largura = 50  # define a largura do inimigo
inimigo_altura = 50  # define a altura do inimigo

jogador_img = pygame.transform.scale(jogador_img, (jogador_largura, jogador_altura))  # redimensiona a imagem do jogador
inimigo_img = pygame.transform.scale(inimigo_img, (inimigo_largura, inimigo_altura))  # redimensiona a imagem do inimigo
fundo_img = pygame.transform.scale(fundo_img, (LARGURA, ALTURA))  # redimensiona o fundo para o tamanho da tela

# -----------------------------  
# Funções auxiliares  
# -----------------------------  
def desenhar_texto(texto, fonte, cor, x, y):  # função que desenha um texto na tela
    img = fonte.render(texto, True, cor)  # renderiza o texto
    tela.blit(img, (x, y))  # desenha o texto na posição desejada


def tela_inicial():  # função que exibe a tela inicial
    while True:  # mantém a tela inicial em repetição
        for evento in pygame.event.get():  # percorre os eventos da janela
            if evento.type == pygame.QUIT:  # verifica se o usuário fechou a janela
                pygame.quit()  # encerra o pygame
                sys.exit()  # encerra o programa
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:  # verifica se o jogador apertou espaço
                return  # sai da tela inicial e inicia o jogo

        tela.fill(BRANCO)  # pinta o fundo de branco
        desenhar_texto("JOGO EM PYGAME", fonte_titulo, PRETO, 180, 200)  # desenha o título principal
        desenhar_texto("Setas: mover | Espaço: atirar", fonte, AZUL, 220, 300)  # desenha as instruções
        desenhar_texto("Pressione ESPAÇO para começar", fonte, AZUL, 220, 340)  # desenha a mensagem para iniciar

        pygame.display.flip()  # atualiza a tela
        clock.tick(60)  # mantém 60 FPS


def tela_game_over(pontos):  # função que exibe a tela de fim de jogo
    while True:  # mantém a tela de game over em repetição
        for evento in pygame.event.get():  # percorre os eventos da janela
            if evento.type == pygame.QUIT:  # verifica se o usuário fechou a janela
                pygame.quit()  # encerra o pygame
                sys.exit()  # encerra o programa
            if evento.type == pygame.KEYDOWN:  # verifica se alguma tecla foi pressionada
                if evento.key == pygame.K_r:  # verifica se a tecla foi R
                    return  # reinicia o jogo
                if evento.key == pygame.K_ESCAPE:  # verifica se a tecla foi ESC
                    pygame.quit()  # encerra o pygame
                    sys.exit()  # encerra o programa

        tela.fill(BRANCO)  # pinta o fundo da tela de branco
        desenhar_texto("GAME OVER", fonte_titulo, VERMELHO, 250, 200)  # mostra o título de fim de jogo
        desenhar_texto(f"Pontuação: {pontos}", fonte, PRETO, 320, 300)  # mostra a pontuação final
        desenhar_texto("R = Reiniciar | ESC = Sair", fonte, AZUL, 250, 360)  # mostra as opções do jogador

        pygame.display.flip()  # atualiza a tela
        clock.tick(60)  # mantém 60 FPS

# -----------------------------  
# Classes  
# -----------------------------  
class Inimigo:  # classe que representa o inimigo
    def __init__(self):  # construtor da classe
        self.resetar()  # inicializa posição e velocidade do inimigo

    def resetar(self):  # função que reposiciona o inimigo
        self.x = random.randint(0, LARGURA - inimigo_largura)  # sorteia a posição X do inimigo
        self.y = random.randint(-300, -50)  # sorteia a posição Y acima da tela
        self.vel = random.randint(3, 6)  # sorteia a velocidade do inimigo

    def mover(self):  # função que move o inimigo
        self.y += self.vel  # move o inimigo para baixo

    def desenhar(self):  # função que desenha o inimigo
        tela.blit(inimigo_img, (self.x, self.y))  # desenha a imagem do inimigo

    def get_rect(self):  # função que retorna a área retangular do inimigo
        return pygame.Rect(self.x, self.y, inimigo_largura, inimigo_altura)  # devolve o retângulo do inimigo


class Tiro:  # classe que representa o tiro
    def __init__(self, x, y):  # construtor da classe
        self.largura = 6  # define a largura do tiro
        self.altura = 18  # define a altura do tiro
        self.x = x  # guarda a posição X do tiro
        self.y = y  # guarda a posição Y do tiro
        self.vel = 10  # define a velocidade do tiro

    def mover(self):  # função que move o tiro
        self.y -= self.vel  # move o tiro para cima

    def desenhar(self):  # função que desenha o tiro
        pygame.draw.rect(tela, AMARELO, (self.x, self.y, self.largura, self.altura))  # desenha o tiro como retângulo amarelo

    def get_rect(self):  # função que retorna a área retangular do tiro
        return pygame.Rect(self.x, self.y, self.largura, self.altura)  # devolve o retângulo do tiro

# -----------------------------  
# Loop do jogo  
# -----------------------------  
def jogar(vidas_iniciais=100, tempo_total=60):  # função principal que executa a partida
    
    jogador_x = 370  # define a posição inicial X do jogador
    jogador_y = 500  # define a posição inicial Y do jogador
    velocidade_jogador = 6  # define a velocidade do jogador

    pontos = 0  # inicia a pontuação com zero
    vidas = vidas_iniciais  # define as vidas iniciais

    inimigos = [Inimigo() for _ in range(5)]  # cria uma lista com 5 inimigos
    tiros = []  # cria uma lista vazia de tiros

    tempo_entre_tiros = 250  # define o intervalo mínimo entre tiros
    ultimo_tiro = 0  # armazena o tempo do último tiro

    # Marca o instante inicial da partida  # comentário original de apoio didático
    inicio_partida = pygame.time.get_ticks()  # registra o instante inicial da partida

    while True:  # inicia o loop principal da partida
        for evento in pygame.event.get():  # percorre os eventos da janela
            if evento.type == pygame.QUIT:  # verifica se o usuário fechou a janela
                pygame.quit()  # encerra o pygame
                sys.exit()  # encerra o programa

            if evento.type == pygame.KEYDOWN:  # verifica se uma tecla foi pressionada
                if evento.key == pygame.K_SPACE:  # verifica se a tecla foi espaço
                    agora = pygame.time.get_ticks()  # captura o tempo atual
                    if agora - ultimo_tiro >= tempo_entre_tiros:  # verifica se já pode atirar novamente
                        tiro_x = jogador_x + jogador_largura // 2 - 3  # calcula a posição X do tiro
                        tiro_y = jogador_y  # define a posição Y do tiro
                        tiros.append(Tiro(tiro_x, tiro_y))  # cria um tiro e adiciona à lista
                        som_tiro.play()  # toca o som do tiro
                        ultimo_tiro = agora  # atualiza o instante do último tiro

        teclas = pygame.key.get_pressed()  # lê o estado atual do teclado

        if teclas[pygame.K_LEFT] and jogador_x > 0:  # verifica movimento para a esquerda
            jogador_x -= velocidade_jogador  # move o jogador para a esquerda

        if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - jogador_largura:  # verifica movimento para a direita
            jogador_x += velocidade_jogador  # move o jogador para a direita

        # -----------------------------  
        # Controle de tempo  
        # -----------------------------  
        agora = pygame.time.get_ticks()  # pega novamente o tempo atual
        tempo_decorrido = (agora - inicio_partida) / 1000  # calcula quantos segundos já passaram
        tempo_restante = max(0, int(tempo_total - tempo_decorrido))  # calcula o tempo restante da partida

        # Fundo  
        tela.blit(fundo_img, (0, 0))  # desenha a imagem de fundo

        # Jogador  
        tela.blit(jogador_img, (jogador_x, jogador_y))  # desenha a imagem do jogador
        jogador_rect = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)  # cria a área retangular do jogador

        # Tiros  
        for tiro in tiros[:]:  # percorre uma cópia da lista de tiros
            tiro.mover()  # move o tiro

            if tiro.y < 0:  # verifica se o tiro saiu da tela
                tiros.remove(tiro)  # remove o tiro da lista
            else:  # caso o tiro ainda esteja na tela
                tiro.desenhar()  # desenha o tiro

        # Inimigos  
        for inimigo in inimigos:  # percorre os inimigos
            inimigo.mover()  # move o inimigo
            inimigo.desenhar()  # desenha o inimigo

            if jogador_rect.colliderect(inimigo.get_rect()):  # verifica colisão entre jogador e inimigo
                vidas -= 1  # reduz uma vida
                inimigo.resetar()  # reposiciona o inimigo

            elif inimigo.y > ALTURA:  # verifica se o inimigo passou da parte inferior
                vidas -= 1  # reduz uma vida
                inimigo.resetar()  # reposiciona o inimigo

            for tiro in tiros[:]:  # percorre uma cópia da lista de tiros
                if tiro.get_rect().colliderect(inimigo.get_rect()):  # verifica colisão entre tiro e inimigo
                    pontos += 10  # soma 10 pontos
                    vidas += 1  # recompensa o jogador com uma vida
                    inimigo.resetar()  # reposiciona o inimigo
                    tiros.remove(tiro)  # remove o tiro que acertou
                    break  # interrompe o laço interno

        # HUD  
        desenhar_texto(f"Pontos: {pontos}", fonte, PRETO, 20, 20)  # mostra a pontuação
        desenhar_texto(f"Vidas: {vidas}", fonte, PRETO, 20, 60)  # mostra as vidas
        desenhar_texto(f"Tiros: {len(tiros)}", fonte, PRETO, 20, 100)  # mostra a quantidade de tiros ativos
        desenhar_texto(f"Tempo: {tempo_restante}s", fonte, PRETO, 20, 140)  # mostra o tempo restante

        pygame.display.flip()  # atualiza a tela
        clock.tick(60)  # mantém o jogo em 60 FPS

        if vidas <= 0 or tempo_restante <= 0:  # verifica se a partida terminou
            return pontos  # retorna a pontuação final

# -----------------------------  
# Execução principal  
# -----------------------------  
while True:  # mantém o programa rodando para permitir reinício
    tela_inicial()  # exibe a tela inicial
    pontuacao = jogar(vidas_iniciais=100, tempo_total=60)  # executa a partida
    tela_game_over(pontuacao)  # exibe a tela de game over