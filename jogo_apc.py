
""""

Projeto Final - Parte 1
Descrição: O seguinte programa corresponde a um jogo implementado em Python, em uma grid 10 x 135 na qual os elementos
são representados e constantemente atualizados. O jogo acaba caso o jogador colida com um inimigo ou o combustível termine.

"""
import pygame
import random

# configuracoes_iniciais
pygame.init()
pygame.display.set_caption("JOGO_APC")

tamanho = 5
altura = 10
largura = 135
tela = pygame.display.set_mode((largura * tamanho,
                                altura * tamanho))

clock = pygame.time.Clock()
fps = 20
velocidade = 5
# cores do jogo
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
preto = (0, 0, 0)
verde_escuro = (0, 106, 0)

probX = 7
probF = 4
pontos = 0
combustivel = 400
grid = []
linhas = []

for linha in range(altura):  # criar uma grid (matriz) com espaço para todos os elementos
    for tile in range(largura):
        espaco = ' '
        linhas.append(espaco)
    grid.append(linhas)
    linhas = []

y_inicial = 4
x_inicial = 0

grid[y_inicial][x_inicial] = ['+']  # o jogo começa com somente o jogador, no lado esquerdo da tela


def instrucoes():
    print('- O personagem começa o jogo com pontuação = 0 e combustível = 400')
    print('- Para atirar, pressione a tecla espaço. Se o tiro atingir o inimigo, + 50 pontos')
    print('- Caso o jogador colida com o elemento azul (combustível), este aumenta em 40 unidades ')
    print('- O combustível diminui 2 unidades quando o personagem se move, 3 quando atira e 1 quando fica parado')
    print('- O jogo termina quando o jogador colidir com um inimigo (vermelho) ou quando o combustível terminar')
    print('Bom jogo!')
    exit()


def game_over_colisao(ultima_pontuacao):
    print('\n')
    print("GAME OVER")
    print("Motivo: Colisão com inimigo")
    print(f'Pontuação: {ultima_pontuacao}')


def game_over_combustivel(ultima_pontuacao):
    print('\n')
    print("GAME OVER")
    print("Motivo: Falta de combustível")
    print(f'Pontuação: {ultima_pontuacao}')


def criar_elemento():  # cria uma posição y aleatória para o elemento (no lado direito da tela)
    elemento_y = round(random.randrange(2, altura))
    elemento_x = largura - 1
    coord_elemento = [elemento_x, elemento_y]
    return coord_elemento


def desenhar_elemento(lista_inimigos, lista_combustivel, probabilidade):
    if probabilidade <= probX:  # Resolve problema em que dois elementos eram colocados na mesma posição
        coord_inimigo = criar_elemento()
        lista_inimigos.append(coord_inimigo)
    if probabilidade <= probF:
        coord_combustivel = criar_elemento()
        if coord_combustivel != coord_inimigo:  # dois elementos distintos não podem ser criados na mesma posição!
            lista_combustivel.append(coord_combustivel)
    return lista_inimigos, lista_combustivel


def criar_tiro(posicao_y, posicao_x):  # cria a posição do tiro a partir da posição do jogador no grid
    y_tiro = posicao_y
    x_tiro = posicao_x + 1
    return [x_tiro, y_tiro]


def probabilidade_elementos():  # escolhe um número pseudo-aleatório para usar na criação de elementos
    numero_escolhido = random.randrange(0, 100)
    return numero_escolhido


def atualizar_pontuacao(apaga_inimigo):
    global pontos
    pontos = pontos + (apaga_inimigo * 50)
    fonte = pygame.font.SysFont("Helvetica", 10)
    texto = fonte.render(f'Pontos: {pontos}', True, preto)
    tela.blit(texto, [600, 0])
    return pontos


def atualizar_combustivel(colisao, movimento, parado, tiro):
    global combustivel
    if colisao == 1:
        combustivel += 40
    if movimento == 1:
        combustivel -= 2
    if parado == 1:
        combustivel -= 1
    if tiro == 1:
        combustivel -= 3

    fonte = pygame.font.SysFont("Helvetica", 10)
    texto = fonte.render(f'Combustível: {combustivel}', True, preto)
    tela.blit(texto, [0, 0])
    return combustivel


