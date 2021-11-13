#! /usr/bin/env python3

from collections import deque

class MinHeap:
    def __init__(self, goalstate, compare):
        self.data = [None]
        self.size = 0
        self.comparator = compare
        self.goalstate = goalstate

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return item in self.data

    def __str__(self):
        return str(self.data)

    def _compare(self, x, y):
        x = self.comparator(self.data[x], self.goalstate)
        y = self.comparator(self.data[y], self.goalstate)

        if x < y:
            return True
        else:
            return False

    def getpos(self, x):
        for i in range(self.size+1):
            if x == self.data[i]:
                return i
        return None

    def _upHeap(self, i):
        while i > 1 and self._compare(i, int(i/2)):
            self._swap(i, int(i/2))
            i = int(i/2)

    def _downHeap(self, i):
        size = self.size
        while 2*i <= size:
            j = 2*i
            if j < size and self._compare(j+1, j):
                j += 1
            if self._compare(i, j):
                break
            self._swap(i, j)
            i = j

    def _swap(self, i, j):
        t = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = t

    def push(self, x):
        self.size += 1
        self.data.append(x)
        self._upHeap(self.size)

    def pop(self):
        if self.size < 1:
            return None
        t = self.data[1]
        self.data[1] = self.data[self.size]
        self.data[self.size] = t
        self.size -= 1
        self._downHeap(1)
        self.data.pop()
        return t

    def peek(self):
        if self.size < 1:
            return None
        return self.data[1]


# comparadores
def hamming(inicialState, goalstate):
    inicial = inicialState.estado
    goal = goalstate.estado
    depth = inicialState.profundidade
    sum = 0
    for x, y in zip(goal, inicial):
        if x != y and x != '0':
            sum += 1
    return sum + depth

def manhattan(inicialState, goalstate):
    inicial = inicialState.estado
    goal = goalstate.estado
    depth = inicialState.profundidade
    sum = 0
    for i in range(16):
        if goal[i] == '0':
            continue
        x1, y1 = (int(i / 4), i % 4)
        for j in range(16):
            if goal[i] == inicial[j]:
                x2, y2 = (int(j / 4), j % 4)
                sum += abs(x1 - x2) + abs(y1 - y2)
                break
    return sum + depth

#Algoritmos de Pesquisa

# Busca em Largura
def bfs(inicialState, goalstate):
    total_nos = 1
    fronteira = deque()
    fronteira.append(inicialState)

    while len(fronteira) > 0:
        state = fronteira.popleft()

        if goalstate == state:
            return state.backtrack, total_nos
        for filho in state.moves():
            total_nos += 1
            fronteira.append(filho)
        del(state);
    return False, total_nos

# Busca em Profundidade
def dfs(inicialState, goalstate, depth):
    total_nos = 1
    fronteira = list()
    visitados = set()
    fronteira.append(inicialState)

    while len(fronteira) > 0:
        state = fronteira.pop()
        visitados.add(state)

        if state == goalstate:
            return state.backtrack, total_nos

        for filho in state.moves():
            total_nos += 1
            if filho.profundidade <= depth:
                if filho not in visitados or filho not in fronteira:
                    fronteira.append(filho)
        del(state)
    return False, total_nos

# Busca Gulosa
def guloso(inicialState, goalstate, comparador):
    total_nos = 1
    print("\nkedia3\n")
    state = inicialState
    print("\nkedia4\n")
    cont = 0
    while state != goalstate:
        print("\nkedia %d\n", cont)
        filhos = state.moves()
        state = filhos.pop()
        for x in filhos:
            total_nos += 1
            if comparador(x, goalstate) < comparador(state, goalstate):
                state = x
        cont = cont + 1
    print("\nkedia5\n")
    return state.backtrack, total_nos

# Busca A*
def astar(inicialState, goalstate, comparador):
    total_nos = 1
    fronteira = MinHeap(goalstate, comparador)
    fronteira.push(inicialState)
    visitados = set()

    while len(fronteira) > 0:
        state = fronteira.pop()
        visitados.add(state)

        if goalstate == state:
            return state.backtrack, total_nos

        for filho in state.moves():
            total_nos += 1
            if filho not in fronteira and filho not in visitados:
                fronteira.push(filho)
            elif filho in fronteira:
                i = fronteira.getpos(filho)
                if fronteira.data[i].profundidade > filho.profundidade:
                    fronteira.data[i] = filho
                    fronteira._upHeap(i)

    return False, total_nos
