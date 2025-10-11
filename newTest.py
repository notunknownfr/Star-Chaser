import turtle
from PIL import Image
from time import time, sleep
import random
from threading import Thread
import os

turtlesList=[]


class turtleCreator(turtle.Turtle):
    def __init__(self,shape,color,xCoor,yCoor):
        
        turtlesList.append(self)
        self.shape(shape)
        self.color(color)
        self.teleport(xCoor,yCoor)


class ScreenClass():
    def __init__(self):
        self.screen=turtle._Screen
        self.screen.setup(1.0, 1.0)
        self.selectStartGame = turtleCreator("square", "white", -58, 180)
        self.selectHistory = turtleCreator("square", "white", 25.9, 115)
        self.selectExit = turtleCreator("square", "white", 2, 50)
        self.changeKeyBindTurtle = turtleCreator("square", "white", 15, -17)


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
        self.bgpic("thumb.gif")

        t=turtleCreator("square","white",0,70)
        t.teleport(-230,-30)
        t.write("PRESS S TO START GAME\n\nPRESS H TO DISPLAY SCORE HISTORY\n\nPRESS ESCAPE TO EXIT THE GAME\n\nPRESS C TO CHANGE KEY SETTINGS")
        t.hideturtle()
        
       
        self.selectStartGame.shapesize(1.3,17)
        self.selectHistory.shapesize(1.3,25.8)
        self.selectExit.shapesize(1.3,23.2)
        self.changeKeyBindTurtle.shapesize(1.3,24.3)

        


class KeyBindManager:
    def __init__(self, screen: ScreenClass):
        self.screen = screen


    def setup_keybinds(self):
        self.screen.listen()  
        self.screen.onkeypress(self.start_game, "s")
        self.screen.onkeypress(self.show_history, "h")
        self.screen.onkeypress(self.exit_game, "Escape")
        self.screen.onkeypress(self.change_keys, "c")
        self.screen.onkeypress(self.pause_game,"p")
        self.screen.onkeypress(self.resume_game,"r")
        self.screen.onkeypress(self.back,"b")

    def start_game(self):
        print("start game")

    def pause_game(self):
        print("pause game")

    
    def resume_game(self):
        print("resume game")

    def back(self):
        print("back")

    def show_history(self):
        print("history")
        
    def exit_game(self):
        self.screen.bye()

    def change_keys(self):
        print("change keys")