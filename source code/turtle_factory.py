from turtle import Turtle
import random

turtlesList=[]

class TurtleFactory(Turtle):
    def __init__(self,shape="square",color="white",xCoor=0,yCoor=0):
        super().__init__()
        turtlesList.append(self)
        self.shape(shape)
        self.color(color)
        self.teleport(xCoor,yCoor)

    @staticmethod
    def hideAllTurtles(self):
        for turtle in turtlesList:
            turtle.hideturtle()

    @staticmethod 
    def clearAllTurtles():
        for turtle in turtlesList:
            turtle.clear()

    def randomTeleport(self):
        self.teleport(random.randint(-300, 300), random.randint(-300, 300))


