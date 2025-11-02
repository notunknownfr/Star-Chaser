from threading import Thread
from turtle_factory import TurtleFactory
from screen import ScreenClass
from state_machine import GameState
from time import time, sleep
from settings import KeyBindManager

class Game:
    def __init__(self, state: GameState, sc:ScreenClass):
        self.screen=sc.screen
        self.score=0
        self.state=state.currentState
        self.time_elapsed=0
        self.selectExit=sc.selectExit
        self.selectHistory=sc.selectHistory
        self.selectStartGame=sc.selectStartGame
        self.timer_turtle=TurtleFactory("square","white",-750,370)
        self.score_turtle=TurtleFactory("","white",-550,370)
        self.t=sc.textTurtle
    def start_game(self):

        if self.time_elapsed==0:

            self.selectExit.hideturtle()
            self.selectHistory.hideturtle()
            self.selectStartGame.hideturtle()
            self.screen.bgpic("thumb.gif")
            self.score=0
            self.inner_timer=3
            self.t.shapesize(1,1)
            self.timer_turtle.hideturtle()
            self.score_turtle.hideturtle()
        
            self.score_display(0)
            self.timer_turtle.write("Time:" + "0" ,align="left",font=("Arial",24,"bold"))
        else:
            self.t.shape("circle")
            self.t.color("white")
            self.t.shapesize(1,1)
            
            
    def time_display(self,x):
        while self.time_elapsed<10 and self.state=="running":
            self.time_elapsed+=1
            sleep(1)
            self.timer_turtle.clear()
            self.timer_turtle.write(("Time:" + str(self.time_elapsed)), align="left",font=("Arial",24,"bold"))


    def startTimeThread(self):   
        Thread(target=self.time_display,args=(self.time_elapsed,),daemon=True).start()
        self.t.showturtle()
        self.t.onclick(self.click_on_turtle)

        while self.time_elapsed< 10 and self.state =="running":
            current_time=time()
            next_move_time=current_time + self.inner_timer

            while time() < next_move_time and self.state=="running":
                self.screen.update()
                sleep(0.01)

            if self.state=="running":
                self.t.randomTeleport()

        if self.state=="running":
            self.time_elapsed=0
            KeyBindManager.exit()  #CANNOT ACCES KEYBINDMANAGER CLASS #FIXED


    def score_display(self,s):
        self.score_turtle.clear()
        self.score_turtle.write("Score:" +str(s),align="left",font=("Arial",24,"bold"))
