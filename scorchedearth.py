import pygame

from gamelogic import scorchedearth

playernames = []
screenSize = [720, 480]
#screenSize = [1920, 1080]
#16:9 recommended

a = int(input("Number players:"))

for i in range(0, a):
    playernames.append(input("Enter player name:"))

game = scorchedearth(screenSize, playernames, True)