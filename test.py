__author__ = 'dugging'
from random import *
from tkinter import *


class World():
    Energy = 2000
    map = []
    iterations = 0

    def __init__(self):
        x = randrange(2 ** 3, 2 ** 5)
        y = randrange(2 ** 3, 2 ** 5)
        for i in range(x):
            self.map.append([])
            for k in range(y):
                self.map[i].append([])
                self.map[i][k] = Tile(affinity=[100, 100, 100, 100, 100, 100, 100, 100], initial="Bl", item=None, mon=None)
        while self.Energy > 1024:
            self.createfood()

    def simulate(self, iteration):
        for x in range(int(iteration)):
            self.iterations += 1
            #Cycle through the map
            for a in range(len(self.map)):
                for b in range(len(self.map[a])):
                    if self.map[a][b].Mon is not None:
                        self.map[a][b].Mon.emaptrans()
                        self.map[a][b].Mon.surroundcheck()
                        self.map[a][b].Mon.digivolve()
                    self.map[a][b].initialupdate()
            if self.iterations % 10 == 0:
                self.createfood()

    def digivolve(self, mon, pos, hunger):
        self.map[pos[0]][pos[1]].Mon = mon
        self.map[pos[0]][pos[1]].Mon.Position = pos
        self.map[pos[0]][pos[1]].Mon.Hunger = hunger
        self.map[pos[0]][pos[1]].initialupdate()

    def createfood(self):
        if self.Energy > 8:
            energy = int(randrange(0, int(self.Energy / 2)) / 8)
            self.Energy -= energy * 8
            temp = Food([energy, energy, energy, energy, energy, energy, energy, energy])
            while True:
                x = randrange(0, len(self.map))
                y = randrange(0, len(self.map[x]))
                if self.map[x][y].Item is None:
                    self.map[x][y].Item = temp
                    self.map[x][y].initialupdate()
                    break


class Food():
    Energy = [0, 0, 0, 0, 0, 0, 0, 0]
    Initial = "Ff"

    def __init__(self, energy):
        self.Energy = energy


class Tile():
    # Energy= [Holy,Dark,Machine,Insect,Dragon,Water,Earth,Beast]
    Affinity = [100, 100, 100, 100, 100, 100, 100, 100]
    Initial = None
    Item = None
    Mon = None

    def __init__(self, initial, affinity, item, mon):
        self.Initial = str(initial)
        self.Affinity = affinity
        self.Item = item
        self.Mon = mon

    def initialupdate(self):
        if self.Mon is not None:
            self.Initial = self.Mon.Initial
        elif self.Mon is not None:
            self.Initial = self.Item.Initial
        else:
            self.Initial = "Bl"


