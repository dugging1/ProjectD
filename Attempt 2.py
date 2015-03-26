from math import fabs

__author__ = 'dugging'
from tkinter import *
from random import *


class World():
    Time = 0
    Energy = 400
    food = 0
    map = []
    Digimon = []
    #1st dimension = digimon ID
    #2nd dimension = the digimon storage
    #3rd dimension = stores Mon() instances

                    #ID 0
                    #|-------------------------------------------------|
                    # Previous digivolutions
                    # |-----------------------|
                    #                             Next digivolutions
                    #                            |--------------------|
    #Digivolutions= [[[previous Mon(),[Energy]], [Next Mon(), [Energy]]]]

    Digivolutions = [[[None, []], [None, []]]]

    def __init__(self):
        self.generate(8, 8)
        self.createtemplates()
        self.createtree()

    def move(self, direction, newpos):
        print("OldPos: " + str(direction))
        print("NewPos: " + str(newpos))
        if direction == "N":
            if newpos[1] == len(self.map[0]):
                self.map[newpos[0]][newpos[1]].Mon = self.map[newpos[0]][0].Mon
                self.map[newpos[0]][0] = None
                self.map[newpos[0]][newpos[1]].initialupdate()
                self.map[newpos[0]][0].initialupdate()
            else:
                self.map[newpos[0]][newpos[1]].Mon = self.map[newpos[0]][newpos[1]-1].Mon
                self.map[newpos[0]][newpos[1]-1].Mon = None
                self.map[newpos[0]][newpos[1]].initialupdate()
                self.map[newpos[0]][newpos[1]-1].initialupdate()
        elif direction == "E":
            if newpos[0] == 0:
                self.map[newpos[0]][newpos[0]].Mon = self.map[len(self.map)-1][newpos[1]].Mon
                self.map[len(self.map)-1][newpos[1]].Mon = None
                self.map[newpos[0]][newpos[1]].initialupdate()
                self.map[len(self.map)-1][newpos[1]].initialupdate()
            else:
                self.map[newpos[0]][newpos[0]].Mon = self.map[newpos[0]-1][newpos[1]].Mon
                self.map[newpos[0]-1][newpos[1]].Mon = None
                self.map[newpos[0]][newpos[1]].initialupdate()
                self.map[newpos[0]-1][newpos[1]].initialupdate()
        elif direction == "S":
            if newpos[1] == 0:
                self.map[newpos[0]][newpos[1]].Mon = self.map[newpos[0]][len(self.map[0])].Mon
                self.map[newpos[0]][len(self.map[0])].Mon = None
                self.map[newpos[0]][newpos[1]].initialupdate()
                self.map[newpos[0]][len(self.map[0])].initialupdate()
            else:
                self.map[newpos[0]][newpos[1]].Mon = self.map[newpos[0]][newpos[1]+1].Mon
                self.map[newpos[0]][newpos[1]+1].Mon = None
                self.map[newpos[0]][newpos[1]].initialupdate()
                self.map[newpos[0]][newpos[1]+1].initialupdate()
        elif direction == "W":
            if newpos[0] == len(self.map):
                self.map[newpos[0]][newpos[0]].Mon = self.map[0][newpos[1]].Mon
                self.map[0][newpos[1]].Mon = None
                self.map[newpos[0]][newpos[1]].initialupdate()
                self.map[0][newpos[1]].initialupdate()
            else:
                self.map[newpos[0]][newpos[0]].Mon = self.map[newpos[0]+1][newpos[1]].Mon
                self.map[newpos[0]+1][newpos[1]].Mon = None
                self.map[newpos[0]][newpos[1]].initialupdate()
                self.map[newpos[0]+1][newpos[1]].initialupdate()
        else:
            print("Invalid direction")

    def simulate(self, iterations):
        for a in range(iterations):
            print("Time: " + str(self.Time))
            self.Time += 1
            self.heat()
            self.createfood()
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    if self.map[x][y].Mon is not None:
                        self.map[x][y].Mon.digivolve()
                        self.map[x][y].Mon.eat()
                        self.map[x][y].Mon.move()

    def createfood(self):
        while self.food < int((len(self.map)*len(self.map[1]))*0.1):
            while True:
                x = randrange(0, len(self.map))
                y = randrange(0, len(self.map[1]))
                if self.map[x][y].Item is None:
                    self.map[x][y].Item = Food([5, 5, 5, 5, 5, 5, 5, 5])
                    self.food += 1
                    self.map[x][y].initialupdate()
                    break

    def heat(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y].Mon is not None:
                    if self.map[x][y].Mon.Level == 0:
                        if self.Energy != 0:
                            self.Energy -= 1
                            self.map[x][y].Mon.Energy[randrange(0, len(self.map[x][y].Mon.Energy))] += 1
                    else:
                        while True:
                            a = randrange(0, len(self.map[x][y].Mon.Energy))
                            if self.map[x][y].Mon.Energy[a] != 0:
                                self.map[x][y].Mon.Energy[a] -= 1
                                self.Energy += 1
                                break

    def generate(self, worldx, worldy):
        for x in range(worldx):
            self.map.append([])
            for y in range(worldy):
                self.map[x].append(Tile("Bl", [100, 100, 100, 100, 100, 100, 100, 100], None, None))

    def createtemplates(self):
        self.Digimon = []
        self.Digimon.append(Mon(0, "Egg", "Eg", 0, 0, [None, None, None], [1, 1, 1, 1, 1, 1, 1, 1]))
        self.Digimon.append(Mon(1, "Zurumon", "Zu", 1, 0, [None, None, None], [0, 0, 5, 0, 0, 0, 0, 0]))

    def createtree(self):
        tempid = 0
        self.Digivolutions = []
        #ID 0 - EGG
        self.Digivolutions.append([]) #add id 0
        self.Digivolutions[tempid].append([]) #add previous digivolutions(2nd dimension "0")
        self.Digivolutions[tempid].append([]) #add next digivolutions(2nd dimension "1")
        self.Digivolutions[tempid][1].append([self.Digimon[1], [0, 0, 5, 0, 0, 0, 0, 0]]) #add Zurumon to next digivolution array
        tempid += 1

        #ID 1 - ZURUMON
        self.Digivolutions.append([]) #add id 1
        self.Digivolutions[tempid].append([]) #add previous digivolutions
        self.Digivolutions[tempid].append([]) #add next digivolutions
        self.Digivolutions[tempid][0].append([self.Digimon[0], [1, 1, 1, 1, 1, 1, 1, 1]])

    def digivolve(self, pos, nextid, energy):
        #print("Digivolution at: (" + str(pos[0]) + "," + str(pos[1]) + ")")
        #print("Digimon name: " + str(self.map[pos[0]][pos[1]].Mon.Name))
        #print("Digivolving to: " + str(self.Digimon[nextid].Name))
        self.map[pos[0]][pos[1]].Mon = self.Digimon[nextid]
        self.map[pos[0]][pos[1]].Mon.Energy = energy
        self.map[pos[0]][pos[1]].Mon.Position = pos
        self.map[pos[0]][pos[1]].Mon.NewPosition = pos
        self.map[pos[0]][pos[1]].initialupdate()


