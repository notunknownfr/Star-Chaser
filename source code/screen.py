from turtle import Screen, Turtle, done
from PIL import Image
from turtle_factory import TurtleFactory

class ScreenClass():
    def __init__(self):

        self.screen=Screen()
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
        # from settings import KeyBindManager  <-- Removed to avoid circular import

        self.screen.bgpic("thumb.gif")

        # Define button positions
        start_pos = (0, 100)
        history_pos = (0, 0)
        exit_pos = (0, -100)
        key_pos = (0, -200)

        # Draw "Start Game" button and text
        self.selectStartGame.teleport(start_pos[0], start_pos[1])
        self.selectStartGame.shapesize(2, 20) # Approx 400px wide
        self.selectStartGame.showturtle()
        
        self.textTurtle.color("black") # Ensure text is visible on white buttons
        self.textTurtle.teleport(start_pos[0], start_pos[1] - 10)
        self.textTurtle.clear() # Clear previous
        self.textTurtle.write("Start Game (S)", align="center", font=("Arial", 16, "bold"))

        # Draw "History" button and text (using a new turtle or reusing textTurtle carefully)
        # Note: textTurtle is one object, we can write multiple times if we don't clear in between or use separate writers
        # But wait, textTurtle.write draws permanently on the canvas until cleared.
        
        self.selectHistory.teleport(history_pos[0], history_pos[1])
        self.selectHistory.shapesize(2, 20)
        self.selectHistory.showturtle()
        
        self.textTurtle.teleport(history_pos[0], history_pos[1] - 10)
        self.textTurtle.write("Score History (H)", align="center", font=("Arial", 16, "bold"))

        # Draw "Exit" button
        self.selectExit.teleport(exit_pos[0], exit_pos[1])
        self.selectExit.shapesize(2, 20)
        self.selectExit.showturtle()

        self.textTurtle.teleport(exit_pos[0], exit_pos[1] - 10)
        self.textTurtle.write("Exit Game (E or ESC)", align="center", font=("Arial", 16, "bold"))
        
        # Draw "Change Key" button
        self.changeKeyBindTurtle.teleport(key_pos[0], key_pos[1])
        self.changeKeyBindTurtle.shapesize(2, 20)
        self.changeKeyBindTurtle.showturtle()

        self.textTurtle.teleport(key_pos[0], key_pos[1] - 10)
        self.textTurtle.write("Settings (C)", align="center", font=("Arial", 16, "bold"))
        
        self.textTurtle.hideturtle()

        # KeyBindManager will be set up in main.py
        # self.keymanager=KeyBindManager(self.screen,"idle",)
        # self.keymanager.setup_keybinds()

if __name__ == "__main__":
    screen = ScreenClass()
    screen.imageSetup()
    screen.StartScreenSetup() 

    done()
