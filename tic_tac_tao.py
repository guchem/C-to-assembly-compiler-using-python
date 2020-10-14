#!/usr/bin/python3
# @author : guchim
# © 2020
from random import randint
from itertools import permutations
import sys
from time import sleep

board = { 'topL':' ','topM':' ','topR':' ',
	'midL':' ','midM':' ','midR':' ',
	'lowL':' ','lowM':' ','lowR':' '
}

def makeBoard(board):
 print(board['topL']+' | ' + board['topM']+' | ' + board['topR'])
 print('--+---+--')
 print(board['midL']+' | ' + board['midM']+' | ' + board['midR'])
 print('--+---+--')

 print(board['lowL']+' | ' + board['lowM']+' | ' + board['lowR'])


# this winset contains every cpossible combination to win if either the player or the computer achieves one of the 48 possible combinations he will win

winSet = [
['topL', 'topM', 'topR'],
['topL', 'topR', 'topM'],
['topM', 'topL', 'topR'],
['topM', 'topR', 'topL'],
['topR', 'topL', 'topM'],
['topR', 'topM', 'topL'],

['midL', 'midM', 'midR'] ,
['midL', 'midR', 'midM'] ,
['midM', 'midL', 'midR'] ,
['midM', 'midR', 'midL'] ,
['midR', 'midL', 'midM'] ,
['midR', 'midM', 'midL'] ,

['lowL', 'lowM', 'lowR'] ,
['lowL', 'lowR', 'lowM'] ,
['lowM', 'lowL', 'lowR'] ,
['lowM', 'lowR', 'lowL'] ,
['lowR', 'lowL', 'lowM'] ,
['lowR', 'lowM', 'lowL'] ,

['topL', 'midL', 'lowL'] ,
['topL', 'lowL', 'midL'] ,
['midL', 'topL', 'lowL'] ,
['midL', 'lowL', 'topL'] ,
['lowL', 'topL', 'midL'] ,
['lowL', 'midL', 'topL'] ,

['topM', 'midM', 'lowM'] ,
['topM', 'lowM', 'midM'] ,
['midM', 'topM', 'lowM'] ,
['midM', 'lowM', 'topM'] ,
['lowM', 'topM', 'midM'] ,
['lowM', 'midM', 'topM'] ,

['topR', 'midR', 'lowR'] ,
['topR', 'lowR', 'midR'] ,
['midR', 'topR', 'lowR'] ,
['midR', 'lowR', 'topR'] ,
['lowR', 'topR', 'midR'] ,
['lowR', 'midR', 'topR'] ,

['topL', 'midM', 'lowR'] ,
['topL', 'lowR', 'midM'] ,
['midM', 'topL', 'lowR'] ,
['midM', 'lowR', 'topL'] ,
['lowR', 'topL', 'midM'] ,
['lowR', 'midM', 'topL'] ,

['topR', 'midL', 'lowL'] ,
['topR', 'lowL', 'midL'] ,
['midL', 'topR', 'lowL'] ,
['midL', 'lowL', 'topR'] ,
['lowL', 'topR', 'midL'] ,
['lowL', 'midL', 'topR'] ]

"""the winner function

the win function takes a list of moves the player or the computer takes and 
computer every possible 3 element combinations of those moves and if one of them
found to be in the winset that player will win
"""

def winner(moves:list,player:str):
 perm = permutations(moves,3)
 for i in perm:
  if list(i) in winSet:
   print()
   makeBoard(board)
   if player == 'player':
    print('\nCongratulations ! You win !\n')
    sys.exit(0)
   else:
    print('\nYou Lose The Computer Wins !\n')
    sys.exit(0)

# this are all available moves left to be taken     
availableMoves = ['topL', 'topM','topR','midL','midM','midR','lowL','lowM','lowR']

# playerSet will register moves taken by the player
playerSet = []

#machineSet will register moves taken by the computer
machineSet = []

print()
makeBoard(board)

for i in range(9):
 print(f'\nYour turn for X .\nmoves left {availableMoves}\nenter" exit" to quit\n')
 playerMove = input('>>>')

 while playerMove not in availableMoves and (playerMove.strip()).lower() != 'exit':
  print('invalid move plase try again ! ')
  playerMove = input('>>>')

 if (playerMove.strip()).lower() == 'exit':
  print('\nYou Quit Come Back \n')
  sys.exit(0)

 board[playerMove] = 'X'
 playerSet.append(playerMove)
 availableMoves.remove(playerMove)
 print('\nYou marked {playerMove} as X\n')
 makeBoard(board)

 if len(playerSet) >= 3:
  winner(playerSet,'player')

 # the time sleep is not necessary it is to add a dramatic effect as if the computer is thinking
 sleep(0.6)
 

 machineMove = availableMoves[randint(0,len(availableMoves)-1)]
 machineSet.append(machineMove)
 availableMoves.remove(machineMove)
 print(f'\a\nmachine has marked {machineMove} as O\n')
 board[machineMove] = 'O'
 makeBoard(board)

 if len(machineSet)>=3:
  winner(machineSet, 'Computer')

print('\nGame Over ! no one wins')
makeBoard(board)