class Mon():
    Name = ""
    Initial = ""
    Level = 0
    Attribute = 0
    Position = [0, 0, "WORLD"]
    Hunger = 0
    Energy = [0, 0, 0, 0, 0, 0, 0, 0]
    Previous = []
    Next = []

    North = ""
    East = ""
    South = ""
    West = ""
    Weight = [0, 0, 0, 0]

    def __init__(self, name, initial, lvl, att, pos, hung, energy):
        self.Energy = energy
        self.Hunger = hung
        self.Initial = initial
        self.Level = lvl
        self.Name = name
        self.Position = pos
        self.Attribute = att

    def emaptrans(self):
        x = randrange(0, len(self.Energy))
        if self.Level == 0:
            if self.Position[2].Energy > 0:
                self.Energy[x] += 1
                self.Position[2].Energy -= 1
        elif self.Level != 0:
            if self.Energy[x] != 0:
                self.Energy[x] -= 1
                self.Position[2].Energy += 1
            else:
                for a in range(len(self.Energy)):
                    if self.Energy[a] != 0:
                        self.Energy[a] -= 1
                        self.Position[2].Energy += 1

    def digivolve(self):
                    #Checking
        digivolve = False
        digimon = 0
        degenerate = False
        for x in range(len(self.Previous)):
            degeneratestats = 0
            #print("     Currently checking: ", self.Previous[x].Name)
            for y in range(len(self.Previous[x].Energy)):
                #print("Currently checking energy level: ", y)
                #print(self.Previous[x].Name, " energy level: ", self.Previous[x].Energy[y])
                #print("self energy level: ", self.Energy[y])
                print("self = ", self.Energy)
                print(self.Previous[x].Name, " = ", self.Previous[x].Energy)
                if self.Previous[x].Energy[y] > self.Energy[y]:
                    degeneratestats += 1
            if degeneratestats == len(self.Energy):
                print("{0} degenerated to {1}".format(str(self.Name), str(self.Previous[x].Name)))
                degenerate = True
                digimon = self.Next[x]
                break
        for a in range(len(self.Next)):
            digivolvestats = 0
            for b in range(len(self.Next[a].Energy)):
                if self.Next[a].Energy[b] <= self.Energy[b]:
                    digivolvestats += 1
            if digivolvestats == len(self.Energy):
                print("{0} digivolved to {1}".format(str(self.Name), str(self.Next[a].Name)))
                digivolve = True
                digimon = self.Next[a]
                break
                    #Digivolving and degenerating
        if digivolve or degenerate:
            temp = digimon
            temp.Energy = self.Energy
            self.Position[2].digivolve(temp, self.Position, self.Hunger)

    def surroundcheck(self):
        weight = [0, 0, 0, 0]
        northwieght = 0
        eastwieght = 0
        southwieght = 0
        westwieght = 0

        if self.Level != 0:
            try:
                self.North = self.Position[2].map[self.Position[0]][self.Position[1] - 1]
            except IndexError:
                self.North = None
            try:
                self.East = self.Position[2].map[self.Position[0] + 1][self.Position[1]]
            except IndexError:
                self.East = None
            try:
                self.South = self.Position[2].map[self.Position[0]][self.Position[1] + 1]
            except IndexError:
                self.South = None
            try:
                self.West = self.Position[2].map[self.Position[0] - 1][self.Position[1]]
            except IndexError:
                self.West = None

            if self.North.Mon is None and self.North.Item is None:
                northwieght = 1
            elif self.North.Mon is None:
                northwieght = 3
            elif self.North is None:
                northwieght = -1
            else:
                print("I DON'T KNOW???")

            if self.East.Mon is None and self.East.Item is None:
                eastwieght = 1
            elif self.East.Mon is None:
                eastwieght = 3
            elif self.East is None:
                eastwieght = -1
            else:
                print("I DON'T KNOW???")

            if self.South.Mon is None and self.South.Item is None:
                southwieght = 1
            elif self.South.Mon is None:
                southwieght = 3
            elif self.South is None:
                southwieght = -1
            else:
                print("I DON'T KNOW???")

            if self.West.Mon is None and self.West.Item is None:
                westwieght = 1
            elif self.West.Mon is None:
                westwieght = 3
            elif self.West is None:
                westwieght = -1
            else:
                print("I DON'T KNOW???")

            if northwieght >= eastwieght and northwieght >= southwieght and northwieght >= westwieght:
                weight[0] = 1
                if eastwieght >= northwieght and eastwieght >= southwieght and eastwieght >= westwieght:
                    weight[1] = 2
                    if southwieght >= westwieght:
                        weight[2] = 3
                        weight[3] = 4
                    elif westwieght >= southwieght:
                        weight[2] = 4
                        weight[3] = 3
                elif southwieght >= northwieght and southwieght >= eastwieght and southwieght >= westwieght:
                    weight[1] = 3
                    if eastwieght >= westwieght:
                        weight[2] = 2
                        weight[3] = 4
                    elif westwieght >= eastwieght:
                        weight[2] = 4
                        weight[3] = 2
                elif westwieght >= northwieght and westwieght >= eastwieght and westwieght >= southwieght:
                    weight[1] = 4
                    if eastwieght >= southwieght:
                        weight[2] = 2
                        weight[3] = 3
            elif eastwieght >= northwieght and eastwieght >= southwieght and eastwieght >= westwieght:
                weight[0] = 2
                if northwieght >= eastwieght and northwieght >= southwieght and northwieght >= westwieght:
                    weight[1] = 1
                    if southwieght >= westwieght:
                        weight[2] = 3
                        weight[3] = 4
                    elif westwieght >= southwieght:
                        weight[2] = 4
                        weight[3] = 3
                elif southwieght >= northwieght and southwieght >= eastwieght and southwieght >= westwieght:
                    weight[1] = 3
                    if northwieght >= westwieght:
                        weight[2] = 1
                        weight[3] = 4
                    elif westwieght >= northwieght:
                        weight[2] = 4
                        weight[3] = 1
                elif westwieght >= northwieght and westwieght >= eastwieght and westwieght >= southwieght:
                    weight[1] = 4
                    if northwieght >= southwieght:
                        weight[2] = 1
                        weight[3] = 3
                    elif southwieght >= northwieght:
                        weight[2] = 3
                        weight[3] = 1
            elif southwieght >= northwieght and southwieght >= eastwieght and southwieght >= westwieght:
                weight[0] = 3
                if northwieght >= eastwieght and northwieght >= southwieght and northwieght >= westwieght:
                    weight[1] = 1
                    if eastwieght >= westwieght:
                        weight[2] = 2
                        weight[3] = 4
                    elif westwieght >= eastwieght:
                        weight[2] = 4
                        weight[3] = 2
                elif eastwieght >= northwieght and eastwieght >= southwieght and eastwieght >= westwieght:
                    weight[1] = 2
                    if northwieght >= westwieght:
                        weight[2] = 1
                        weight[3] = 4
                    elif westwieght >= northwieght:
                        weight[2] = 4
                        weight[3] = 1
                elif westwieght >= northwieght and westwieght >= eastwieght and westwieght >= southwieght:
                    weight[1] = 4
                    if northwieght >= westwieght:
                        weight[2] = 1
                        weight[3] = 4
                    elif westwieght >= northwieght:
                        weight[2] = 4
                        weight[3] = 1
            elif westwieght >= northwieght and westwieght >= eastwieght and westwieght >= southwieght:
                weight[0] = 4
                if northwieght >= eastwieght and northwieght >= southwieght and northwieght >= westwieght:
                    weight[1] = 1
                    if eastwieght >= southwieght:
                        weight[2] = 2
                        weight[3] = 3
                    elif southwieght >= eastwieght:
                        weight[2] = 3
                        weight[3] = 2
                elif eastwieght >= northwieght and eastwieght >= southwieght and eastwieght >= westwieght:
                    weight[1] = 2
                    if northwieght >= southwieght:
                        weight[2] = 1
                        weight[3] = 3
                    elif southwieght >= northwieght:
                        weight[2] = 3
                        weight[3] = 1
                elif southwieght >= northwieght and southwieght >= eastwieght and southwieght >= westwieght:
                    weight[1] = 3
                    if northwieght >= eastwieght:
                        weight[2] = 1
                        weight[3] = 2

            self.Weight = weight


