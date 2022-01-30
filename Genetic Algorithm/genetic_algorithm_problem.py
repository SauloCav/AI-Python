from random import randint

class Genetic_Algorithm():

    def __init__(self, x_min, x_max, tam_populacao, taxa_mutacao, taxa_crossover, num_geracoes):
       
        self.x_min = x_min
        self.x_max = x_max
        self.tam_populacao = tam_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.num_geracoes = num_geracoes

        qtd_bits_x_min = len(bin(x_min).replace('0b', '' if x_min < 0 else '+'))
        qtd_bits_x_max = len(bin(x_max).replace('0b', '' if x_max < 0 else '+'))

        self.num_bits = qtd_bits_x_max if qtd_bits_x_max >= qtd_bits_x_min else qtd_bits_x_min
        self._gerar_populacao()


    def _gerar_populacao(self):

        self.populacao = [[] for i in range(self.tam_populacao)]

        for individuo in self.populacao:
            num = randint(self.x_min, self.x_max)
            num_bin = bin(num).replace('0b', '' if num < 0 else '+').zfill(self.num_bits)

            for bit in num_bin:
                individuo.append(bit)


    def _funcao_objetivo(self, num_bin):

        num = int(''.join(num_bin), 2)

        return num**2 -3*num + 4


    def avaliar(self):

        self.avaliacao = []

        for individuo in self.populacao:
            self.avaliacao.append(self._funcao_objetivo(individuo))


    def selecionar(self):

        participantes_torneio = list(zip(self.populacao, self.avaliacao))
        individuo_1 = participantes_torneio[randint(0, self.tam_populacao - 1)]
        individuo_2 = participantes_torneio[randint(0, self.tam_populacao - 1)]

        return individuo_1[0] if individuo_1[1] >= individuo_2[1] else individuo_2[0]


    def _ajustar(self, individuo):

        if int(''.join(individuo), 2) < self.x_min:
            ajuste = bin(self.x_min).replace('0b', '' if self.x_min < 0 else '+').zfill(self.num_bits)
            for indice, bit in enumerate(ajuste):
                individuo[indice] = bit
        elif int(''.join(individuo), 2) > self.x_max:
            ajuste = bin(self.x_max).replace('0b', '' if self.x_max < 0 else '+').zfill(self.num_bits)
            for indice, bit in enumerate(ajuste):
                individuo[indice] = bit


    def crossover(self, pai, mae):

        if randint(1,100) <= self.taxa_crossover:
            ponto_de_corte = randint(1, self.num_bits - 1)
            filho_1 = pai[:ponto_de_corte] + mae[ponto_de_corte:]
            filho_2 = mae[:ponto_de_corte] + pai[ponto_de_corte:]
            self._ajustar(filho_1)
            self._ajustar(filho_2)    
        else:
            filho_1 = pai[:]
            filho_2 = mae[:]

        return (filho_1, filho_2)

    def mutar(self, individuo):

        tabela_mutacao = str.maketrans('+-01', '-+10')

        if randint(1,100) <= self.taxa_mutacao:
            bit = randint(0, self.num_bits - 1)
            individuo[bit] = individuo[bit].translate(tabela_mutacao)

        self._ajustar(individuo)

    def econtrar_filho_mais_apto(self):
       
        candidatos = list(zip(self.populacao, self.avaliacao))

        return min(candidatos, key=lambda elemento: elemento[1])


def main():

    algoritmo_genetico = Genetic_Algorithm(-10, 10, 4, 1, 60, 5)

    algoritmo_genetico.avaliar()

    for i in range(algoritmo_genetico.num_geracoes):

        print( 'Resultado {}: {}'.format(i, algoritmo_genetico.econtrar_filho_mais_apto()) )

        nova_populacao = []
        while len(nova_populacao) < algoritmo_genetico.tam_populacao:

            pai = algoritmo_genetico.selecionar()
            mae = algoritmo_genetico.selecionar()

            filho_1, filho_2 = algoritmo_genetico.crossover(pai, mae)

            algoritmo_genetico.mutar(filho_1)
            algoritmo_genetico.mutar(filho_2)
            nova_populacao.append(filho_1)
            nova_populacao.append(filho_2)

        algoritmo_genetico.populacao = nova_populacao
        algoritmo_genetico.avaliar()

    print( 'Resultado {}: {}'.format(i+1, algoritmo_genetico.econtrar_filho_mais_apto()) )

    return 0

if __name__ == '__main__':
    main()
