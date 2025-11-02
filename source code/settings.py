from game import Game
from state_machine import GameState
from turtle import _Screen
from score_manager import FileManager
from turtle_factory import TurtleFactory

class KeyBindManager:         #CONFUSION
    def __init__(self, screen: _Screen,state: GameState,game: Game, fileManager: FileManager):
        self.gameState=state
        self.state=state  #CONFUSION
        self.game=game
        self.file=fileManager
        self.screen = screen
        self.scturtle=TurtleFactory("circle","white")
        self.startKey="s"
        self.pauseKey="p"
        self.historyKey="h"
        self.backKey="b"
        self.resumeKey="r"
        self.exitKey="Escape"
        self.keyBindChangeKey="c"

    def setup_keybinds(self):
        self.screen.listen()  
        self.screen.onkeypress(self.start_game, self.startKey)
        self.screen.onkeypress(self.history_display, self.historyKey)
        self.screen.onkeypress(self.exit_caller, self.exitKey)
        self.screen.onkeypress(self.keyBindChange_caller, self.keyBindChangeKey)
        self.screen.onkeypress(self.pause_caller,self.pauseKey)
        self.screen.onkeypress(self.resume_caller,self.resumeKey)
        self.screen.onkeypress(self.back_caller,self.backKey)


    def function_caller(self):
        if self.state.currentState == "idle":
            #confusion 
            pass

        elif self.state.currentState == "running":
            self.start_game()

        elif self.state.currentState=="changeKeyBind":
            self.changeKeyBind()

        elif self.state.currentState=="back":
            self.go_back()

        elif self.state.currentState=="history":
            self.history_display()

        elif self.state.currentState=="pause":
            self.pause()

        elif self.state.currentState=="resume":
            self.state="running"
            self.start_game()
            


    def resume_caller(self,x=None,y=None):
        if self.state.currentState=="pause":
            self.screen.textTurtle.clear()  #CONFUSION
            self.state.change_state("resume")

        else:
            pass

    def back_caller(self,x=None,y=None):
        
        if self.state.currentState=="history":
            self.scturtle.clear()
            self.scturtle.hideturtle()
            self.state.change_state("back")
        elif self.state.currentState=="changeKeyBind":
            self.state.change_state("back")

            
    
    def run_caller(self,x=None,y=None):
        if self.state.currentState=="idle" or self.state.currentState=="exit":
            return self.state.change_state("running")
        else:
            pass
    
    def exit_caller(self,x=None,y=None):
        self.exit()

    def history_display_caller(self,x=None,y=None):
        if self.state.currentState=="idle" or self.state.currentState=="exit":
            self.state.change_state("history")
        else:
            pass

        
    def pause_caller(self):
        if self.state.currentState == "running":
            self.state.change_state("pause")

    def keyBindChange_caller(self,x=None,y=None):

        if self.state.currentState=="idle":
            TurtleFactory.hideAllTurtles()
            self.screen.textTurtle.clear()  # CONFUSION
            self.state.change_state("changeKeyBind")

    def exit(self):
        self.screen.bye()

    def pause(self):

        self.screen.textTurtle.shape("square")        #CONFUSION
        self.screen.textTurtle.onclick(self.resume_caller)
        self.screen.textTurtle.shapesize(2,16)
        self.screen.textTurtle.teleport(-30,0)
        self.screen.textTurtle.write("Game paused, press R to resume",align="center",font=("Arial",16,"normal"))
        self.screen.textTurtle.color("")


    def start_game(self):
        if self.state=="idle":
            #CONFUSION as don't have access startScreenSetup function from ScreenClass 
            pass

    def go_back(self):
        self.state.change_state("idle")


    def history_display(self):
        if self.state!="running":
            
            self.screen.selectExit.hideturtle()              #CONFUSION
            self.screen.selectHistory.hideturtle()
            self.screen.selectStartGame.hideturtle()
            self.screen.bgpic("history.gif")
        
            self.screen.textTurtle.clear()
            self.game.timer_turtle.clear()
            self.game.score_turtle.clear()
            self.screen.textTurle.hideturtle()    #CONFUSION
            self.game.timer_turtle.hideturtle()
            self.game.score_turtle.hideturtle()
        
            self.file.file_sorter()
            self.file.score_file= open("score_history.txt","r")

            his=self.file.score_file.read()
            self.scturtle=TurtleFactory()
            self.scturtle.hideturtle()
            self.scturtle.color("white")
            self.scturtle.write(his,align="center",font=("Arial",16,"normal"))
            self.scturtle.teleport(0, -250)
            self.scturtle.showturtle()
            self.scturtle.shape("square")
            self.scturtle.shapesize(1,16)
            self.scturtle.onclick(self.back_caller)
            self.scturtle.write("Press B to go back to main menu",align="center",font=("Arial",16,"normal"))
            self.scturtle.color("")

    def keyChange(self, attr_name, func):

        for x in [self.startChangerTurtle,self.historyDisplayChangerTurtle,self.pauseChanger, self.resumeChanger,self.backChanger, self.exitChanger]:
            x.clear()
            x.hideturtle()
        new_key = self.screen.textinput("Key Bind Change", "Enter the new button to set (single key or special: enter, escape): ")
        if not new_key:
            self.screen.textinput.write("No change made. Keeping old key.", align="center", font=("Courier", 16))
            return
        new_key = new_key.strip()
        mapping = {"enter": "Return", "return": "Return", "esc": "Escape", "escape": "Escape", "space": "space", " ": "space"}
        mapped_key = mapping.get(new_key.lower(), new_key)
        old_key = getattr(self, attr_name, None)
        if old_key:
            self.screen.onkeypress(None, old_key)
        self.screen.onkeypress(func, mapped_key)
        setattr(self, attr_name, mapped_key)
        self.screen.listen()
        self.screen.textTurtle.clear()
        self.screen.textTurtle.teleport(20, -80)
        self.screen.textTurtle.write(f"New key set: {mapped_key}", align="center", font=("Courier", 16))
        self.screen.textTurtle.teleport(20, -110)
        self.screen.textTurtle.write("Press B or click here to go back to settings", align="center", font=("Courier", 14))

        


    def changeKeyBind(self):
        self.startChangerTurtle=TurtleFactory()
        self.historyDisplayChangerTurtle=TurtleFactory()
        self.exitChanger=TurtleFactory()
        self.pauseChanger=TurtleFactory()
        self.resumeChanger=TurtleFactory()
        self.backChanger=TurtleFactory()
        font_size = 23

        self.startChangerTurtle.onclick(lambda x, y: self.keyChange("startKey", self.run_caller))
        self.historyDisplayChangerTurtle.onclick(lambda x, y: self.keyChange("historyKey", self.history_display_caller))
        self.pauseChanger.onclick(lambda x, y: self.keyChange("pauseKey", self.pause_caller))
        self.resumeChanger.onclick(lambda x, y: self.keyChange("resumeKey", self.resume_caller))
        self.backChanger.onclick(lambda x, y: self.keyChange("backKey", self.back_caller))
        self.exitChanger.onclick(lambda x, y: self.keyChange("exitKey", self.exit_caller))


        yDim=200
        for x in [self.startChangerTurtle,self.historyDisplayChangerTurtle,self.pauseChanger, self.resumeChanger,self.backChanger, self.exitChanger]:
            x.color("#DCCFC2")  
            x.teleport(0, yDim)
            yDim-=70

        self.startChangerTurtle.write("Press here to change 'start' button keybind", align="center", font=("Arial", font_size))
        self.historyDisplayChangerTurtle.write("Press here to change 'History display' button keybind", align="center", font=("Arial", font_size))
        self.pauseChanger.write("Press here to change 'pause' button keybind", align="center", font=("Arial", font_size))
        self.resumeChanger.write("Press  to change 'resume' button keybind", align="center", font=("Arial", font_size))
        self.backChanger.write("Press here to change 'back' button keybind", align="center", font=("Arial", font_size))
        self.exitChanger.write("Press here to change 'Exit' button keybind", align="center", font=("Arial", font_size))
        
        
        
        
        for x in [self.startChangerTurtle,self.historyDisplayChangerTurtle,self.pauseChanger, self.resumeChanger,self.backChanger, self.exitChanger]:
            x.shape("square")
            yDim=x.ycor()
            x.teleport(0,yDim+15)

            if x==self.historyDisplayChangerTurtle:
                x.shapesize(2, 35.5)
            else:
                x.shapesize(2, 29)  
            x.color("")
            self.screen.listen()
