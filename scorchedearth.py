from gameloop import gameloop

# Left right with a and d
# switch item q and e
# aim with mouse
# shoot with space bar
# enter to start new game
# escape to quit

playernames = []
screenSize = [1200, 800]
#screenSize = [1920, 1080]

a = int(input("Number players:"))

for i in range(0, a):
    playernames.append(input("Enter player name:"))

game = gameloop(screenSize, playernames, False)