def start_game():
    lista_inimigos = []
    lista_combustivel = []
    posicoes_tiro = []
    tiro = False
    game_over = False

    posicao_y = y_inicial
    posicao_x = x_inicial

    while not game_over:

        # condições default
        combustivel_colisao = 0
        combustivel_movimento = 0
        combustivel_parado = 1
        combustivel_atirar = 0
        apaga_inimigo = 0
        moveu = False

        tela.fill(branco)

        for event in pygame.event.get():  # pega a entrada do teclado
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if posicao_y > 2:  # limita até onde o x vai
                        grid[posicao_y][posicao_x] = ' '  # deixa o tile onde estava vazio
                        posicao_y -= 1
                        grid[posicao_y][posicao_x] = '+'  # vai pro tile de destino
                        moveu = True
                if event.key == pygame.K_s:
                    if posicao_y < altura - 1:  # limita até onde o x vai
                        grid[posicao_y][posicao_x] = ' '  # deixa o tile onde estava vazio
                        posicao_y += 1
                        grid[posicao_y][posicao_x] = '+'  # vai pro tile de destino
                        moveu = True
                if event.key == pygame.K_SPACE:  # tecla para atirar
                    coordenadas_tiro = criar_tiro(posicao_y, posicao_x)  # cria o tiro na grid
                    posicoes_tiro.append(coordenadas_tiro)  # coloca as posições em uma lista pra atualizar
                    combustivel_atirar = 1  # será descontado do combustível 3pts
                    tiro = True  # a partir da primeira vez que atira, sempre atualiza as posições

        probabilidade = probabilidade_elementos()  # cria um número pseudo-aleatório
        posicoes_inimigo, posicoes_combustivel = desenhar_elemento(lista_inimigos, lista_combustivel, probabilidade)
        # cria novos elementos, tanto inimigo como combustível

        if moveu == True:
            combustivel_movimento = 1  # vão ser descontados 2pts do combustível
            combustivel_parado = 0  # o ponto por ficar parado não vai ser descontado

        if tiro == True:
            for posicao_t in posicoes_tiro:  # atualiza as posições de tiro na grid e na janela pygame
                if posicao_t[0] < 135:  # a grid vai de 0 a 134
                    if grid[posicao_t[1]][posicao_t[0]] == ' ':  # se não tiver nada na frente
                        pygame.draw.rect(tela, verde_escuro, [posicao_t[0] * 5, posicao_t[1] * 5, tamanho, tamanho])
                        grid[posicao_t[1]][posicao_t[0] - 1] = ' '  # deixa o espaço onde estava vazio
                        grid[posicao_t[1]][posicao_t[0]] = 'T'  # ocupa o próximo espaço na grid
                        posicao_t[0] += 1  # atualiza o x para o próximo loop
                    else:
                        grid[posicao_t[1]][posicao_t[0]] = ' '  # colidiu, então esvazia o tile da frente
                        posicao_t[0] = 136  # joga pra fora da grid, a posição não é mais atualizada (x não é válido)
                elif posicao_t[0] == 135:   # se o tiro chega no fim da grid sem acertar nada
                    grid[posicao_t[1]][posicao_t[0] - 1] = ' '  # esvazia o ultimo tile que ocupou (x = 134)
                    posicao_t[0] = 136      # joga pra fora da grid

        for posicao_i in posicoes_inimigo:
            if grid[posicao_i[1]][posicao_i[0]] == '+':  # se o personagem colidir com o inimigo, GAME OVER
                game_over_colisao(pontos)
                game_over = True
            if posicao_i[0] != -2:  # o X chega a -2 (precisa chegar ao -1 pra esvaziar o tile do 0)
                if grid[posicao_i[1]][posicao_i[0]] == 'T':  # se encontrar um tiro
                    grid[posicao_i[1]][posicao_i[0]] = ' '   # esvazia o próximo tile
                    posicao_i[0] = -2  # elimina o elemento da grid, não é mais atualizado (não tem um x válido)
                    apaga_inimigo = 1  # aumentar a pontuação em 50 pts
                else:
                    pygame.draw.rect(tela, vermelho, [posicao_i[0] * 5, posicao_i[1] * 5, tamanho, tamanho])
                    if posicao_i[0] != 134:  # quanto está no primeiro tile da direita ele não esvazia o tile atrás
                        grid[posicao_i[1]][posicao_i[0] + 1] = ' '
                    grid[posicao_i[1]][posicao_i[0]] = 'X'  # coloca no tile da frente
                    posicao_i[0] -= 1

        for posicao_c in posicoes_combustivel:
            if grid[posicao_c[1]][posicao_c[0]] == '+':  # se o personagem colidir com combustivel, 1
                grid[posicao_c[1]][posicao_c[0] + 1] = ' '  # tile atrás fica vazio
                posicao_c[0] = -1  # coloca o elemento pra fora da grid (x não válido)
                combustivel_colisao = 1
            else:
                if posicao_c[0] != -1:
                    if grid[posicao_c[1]][posicao_c[0]] == 'T':  # se o elemento à frente for um tiro
                        grid[posicao_c[1]][posicao_c[0]] = ' '  # elemento a frente vira vazio
                        posicao_c[0] = -1  # elimina o elemento da grid, não é mais atualizado (não tem um x válido)
                    else:
                        pygame.draw.rect(tela, azul, [posicao_c[0] * 5, posicao_c[1] * 5, tamanho, tamanho])
                        if posicao_c[0] != 134:
                            grid[posicao_c[1]][posicao_c[0] + 1] = ' '
                        grid[posicao_c[1]][posicao_c[0]] = 'F'
                        posicao_c[0] -= 1

        pygame.draw.rect(tela, verde, [posicao_x * 5, posicao_y * 5, tamanho, tamanho])
        pontos = atualizar_pontuacao(apaga_inimigo) # atualizar a pontuação mostrada
        combustivel = atualizar_combustivel(combustivel_colisao, combustivel_movimento, combustivel_parado,
                                            combustivel_atirar)  # atualizar o combustível

        if combustivel <= 0:  # condição GAME OVER
            game_over_combustivel(pontos)
            game_over = True

        clock.tick(fps)
        pygame.display.flip()


def menu():
    print("1 - Jogar")
    print("2 - Configuracoes")
    print("3 - Ranking")
    print("4 - Instrucoes")
    print("5 - Sair")

    escolha = int(input("Escolha uma opção:"))
    return escolha


print("JOGO APC")
input()

match menu():
    case 1: start_game()
    #   case 2: configuracoes()
    #   case 3: ranking()
    case 4: instrucoes()
    case 5: exit()
