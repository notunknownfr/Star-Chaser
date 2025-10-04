from turtle import *
from PIL import Image
from time import time, sleep
import random
from threading import Thread
import os

turtlesList=[]


class turtleCreator:
    def __init__(self,shape,color,xCoor,yCoor):
        self.newTurtle=Turtle()
        turtlesList.append(self.newTurtle)
        self.newTurtle.shape(shape)
        self.newTurtle.color(color)
        self.newTurtle.teleport(xCoor,yCoor)

    def hideAllTurtles(self):
        for turtle in turtlesList:
            turtle.hideturtle()
        
    def showTurtle(self):
         self.newTurtle.showturtle()

    def hideTurtle(self):
        self.newTurtle.hideturtle()

    def TurtleTeleport(self):
            self.newTurtle.teleport(random.randint(-300, 300), random.randint(-300, 300))

    def turtleDeletion(self):
         self.newTurtle.clear()

    def changeShape(self,shape):
         self.newTurtle.shape(shape)

    def changeSize(self,width,length):
         self.newTurtle.shapesize(width,length)

    def changeColor(self,newColor):
        self.newTurtle.color(newColor)
        

class ScreenClass:
    def __init__(self):
        
        self.newScreen=Screen()

    def imageSetup(self):
        img=Image.open("stars.gif")
        img=img.resize((1920, 1080))
        img.save("stars.gif")

        img=Image.open("thumb.gif")
        img=img.resize((1920, 1080))
        img.save("thumb.gif")
        
        img=Image.open("history.gif")
        img=img.resize((1920, 1080))
        img.save("history.gif")

    def StartScreenSetup(self):
        t=turtleCreator("square","white",0,70)
        selectStartGame=turtleCreator("square","white",0,40)
        selectExit=turtleCreator("square","white",0,10)
        selectHistory=turtleCreator("square","white",0,-20)
        changeKeyBindTurtle=turtleCreator("square","white",0,-50)


        self.newScreen.bgpic("thumb.gif")
        t.changeColor("white")
        t.TurtleTeleport(70,0)
        t.write("PRESS S TO START GAME\n\nPRESS H TO DISPLAY SCORE HISTORY\n\nPRESS ESCAPE TO EXIT THE GAME\n\nPRESS C TO CHANGE KEY SETTINGS",align="center",font=("Arial",16,"normal"))
        t.hideTurtle()


        selectStartGame.showTurtle()
        selectExit.showTurtle()
        selectHistory.showTurtle()
        
        changeKeyBindTurtle.changeColor("")
        changeKeyBindTurtle.changeShape("square")
        changeKeyBindTurtle.changeSize(1,19)
        changeKeyBindTurtle.TurtleTeleport(60,10)

        
        selectStartGame.changeColor("")
        selectStartGame.changeShape("square")
        selectStartGame.changeSize(1,13)
        selectStartGame.TurtleTeleport(0,160)

        selectHistory.changeColor("")
        selectHistory.changeShape("square")
        selectHistory.changeSize(1,20)
        selectHistory.TurtleTeleport(67,110)

        selectExit.changeColor("")
        selectExit.changeShape("square")
        selectExit.changeShape(1,17.8)
        selectExit.TurtleTeleport(50,60)




x=ScreenClass()
x.StartScreenSetup()