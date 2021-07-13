#!/usr/bin/python3
# @author : guchim
# © 2020
# updated july 8 2021
from random import randint
import sys
from time import sleep


board = {
    'topL': ' ', 'topM': ' ', 'topR': ' ',
    'midL': ' ', 'midM': ' ', 'midR': ' ',
    'lowL': ' ', 'lowM': ' ', 'lowR': ' '
}


def makeBoard():
    print(board['topL'] + ' | ' + board['topM'] + ' | ' + board['topR'])
    print('--+---+--')
    print(board['midL'] + ' | ' + board['midM'] + ' | ' + board['midR'])
    print('--+---+--')
    print(board['lowL'] + ' | ' + board['lowM'] + ' | ' + board['lowR'])


def winner():
    if board['topL'] == board['topM'] == board['topR'] and board['topR'] != ' '  or \
        board['midL'] == board['midM'] == board['midR'] and board['midR']  != ' ' or \
        board['lowL'] == board['lowM'] == board['lowR'] and board['lowR']  != ' ' or \
        board['topL'] == board['midL'] == board['lowL'] and board['lowL']  != ' ' or \
        board['topM'] == board['midM'] == board['lowM'] and board['lowM']  != ' ' or \
        board['topR'] == board['midR'] == board['lowR'] and board['lowR']  != ' ' or \
        board['topL'] == board['midM'] == board['lowR'] and board['lowR']  != ' ' or \
        board['topR'] == board['midM'] == board['lowL'] and board['lowL']  != ' ' :
        return True
    return False


availableMoves = ['topL', 'topM','topR','midL','midM','midR','lowL','lowM','lowR']


print()
makeBoard()

moves = 9
while moves > 0:
    print(f'\nYour turn for X .\nmoves left {availableMoves}\nenter" exit" to quit\n')
    playerMove = input('>>>')

    while playerMove not in availableMoves and (playerMove.strip()).lower() != 'exit':
        print('invalid move plase try again ! ')
        playerMove = input('>>>')

    if (playerMove.strip()).lower() == 'exit':
        print('\nYou Quit Come Back \n')
        sys.exit(0)

    board[playerMove] = 'X'
    moves -= 1
    availableMoves.remove(playerMove)
    makeBoard()
    if moves == 0:
        print('\nGame Over ! no one wins')
        sys.exit(1)
    if winner():
        print('Player has won')
        sys.exit(0)

    sleep(0.6)

    machineMove = availableMoves[randint(0, len(availableMoves) - 1)]

    availableMoves.remove(machineMove)
    print(f'\a\nmachine has marked {machineMove} as O\n')
    board[machineMove] = 'O'
    moves -= 1
    makeBoard()

    if winner():
        print('Machine has won')
        sys.exit(0)

else:
    print('\nGame Over ! no one wins')
    makeBoard()
    sys.exit(1)