class Food():
    Energy = [0, 0, 0, 0, 0, 0, 0, 0]
    Initial = "Ff"

    def __init__(self, energy):
        self.Energy = energy


class Tile():
    # Energy= [Holy,Dark,Machine,Insect,Dragon,Water,Earth,Beast]
    Affinity = [100, 100, 100, 100, 100, 100, 100, 100]
    Mon = None
    Item = None
    Initial = None

    def __init__(self, initial, affinity, item, mon):
        self.Initial = str(initial)
        self.Affinity = affinity
        self.Item = item
        self.Mon = mon

    def initialupdate(self):
        if self.Mon is not None:
            self.Initial = self.Mon.Initial
        elif self.Item is not None:
            self.Initial = self.Item.Initial
        else:
            self.Initial = "Bl"


class Mon():
    ID = None
    Name = None
    Initial = None
    Level = None
    Attribute = None
    Position = [None, None, None]
    #Energy= [Holy,Dark,Beast,Machine,Dragon,Water,Bird,Insect]
    Energy = [None, None, None, None, None, None, None, None]
    Weight = [None, None, None, None]

    def __init__(self, did, name, initial, level, attribute, position, energy):
        self.ID = did
        self.Name = name
        self.Initial = initial
        self.Level = level
        self.Attribute = attribute
        self.Position = position
        self.Position = position
        self.Energy = energy

    def move(self):
        targets = []
        order = []
        for x in range(len(self.Position[2].map)):
            for y in range(len(self.Position[2].map[x])):
                if self.Position[2].map[x][y].Item is not None:
                    targets.append([x, y])
        for a in targets:
            distance = fabs(self.Position[0]-a[0]) + fabs(self.Position[1]-a[1])
            if len(order) == 0:
                order.append([distance, a])
            else:
                for b in range(len(order)):
                    if distance < order[b][0]:
                        order.insert(b, [distance, a])
                        break
                    elif distance == order[b][0]:
                        order.insert(b+1, [distance, a])
                        break
                    else:
                        order.append([distance, a])
                        break

        if order[0][1][0] > self.Position[0]:
            #move down
            if self.Position[1] + 1 == len(self.Position[2].map):
                self.Position[1] = 0
            else:
                self.Position[1] += 1
            self.Position[2].move("S", self.Position)
            pass
        elif order[0][1][0] < self.Position[0]:
            #move up
            if self.Position[1] - 1 < 0:
                self.Position[1] = len(self.Position[2].map)-1
            else:
                self.Position[1] -= 1
            self.Position[2].move("N", self.Position)
            pass
        else:
            if order[0][1][1] > self.Position[1]:
                #move right
                if self.Position[0] + 1 == len(self.Position[2].map[1]):
                    self.Position[0] = 0
                else:
                    self.Position[0] += 1
                self.Position[2].move("E", self.Position)
                pass
            elif order[0][1][1] < self.Position[1]:
                #move left
                if self.Position[1] - 1 < 0:
                    self.Position[0] = len(self.Position[2].map[1])-1
                else:
                    self.Position[0] -= 1
                self.Position[2].move("W", self.Position)
                pass

        self.targets = targets
        self.order = order

    def eat(self):
        if self.Position[2].map[self.Position[0]][self.Position[1]].Item is not None:
            for energy in range(len(self.Position[2].map[self.Position[0]][self.Position[1]].Item.Energy)):
                self.Energy[energy] += self.Position[2].map[self.Position[0]][self.Position[1]].Item.Energy[energy]
            self.Position[2].map[self.Position[0]][self.Position[1]].Item = None

    def digivolve(self):
        digivolve = False
        degenerate = False
        #Previous(Degeneration)
        for previous in self.Position[2].Digivolutions[self.ID][0]:
            degeneratestats = 0
            for energytype in range(len(previous[1])):
                if previous[1][energytype] >= self.Energy[energytype]:
                    degeneratestats += 1
            if degeneratestats == len(self.Energy):
                degenerate = True
                digimon = previous[0].ID
                break
        #Next(Digivolution)
        for Next in self.Position[2].Digivolutions[self.ID][1]:
            digivolvestats = 0
            for energytype in range(len(Next[1])):
                if Next[1][energytype] <= self.Energy[energytype]:
                    digivolvestats += 1
            if digivolvestats == len(self.Energy):
                digivolve = True
                digimon = Next[0].ID
                break
        if degenerate or digivolve:
            if degenerate:
                print(self.Name + " degenerated to " + self.Position[2].Digimon[digimon].Name)
            elif digivolve:
                print(self.Name + " digivolved to " + self.Position[2].Digimon[digimon].Name)
            self.Position[2].digivolve(self.Position, digimon, self.Energy)


class Display():
    @staticmethod
    def map(world):
        gui = Tk()
        gui.title("ProjectD")
        for x in range(len(world.map)):
            for y in range(len(world.map[x])):
                Label(gui, text=str(world.map[x][y].Initial)).grid(column=x, row=y)

test = World()
test.createfood()
test.digivolve([1, 1, test], 1, [5, 5, 5, 5, 5, 5, 5, 5])
test.move("N", [1, 0, test])
#test.simulate(10)
Display.map(test)
