import copy


class Tabuleiro:
    def __init__(self, arg, parent=None, depth=0):
        self.estado = arg
        self._findx()
        self.filhos = []
        self.backtrack = parent
        self.profundidade = depth


    def __hash__(self):
        return hash(''.join(self.estado))

    def __copy__(self):
        return Tabuleiro(self.estado)

    def __str__(self):
        text = """┌──┬──┬──┬──┐
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
└──┴──┴──┴──┘""" \
            .format(self.estado[0].rjust(2, '0'), self.estado[1].rjust(2, '0'), self.estado[2].rjust(2, '0'),
                    self.estado[3].rjust(2, '0'),
                    self.estado[4].rjust(2, '0'), self.estado[5].rjust(2, '0'), self.estado[6].rjust(2, '0'),
                    self.estado[7].rjust(2, '0'),
                    self.estado[8].rjust(2, '0'), self.estado[9].rjust(2, '0'), self.estado[10].rjust(2, '0'),
                    self.estado[11].rjust(2, '0'),
                    self.estado[12].rjust(2, '0'), self.estado[13].rjust(2, '0'), self.estado[14].rjust(2, '0'),
                    self.estado[15].rjust(2, '0')).replace("00", "  ")
        return text

    def __repr__(self):
        return str(self.estado)

    def __eq__(self, other):
        return self.estado == other

    def _findx(self):
        i = 0
        while self.estado[i] != '0':
            i += 1
        self.x, self.y = (int(i / 4), i % 4)

    def solvabilidade(self):
        # Par:1 ; Impar:0
        soma = 0
        for i in range(0, 16):
            for j in range(i + 1, 16):
                if self.estado[i] > self.estado[j] and self.estado[i] != '0' and self.estado[j] != '0':
                    soma += 1
        for i in range(0, 16):
            if self.estado[i] == '0':
                a = int(i / 4) % 2 == 0
                b = not (soma % 2 == 0)
                # print(i, soma)
                # print("a == b", a, b, a==b)
                self.solvable = (a == b)
                return self.solvable

    def getX(self):
        return self.x, self.y

    # Definicao dos movimentos
    def _left(self):
        move = copy.deepcopy(self.estado)
        btrack = copy.deepcopy(self.backtrack)
        if btrack is None:
            btrack = ['Left']
        else:
            btrack.append('Left')
        if self.y != 0:
            move[self.x * 4 + self.y] = move[self.x * 4 + self.y - 1]
            move[self.x * 4 + self.y - 1] = '0'
            tleft = Tabuleiro(move, parent=btrack, depth=self.profundidade + 1)
            self.filhos.append(tleft)

    def _right(self):
        move = copy.deepcopy(self.estado)
        btrack = copy.deepcopy(self.backtrack)
        if btrack is None:
            btrack = ['Right']
        else:
            btrack.append('Right')
        if self.y != 3:
            move[self.x * 4 + self.y] = move[self.x * 4 + self.y + 1]
            move[self.x * 4 + self.y + 1] = '0'
            tright = Tabuleiro(move, parent=btrack, depth=self.profundidade + 1)
            self.filhos.append(tright)

    def _up(self):
        move = copy.deepcopy(self.estado)
        btrack = copy.deepcopy(self.backtrack)
        if btrack is None:
            btrack = ['Up']
        else:
            btrack.append('Up')
        if self.x != 0:
            move[self.x * 4 + self.y] = move[(self.x - 1) * 4 + self.y]
            move[(self.x - 1) * 4 + self.y] = '0'
            tup = Tabuleiro(move, parent=btrack, depth=self.profundidade + 1)
            self.filhos.append(tup)

    def _down(self):
        move = copy.deepcopy(self.estado)
        btrack = copy.deepcopy(self.backtrack)
        if btrack is None:
            btrack = ['Down']
        else:
            btrack.append('Down')
        if self.x != 3:
            move[self.x * 4 + self.y] = move[(self.x + 1) * 4 + self.y]
            move[(self.x + 1) * 4 + self.y] = '0'
            tdown = Tabuleiro(move, parent=btrack, depth=self.profundidade + 1)
            self.filhos.append(tdown)

    def moves(self):
        if self.profundidade > 1:
            last = self.backtrack[self.profundidade-1]
        else:
            last = "0"
        if last != "Right":
            self._left()
        if last != "Left":
            self._right()
        if last != "Down":
            self._up()
        if last != "Up":
            self._down()
        return self.filhos
