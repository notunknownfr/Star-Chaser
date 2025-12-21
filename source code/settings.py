
from state_machine import GameState
from score_manager import FileManager
from turtle_factory import TurtleFactory

class KeyBindManager:
    def __init__(self, screen_class, state: GameState, game, fileManager: FileManager):
        self.gameState = state
        self.state = state
        self.game = game
        self.file = fileManager
        self.screen_class = screen_class 
        self.screen = screen_class.screen
        
        self.scturtle = TurtleFactory("circle", "white")
        self.scturtle.hideturtle()  
        self.startKey = "s"
        self.pauseKey = "p"
        self.historyKey = "h"
        self.backKey = "b"
        self.resumeKey = "r"
        self.exitKey = "Escape"
        self.keyBindChangeKey = "c"

    def setup_keybinds(self):
        self.screen.listen()  
        self.screen.onkeypress(self.run_caller, self.startKey)
        self.screen.onkeypress(self.history_display_caller, self.historyKey)
        self.screen.onkeypress(self.exit_caller, self.exitKey)
        self.screen.onkeypress(self.exit_caller, "e")  
        self.screen.onkeypress(self.keyBindChange_caller, self.keyBindChangeKey)
        self.screen.onkeypress(self.pause_caller, self.pauseKey)
        self.screen.onkeypress(self.resume_caller, self.resumeKey)
        self.screen.onkeypress(self.back_caller, self.backKey)

    def function_caller(self):
        curr = self.state.currentState
        if curr == "idle":
            pass
        elif curr == "running":
            self.start_game()
        elif curr == "changeKeyBind":
            self.changeKeyBind()
        elif curr == "back":
            self.go_back()
        elif curr == "history":
            self.history_display()
        elif curr == "pause":
            self.pause()
        elif curr == "resume":
            self.state.currentState = "running"
            self.start_game()

    def resume_caller(self, x=None, y=None):
        if self.state.currentState == "pause":
            self.screen_class.textTurtle.clear()
            self.state.change_state("resume")

    def back_caller(self, x=None, y=None):
        if self.state.currentState == "history":
            self.scturtle.clear()
            self.scturtle.hideturtle()
            self.state.change_state("back")
        elif self.state.currentState == "changeKeyBind":
            self.state.change_state("back")

    def run_caller(self, x=None, y=None):
        if self.state.currentState == "idle" or self.state.currentState == "exit":
            self.state.change_state("running")

    def exit_caller(self, x=None, y=None):
        self.exit()

    def history_display_caller(self, x=None, y=None):
        if self.state.currentState == "idle" or self.state.currentState == "exit":
            self.state.change_state("history")

    def pause_caller(self, x=None, y=None):
        if self.state.currentState == "running":
            self.state.change_state("pause")

    def keyBindChange_caller(self, x=None, y=None):
        if self.state.currentState == "idle":
            TurtleFactory.hideAllTurtles()
            self.screen_class.textTurtle.clear()
            self.state.change_state("changeKeyBind")

    def exit(self):
        try:
            self.screen.bye()
        except Exception:
            pass

    def pause(self):
        self.screen_class.textTurtle.shape("square")
        self.screen_class.textTurtle.onclick(self.resume_caller)
        self.screen_class.textTurtle.shapesize(2, 16)
        self.screen_class.textTurtle.teleport(-30, 0)
        self.screen_class.textTurtle.write("Game paused, press R to resume", align="center", font=("Arial", 16, "normal"))
        self.screen_class.textTurtle.color("")

    def start_game(self):
     
        if self.state.currentState == "running" or self.state.currentState == "resume": 
             self.game.start_game()

    def go_back(self):
        
        if hasattr(self, 'scturtle'):
            self.scturtle.clear()
            self.scturtle.hideturtle()
        
       
        self.screen.bgpic("thumb.gif")
        
       
        self.screen_class.selectExit.showturtle()
        self.screen_class.selectHistory.showturtle()
        self.screen_class.selectStartGame.showturtle()
        self.screen_class.changeKeyBindTurtle.showturtle()
       
        self.screen_class.textTurtle.clear()
        self.screen_class.textTurtle.color("black")
        
        
        start_pos = (0, 100)
        history_pos = (0, 0)
        exit_pos = (0, -100)
        key_pos = (0, -200)
        
        self.screen_class.textTurtle.teleport(start_pos[0], start_pos[1] - 10)
        self.screen_class.textTurtle.write("Start Game (S)", align="center", font=("Arial", 16, "bold"))
        
        self.screen_class.textTurtle.teleport(history_pos[0], history_pos[1] - 10)
        self.screen_class.textTurtle.write("Score History (H)", align="center", font=("Arial", 16, "bold"))
        
        self.screen_class.textTurtle.teleport(exit_pos[0], exit_pos[1] - 10)
        self.screen_class.textTurtle.write("Exit Game (E or ESC)", align="center", font=("Arial", 16, "bold"))
        
        self.screen_class.textTurtle.teleport(key_pos[0], key_pos[1] - 10)
        self.screen_class.textTurtle.write("Settings (C)", align="center", font=("Arial", 16, "bold"))
        
        self.screen_class.textTurtle.hideturtle()
        
        # Change state to idle
        self.state.change_state("idle")

    def history_display(self):
        if self.state.currentState != "running":
            # Hide menu elements
            self.screen_class.selectExit.hideturtle()
            self.screen_class.selectHistory.hideturtle()
            self.screen_class.selectStartGame.hideturtle()
            self.screen_class.changeKeyBindTurtle.hideturtle()
            
            self.screen.bgpic("history.gif")
        
            self.screen_class.textTurtle.clear()
            self.game.timer_turtle.clear()
            self.game.score_turtle.clear()
            self.screen_class.textTurtle.hideturtle()
            self.game.timer_turtle.hideturtle()
            self.game.score_turtle.hideturtle()
        
            self.file.file_sorter()
            
            try:
                with open("source/score_history.txt", "r") as f:
                    his = f.read()
            except FileNotFoundError:
                his = "No history yet."

            if not hasattr(self, 'scturtle') or self.scturtle is None:
                 self.scturtle = TurtleFactory()
            
            self.scturtle.clear()
            self.scturtle.hideturtle()
            self.scturtle.color("white")
            
            self.scturtle.teleport(0, 200)
            self.scturtle.write(his, align="center", font=("Arial", 16, "normal"))
    
            self.scturtle.teleport(0, -250)
            self.scturtle.write("Press B to go back to main menu", align="center", font=("Arial", 16, "normal"))
            
            
            self.scturtle.teleport(0, -250)
            self.scturtle.showturtle()
            self.scturtle.shape("square")
            self.scturtle.shapesize(1, 16)
            self.scturtle.onclick(self.back_caller)
            self.scturtle.color("")

    def keyChange(self, attr_name, func):
        for x in [self.startChangerTurtle, self.historyDisplayChangerTurtle, self.pauseChanger, self.resumeChanger, self.backChanger, self.exitChanger]:
            x.clear()
            x.hideturtle()
        new_key = self.screen.textinput("Key Bind Change", "Enter the new button to set (single key or special: enter, escape): ")
        
        if not new_key:
            self.screen_class.textTurtle.clear()
            self.screen_class.textTurtle.color("white")
            self.screen_class.textTurtle.write("No change made.", align="center", font=("Arial", 20, "bold"))
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
        
        self.screen_class.textTurtle.clear()
        self.screen_class.textTurtle.color("white")  
        self.screen_class.textTurtle.teleport(0, 0)
        self.screen_class.textTurtle.write(f"New key set: {mapped_key}", align="center", font=("Arial", 24, "bold"))
        self.screen_class.textTurtle.teleport(0, -50)
        self.screen_class.textTurtle.write("Press B to go back", align="center", font=("Arial", 18, "normal"))

    def changeKeyBind(self):
        self.startChangerTurtle = TurtleFactory()
        self.historyDisplayChangerTurtle = TurtleFactory()
        self.exitChanger = TurtleFactory()
        self.pauseChanger = TurtleFactory()
        self.resumeChanger = TurtleFactory()
        self.backChanger = TurtleFactory()
        font_size = 23

        self.startChangerTurtle.onclick(lambda x, y: self.keyChange("startKey", self.run_caller))
        self.historyDisplayChangerTurtle.onclick(lambda x, y: self.keyChange("historyKey", self.history_display_caller))
        self.pauseChanger.onclick(lambda x, y: self.keyChange("pauseKey", self.pause_caller))
        self.resumeChanger.onclick(lambda x, y: self.keyChange("resumeKey", self.resume_caller))
        self.backChanger.onclick(lambda x, y: self.keyChange("backKey", self.back_caller))
        self.exitChanger.onclick(lambda x, y: self.keyChange("exitKey", self.exit_caller))

        yDim = 200
        turtles = [self.startChangerTurtle, self.historyDisplayChangerTurtle, self.pauseChanger, self.resumeChanger, self.backChanger, self.exitChanger]
        
        for x in turtles:
            x.color("#DCCFC2")
            x.teleport(0, yDim)
            yDim -= 70

        self.startChangerTurtle.write("Press here to change 'start' button keybind", align="center", font=("Arial", font_size))
        self.historyDisplayChangerTurtle.write("Press here to change 'History display' button keybind", align="center", font=("Arial", font_size))
        self.pauseChanger.write("Press here to change 'pause' button keybind", align="center", font=("Arial", font_size))
        self.resumeChanger.write("Press to change 'resume' button keybind", align="center", font=("Arial", font_size))
        self.backChanger.write("Press here to change 'back' button keybind", align="center", font=("Arial", font_size))
        self.exitChanger.write("Press here to change 'Exit' button keybind", align="center", font=("Arial", font_size))

        for x in turtles:
            x.shape("square")
            yDim = x.ycor()
            x.teleport(0, yDim + 15)

            if x == self.historyDisplayChangerTurtle:
                x.shapesize(2, 35.5)
            else:
                x.shapesize(2, 29)
            x.color("")
        
        self.screen.listen()
