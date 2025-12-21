from turtle_factory import TurtleFactory
from screen import ScreenClass
from state_machine import GameState
from settings import KeyBindManager

class Game:
    def __init__(self, state: GameState, sc:ScreenClass):
        self.screen=sc.screen
        self.screen_class = sc  #Store reference to ScreenClass
        self.score=0
        self.state_manager = state  #Store the GameState object
        self.time_elapsed=0
        self.selectExit=sc.selectExit
        self.selectHistory=sc.selectHistory
        self.selectStartGame=sc.selectStartGame
        self.timer_turtle=TurtleFactory("square","white",-750,370)
        self.score_turtle=TurtleFactory("square","white",-550,370)
        #Hide timer and score turtles initially (only show during gameplay)
        self.timer_turtle.hideturtle()
        self.score_turtle.hideturtle()
        self.t=sc.textTurtle
        self.keyBindManager = None #Initialize to None

    def start_game(self):
        if self.time_elapsed == 0:
            #Hide all menu buttons
            self.selectExit.hideturtle()
            self.selectHistory.hideturtle()
            self.selectStartGame.hideturtle()
            self.screen_class.changeKeyBindTurtle.hideturtle()
            
            #Hide the scturtle from KeyBindManager 
            if self.keyBindManager and hasattr(self.keyBindManager, 'scturtle'):
                self.keyBindManager.scturtle.hideturtle()
            
            #Clear menu text
            self.t.clear()
            
            self.screen.bgpic("thumb.gif")
            self.score = 0
            self.inner_timer = 3
            
            #Set up the clickable turtle as a white circle
            self.t.shape("circle")
            self.t.color("white")
            self.t.shapesize(1, 1)
            
            #Keep timer and score turtles hidden, only show text
            self.timer_turtle.hideturtle()
            self.score_turtle.hideturtle()
            self.score_display(0)
            self.timer_turtle.write("Time:" + "0", align="left", font=("Arial", 24, "bold"))
            
            #Start the game loop
            self.startTimeThread()
        else:
            #Resuming from pause
            self.t.shape("circle")
            self.t.color("white")
            self.t.shapesize(1, 1)
            
            #Clear pause message
            self.t.clear()
            
            self.t.onclick(self.click_on_turtle)
            
            #Restart the timer
            self.screen.ontimer(self.time_display, 1000)
            self.screen.ontimer(self.move_turtle, int(self.inner_timer * 1000))

    def time_display(self):
        if self.time_elapsed < 10 and self.state_manager.currentState == "running":
            self.time_elapsed += 1
            self.timer_turtle.clear()
            self.timer_turtle.write(("Time:" + str(self.time_elapsed)), align="left", font=("Arial", 24, "bold"))
            

            self.screen.ontimer(self.time_display, 1000)
        elif self.time_elapsed >= 10:
             
            #Game Over logic
            self.end_game()

    def startTimeThread(self):
        #Initial call to timer logic
        self.t.showturtle()
        self.t.onclick(self.click_on_turtle)
        
        #Start the timer loop
        self.screen.ontimer(self.time_display, 1000)
        
        self.move_turtle()

    def move_turtle(self):
        if self.state_manager.currentState == "running" and self.time_elapsed < 10:
             self.t.randomTeleport()
             #Schedule next move based on inner_timer
             self.screen.ontimer(self.move_turtle, int(self.inner_timer * 1000))

    def click_on_turtle(self, x, y):
        if self.state_manager.currentState == "running":
            self.score += 1
            self.score_display(self.score)
            self.t.randomTeleport()

    def end_game(self):
      
        if self.keyBindManager:
            self.keyBindManager.state.currentState = "game_over"
        
        #Save the score to file
        if self.score > 0:
            try:
                with open("source/score_history.txt", "a") as f:
                    f.write(str(self.score) + "\n")
            except Exception as e:
                print(f"Error saving score: {e}")
        
        # Hide the game turtle
        self.t.hideturtle()
        
        # Clear timer and score displays
        self.timer_turtle.clear()
        self.score_turtle.clear()
        
        # Show game over screen
        self.show_game_over()
    
    def show_game_over(self):
        #Create a game over display
        self.t.clear()
        self.t.shape("square")
        self.t.color("white")
        self.t.teleport(0, 50)
        self.t.write(f"GAME OVER!", align="center", font=("Arial", 32, "bold"))
        
        self.t.teleport(0, 0)
        self.t.write(f"Your Score: {self.score}", align="center", font=("Arial", 24, "normal"))
        
        self.t.teleport(0, -50)
        self.t.write("Press SPACE to return to menu", align="center", font=("Arial", 16, "normal"))
        
        # Set up space key to return to menu
        self.screen.onkeypress(self.return_to_menu, "space")
        self.screen.listen()
    
    def return_to_menu(self):
        # Clear the game over screen
        self.t.clear()
        
        # Reset game state
        self.time_elapsed = 0
        self.score = 0
        
        # Unbind the space key handler
        self.screen.onkeypress(None, "space")
        
        # Explicitly set state to idle FIRST
        if self.keyBindManager:
            self.keyBindManager.state.currentState = "idle"
        
        # Go back to menu (this restores menu visuals)
        if self.keyBindManager:
            self.keyBindManager.go_back()
        
        # Then re-setup the menu keybinds
        if self.keyBindManager:
            self.keyBindManager.setup_keybinds() 



    def score_display(self,s):
        self.score_turtle.clear()
        self.score_turtle.write("Score:" +str(s),align="left",font=("Arial",24,"bold"))
