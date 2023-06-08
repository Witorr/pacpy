import os
import time
import random

class SimulacaoPacman:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.matrix = [['.' for _ in range(colunas)] for _ in range(linhas)]
        self.p_atual = self.definir_posicao_inicial()
        self.iteracao = 0
        self.p_anterior = None
        self.num_inimigos = 3 # Quantidade de Inimigos
        self.gerar_inimigos()
        

    def definir_posicao_inicial(self):
        posicoes_disponiveis = [(i, j) for i in range(self.linhas) for j in range(self.colunas)]
        return random.choice(posicoes_disponiveis)
    
    def gerar_inimigos(self):
        posicoes_disponiveis = [(i, j) for i in range(self.linhas) for j in range(self.colunas)]
        posicoes_inimigos = random.sample(posicoes_disponiveis, self.num_inimigos)
        for pos in posicoes_inimigos:
            self.matrix[pos[0]][pos[1]] = '@'

    def mover(self):
        i, j = self.p_atual
        self.matrix[i][j] = 'O' if self.iteracao % 2 == 0 else 'o'

        comida_proxima = self.encontrar_comida_proxima()
        if comida_proxima is None:
            return

        comida_linha, comida_coluna = comida_proxima
        if i < comida_linha:
            self.p_anterior = self.p_atual
            self.p_atual = i + 1, j
        elif i > comida_linha:
            self.p_anterior = self.p_atual
            self.p_atual = i - 1, j
        elif j < comida_coluna:
            self.p_anterior = self.p_atual
            self.p_atual = i, j + 1
        elif j > comida_coluna:
            self.p_anterior = self.p_atual
            self.p_atual = i, j - 1

        self.iteracao += 1
        
    def colisao_inimigo(self):
        i, j = self.p_atual
        if self.matrix[i][j] == '@':
            return True
        return False

    def encontrar_comida_proxima(self):
        posicao_pacman = self.p_atual
        posicoes_comida = []

        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.matrix[i][j] == 'X':
                    posicoes_comida.append((i, j))

        if not posicoes_comida:
            return None

        comida_proxima = min(posicoes_comida, key=lambda pos: self.distancia(posicao_pacman, pos))
        return comida_proxima

    def distancia(self, pos1, pos2):
        i1, j1 = pos1
        i2, j2 = pos2
        return abs(i1 - i2) + abs(j1 - j2)

    def coletar_comida(self):
        i, j = self.p_atual
        if self.matrix[i][j] == 'X':
            self.matrix[i][j] = '.'

    def restaurar_p_anterior(self):
        if self.p_anterior is not None:
            i, j = self.p_anterior
            self.matrix[i][j] = '.'

    def simular_movimento(self):
        while 'X' in [item for linha in self.matrix for item in linha]:
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal após cada iteração - Requisito atendido
            self.restaurar_p_anterior()
            self.mover()
            if self.colisao_inimigo(): # Colisão Ativada
                break
            self.coletar_comida()
            self.exibir_matrix()
            time.sleep(0.6)  # Use “sleep(0.6)” para o computador aguardar por 60 ms - Requisito atendido

    def exibir_matrix(self):
        for linha in self.matrix:
            print(' '.join(linha))

# Tamanho da Hub
linhas = 8
colunas = 10

# Bota o Pac pra rodar
pacman = SimulacaoPacman(linhas, colunas)

# Adiciona comidas de maneira aleatórias para o Pacman
NUM_COMIDAS = 3
posicoes_disponiveis = [(i, j) for i in range(linhas) for j in range(colunas)]
comidas = random.sample(posicoes_disponiveis, NUM_COMIDAS)
for comida in comidas:
    pacman.matrix[comida[0]][comida[1]] = 'X'

# Simular o movimento do Pacman
pacman.simular_movimento()