class Display():
    @staticmethod
    def map(world):
        gui = Tk()
        gui.title("Project D")
        for x in range(len(world.map)):
            for y in range(len(world.map[x])):
                #print("(", x, ",", y, ")", " is ", world.map[x][y].Initial)
                Label(gui, text=str(world.map[x][y].Initial)).grid(column=x, row=y)

    @staticmethod
    def mapdigimon(world):
        digicount = 0
        for x in range(len(world.map)):
            for y in range(len(world.map[x])):
                if world.map[x][y].Mon is not None:
                    digicount += 1
        print(digicount)

    @staticmethod
    def mapfood(world):
        foodcount = 0
        for x in range(len(world.map)):
            for y in range(len(world.map[x])):
                if world.map[x][y].Item is not None:
                    if world.map[x][y].Item.Initial == "Ff":
                        foodcount += 1
        print(foodcount)


test = World()


# Mon("Name",Initial,Lvl,Type,Pos[],Hunger,Affinity)
#energy= [Holy,Dark,Machine,Insect,Dragon,Water,Earth,Beast]

#Egg
Egg = Mon("Egg", "Eg", 0, 3, [0, 0, None], 0, [1, 1, 1, 1, 1, 1, 1, 1])

#In-Training 1
Botomon = Mon("Botomon", "Bo", 1, 3, [0, 0, None], 0, [0, 0, 0, 0, 20, 0, 0, 0])
Punimon = Mon("Punimon", "Pu", 1, 3, [0, 0, None], 0, [0, 0, 0, 0, 0, 20, 0, 0])
Zurumon = Mon("Zurumon", "Zu", 1, 3, [0, 0, None], 0, [0, 0, 20, 0, 0, 0, 0, 0])

