from turtle import _Screen, Turtle, done
from PIL import Image
from turtle_factory import TurtleFactory
from settings import KeyBindManager

class ScreenClass(_Screen):
    def __init__(self):
        self.screen=_Screen
        self.screen.setup(1.0, 1.0)
        self.selectStartGame = TurtleFactory("square", "white", -58, 180)
        self.selectHistory = TurtleFactory("square", "white", 25.9, 115)
        self.selectExit = TurtleFactory("square", "white", 2, 50)
        self.changeKeyBindTurtle = TurtleFactory("square", "white", 15, -17)
        self.textTurtle=TurtleFactory("square","white",0,70)


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
        self.screen.bgpic("thumb.gif")

        self.textTurtle.teleport(-230,-30)
        self.textTurtle.write("PRESS S TO START GAME\n\nPRESS H TO DISPLAY SCORE HISTORY\n\nPRESS ESCAPE TO EXIT THE GAME\n\nPRESS C TO CHANGE KEY SETTINGS")
        self.textTurtle.hideturtle()
       
        self.selectStartGame.shapesize(1.3,17)
        self.selectHistory.shapesize(1.3,25.8)
        self.selectExit.shapesize(1.3,23.2)
        self.changeKeyBindTurtle.shapesize(1.3,24.3)

        self.keymanager=KeyBindManager(self.screen)
        self.keymanager.setup_keybinds()

