import pygame

from gamelogic import scorchedearth

playernames = []
screenSize = [1280, 720]
#16:9 recommended

a = int(input("Number players (max 7):"))

for i in range(0, min(a, 7)):
    playernames.append(input("Enter player name:"))

game = scorchedearth(screenSize, playernames, False)