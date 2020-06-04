

class playerinventory:

    def __init__(self, items, amounts, default=0):
        if len(amounts) != len(items):
            raise Exception("amounts is not same length as items. Lenght amounts: ", len(amounts), ", Lenght items: ", len(items))
        if not default < len(amounts) or default < 0:
            raise Exception("default index is out of bounds")
        if len(items) == 0:
            raise Exception("item list length cant be 0")

        self.slots = len(amounts)
        self.index = default
        #holds the classes of the items in the inventory
        self.items = items
        #amount -1 is infinity
        self.amounts = amounts

    #returns true if non zero item found, false if not
    def nextnonzero(self):
        # TODO : implement this function
        return

    #returns true if non zero item found, false if not
    def previousnonzero(self):
        # TODO : implement this function
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

    #return the current object and subtracts one of its amount, switch to default if empty
    def usecurrent(self):
        if self.amounts[self.index] == 0:
            return None
        elif self.amounts[self.index] < 0:
            return self.items[self.index]
        else:
            self.amounts[self.index] -= 1
            return self.items[self.index]

    #add a number to total amount of a given type, raises exception when item is not in inventory
    def addtoitemamount(self, item, amount):
        if item in self.items:
            index = self.items.index(item)
            if self.amounts[index] >= 0:
                self.amounts[index] += amount
        else:
            raise Exception("item not in inventory")

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

    def copy(self):
        #todo implement this function