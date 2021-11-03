#! /usr/bin/env python3
import sys
import argparse
from Class import Tabuleiro
from Functions import bfs, dfs, astar, guloso, hamming, manhattan

def main():
    
    parser = argparse.ArgumentParser(description='This is a 15 puzzle solver.')
    parser.add_argument('--dfs', type=int,
                        help='Run Depth-first search (provide a positive integer, max depth to search)')
    parser.add_argument('--bfs', action='store_true',
                        help='Run Breadth-first search')
    parser.add_argument('--astar', '--a', type=int, choices=[1, 2],
                        help='Run A* search (1 -hamming; 2 -manhattan)')
    parser.add_argument('--greedy', '--gulosa', type=int, choices=[1, 2],
                        help='Run Greedy search (1 -hamming; 2 -manhattan)')

    parser.add_argument('--input', '-i', help='Specify an input file for tests')
    args = parser.parse_args()

    # Ler tabuleiros
    if args.input is None:
        inicialState = input("Starting Board:\n").split()
        goalState = input("Goal Board:\n").split()
    else:
        try:
            numbers = []
            with open(args.input, "r") as f:
                lines = f.readlines()
                for line in lines:
                    numbers = numbers + line.split()
            inicialState = numbers[:16]
            numbers = numbers[16:]
            goalState = numbers[:16]
        except FileNotFoundError:
            sys.stderr.write("Invalid file path")
            sys.exit(1)

    # iniciar tabuleiros
    inicialState = Tabuleiro(inicialState)
    goalState = Tabuleiro(goalState)
    print('Estado Inicial:')
    print(inicialState)
    print('Estado Objetivo:')
    print(goalState)

    if inicialState == goalState:
        print("Both are the same. Already solved!")
        sys.exit(0)

    if inicialState.solvabilidade() ^ goalState.solvabilidade():
        print('Invalid boards.')
        sys.exit(1)

    if args.astar is None and not args.bfs and args.dfs is None and not args.idfs and args.greedy is None:
        sys.stderr.write("Provide a valid input.")

        #Busca em Largura
        print("Breadth-first search:")
        moves, nodes = bfs(inicialState, goalState)
        print(nodes, "nodes used.")
        if moves:
            print("Path to goal:")
            print(" -> ".join(moves))
        else:
            print("No solution found.")
        print("\n")

        #Busca em Profundidade
        print("Depth-first search:")
        moves, nodes= dfs(inicialState, goalState, 12)
        print(nodes, "nodes used.")
        if moves:
            print("Path to goal:")
            print(" -> ".join(moves))
        else:
            print("No solution found.")
        print("\n")

        #Busca A*
        print("A* search:")
        comp = manhattan
        if args.astar == 1:
            comp = hamming
        moves, nodes = astar(inicialState, goalState, comp)
        print(nodes, "nodes used.")
        if moves:
            print("Path to goal:")
            print(" -> ".join(moves))
        else:
            print("No solution found.")
        print("\n")

        '''#Busca Gulosa
        print("Greedy search:")
        comp = manhattan
        print("\nkedia1\n")
        if args.greedy == 1:
            comp = hamming
        print("\nkedia2\n")
        moves, nodes = guloso(inicialState, goalState, comp)
        print("\nkedia72\n")
        print(nodes, "nodes used.")
        if moves:
            print("Path to goal:")
            print(" -> ".join(moves))
        else:
            print("No solution found.")'''

        sys.exit(1)

    if inicialState == goalState:
        print("Both are the same. Already solved!")
        sys.exit(0)    

if __name__ == '__main__':
    main()
