from particles import particle
from Vector import Vector2d

class playerinventory:

    def __init__(self, items, amounts, default=0, owner=None):
        if len(amounts) != len(items):
            raise Exception("amounts is not same length as items. Lenght amounts: ", len(amounts), ", Lenght items: ", len(items))
        if not default < len(amounts) or default < 0:
            raise Exception("default index is out of bounds")
        if len(items) == 0:
            raise Exception("item list length cant be 0")

        self.slots = len(amounts)
        self.default = default
        self.index = self.default
        #holds the classes of the items in the inventory
        self.items = items
        #amount -1 is infinity
        self.amounts = amounts

        self.owner = owner

    #returns true if non zero item found, false if not
    def nextnonzero(self):
        counter = 0
        self.next()

        while self.amounts[self.index] == 0:
            counter += 1
            self.next()
            if counter >= self.slots:
                if self.amounts[self.index] == 0:
                    return False
                else:
                    break
        return True

    #returns true if non zero item found, false if not
    def previousnonzero(self):
        counter = 0
        self.previous()
        while self.amounts[self.index] == 0:
            counter += 1
            self.previous()
            if counter >= self.slots:
                if self.amounts[self.index] == 0:
                    return False
                else:
                    break
        return

    #returns next item in list
    def next(self):
        self.index = (self.index + 1) % self.slots

    #return previous item in list
    def previous(self):
        if self.index == 0:
            self.index = self.slots - 1
        else:
            self.index -= 1

    #get the currently selected item
    def getcurrentitem(self):
        return self.items[self.index]

    #get amount of currently selected type
    def getcurrentamount(self):
        return self.amounts[self.index]

    #return the current object and subtracts one of its amount, switch to next non zero if paramtere is true and amount is zero
    def usecurrent(self, switchwhenemtpy):
        if self.amounts[self.index] == 0:
            #switch to next nonzero item if empty
            if switchwhenemtpy and self.amounts[self.index] == 0:
                self.nextnonzero()
            return None
        elif self.amounts[self.index] < 0:
            return self.items[self.index]
        else:
            self.amounts[self.index] -= 1
            item = self.items[self.index]
            #switch to next nonzero item if empty
            if switchwhenemtpy and self.amounts[self.index] == 0:
                self.nextnonzero()

            return item

    #add a number to total amount of a given type, raises exception when item is not in inventory
    def addtoitemamount(self, item, amount):
        if item in self.items:
            index = self.items.index(item)
            if self.amounts[index] >= 0:
                self.amounts[index] += amount
            self.pickupparticle(item, amount)
        else:
            self.newitem(item, amount)

    #set the amount of a given item
    def setitemamount(self, item, amount):
        if item in self.items:
            index = self.items.index(item)
            self.amounts[index] = amount
        else:
            raise Exception("item not in inventory")

    #adds an item to the inventory
    def newitem(self, item, amount):
        if item in self.items:
            raise Exception("item is already in inventory")
        else:
            self.items.append(item)
            self.amounts.append(amount)
            self.slots += 1
            self.pickupparticle(item, amount)


    #set current index to index of item passed, raises exception if item is not in inventpry
    def settoitem(self, item):
        if item in self.items:
            self.index = self.items.index(item)
            return True
        else:
            raise Exception("item not in inventory")

    #gets te amount of item, raises exception if item is not in inventpry
    def getamountofitem(self, item):
        if item in self.items:
            return self.amounts[self.items.index(item)]
        else:
            raise Exception("item not in inventory")

    #returns a copy of the inventory
    def copy(self):
        return playerinventory(self.items.copy(), self.amounts.copy(), self.default)

    # pickup particle, text that gets displayed above the player
    def pickupparticle(self, item, amount):
        text = "+" + str(amount) + " " + item._name
        textsurface = self.owner.font.render(text, False, self.owner.color)
        particle([self.owner.pos[0], self.owner.pos[1] - 60], textsurface, 3, Vector2d(0.0, -1.0), 0.7, 0.19, self.owner.entities[2], True, 0.0, None, 8.0)
