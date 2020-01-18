# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 15:58:11 2020

@author: Brenden Lowe
"""

import Dominion
import random
import testUtility
from collections import defaultdict

#Get player names
player_names = testUtility.getPlayers()

#number of curses and victory cards
nV = testUtility.victoryCount(player_names)
nC = testUtility.cursesCount(player_names)

#Define box
box = testUtility.getBoxes(nV)

supply_order = testUtility.getSupplyOrder()

#Define supply
supply = testUtility.getSupply(player_names, nV, nC, box)

#initialize the trash
trash = testUtility.initializeTrash()

#Costruct the Player objects
players = testUtility.constructPlayers(player_names)

#Play the game
turn  = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print ("\rStart of turn " + str(turn))    
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)
            

#Final score
dcs=Dominion.cardsummaries(players)
vp=dcs.loc['VICTORY POINTS']
vpmax=vp.max()
winners=[]
for i in vp.index:
    if vp.loc[i]==vpmax:
        winners.append(i)
if len(winners)>1:
    winstring= ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0],'wins!'])

print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)