#In-Training 2
Koromon = Mon("Koromon", "Ko", 2, 2, [0, 0, None], 0, [0, 0, 0, 0, 40, 0, 0, 0])
Tsunomon = Mon("Tsunomon", "Ts", 2, 1, [0, 0, None], 0, [0, 0, 0, 0, 0, 40, 0, 0])
Pagumon = Mon("Pagumon", "Pa", 2, 0, [0, 0, None], 0, [0, 20, 0, 0, 20, 0, 0, 0])

#Rookie
Augumon = Mon("Augumon", "Au", 3, 2, [0, 0, None], 0, [0, 0, 0, 0, 80, 0, 0, 0])
BlkAugumon = Mon("Black Augumon", "BA", 3, 0, [0, 0, None], 0, [0, 20, 0, 0, 60, 0, 0, 0])
Gabumon = Mon("Gabumon", "Ga", 3, 2, [0, 0, None], 0, [0, 0, 0, 0, 0, 20, 0, 60])
Elecmon = Mon("Elecmon", "El", 3, 1, [0, 0, None], 0, [0, 0, 40, 40, 0, 0, 0, 0])
Gotsumon = Mon("Gotsumon", "Go", 3, 1, [0, 0, None], 0, [0, 0, 20, 0, 0, 0, 60, 0])
Goblimon = Mon("Goblimon", "Gb", 3, 0, [0, 0, None], 0, [0, 10, 0, 0, 0, 0, 0, 70])
DemiDevimon = Mon("DemiDevimon", "Dd", 3, 0, [0, 0, None], 0, [0, 70, 0, 0, 10, 0, 0, 0])

#Egg
Egg.Next = [Botomon, Punimon, Zurumon]

#In-Training 1
    #Zurumon
Zurumon.Previous = [Egg]
Zurumon.Next = [Pagumon]
    #Botomon
Botomon.Previous = [Egg]
Botomon.Next = [Koromon]
    #Punimon
Punimon.Previous = [Egg]
Punimon.Next = [Tsunomon]

#In-Training 2
    #Koromon
Koromon.Previous = [Botomon]
Koromon.Next = [Augumon]
    #Tsunonmon
Tsunomon.Previous = [Punimon]
Tsunomon.Next = [Gabumon, Elecmon]
    #Pagumon
Pagumon.Previous = [Zurumon]
Pagumon.Next = [Gotsumon, Goblimon, DemiDevimon]

#Rookie
    #Augumon
Augumon.Previous = [Koromon]
Augumon.Next = []
    #Gabumon
Gabumon.Previous = [Tsunomon]
Gabumon.Next = []
    #Elecmon
Elecmon.Previous = [Tsunomon]
Elecmon.Next = []
    #Gotsumon
Gotsumon.Previous = [Pagumon]
Gotsumon.Next = []
    #Goblimon
Goblimon.Previous = [Pagumon]
Goblimon.Next = []
    #DemiDevimon
DemiDevimon.Previous = [Pagumon]
DemiDevimon.Next = []

#Testing
test.digivolve(Egg, [0, 0, test], 0)
#test.map[0][0].Mon.Energy[5] = 20
test.createfood()