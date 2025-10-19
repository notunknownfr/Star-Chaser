from turtle import _Screen, Turtle, done
from PIL import Image
from time import time, sleep
import random
from threading import Thread
import os

turtlesList=[]


class TurtleCreator(Turtle):
    def __init__(self,shape,color,xCoor=0,yCoor=0):
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



class ScreenClass(_Screen):
    def __init__(self):
        self.screen=_Screen
        self.screen.setup(1.0, 1.0)
        self.selectStartGame = TurtleCreator("square", "white", -58, 180)
        self.selectHistory = TurtleCreator("square", "white", 25.9, 115)
        self.selectExit = TurtleCreator("square", "white", 2, 50)
        self.changeKeyBindTurtle = TurtleCreator("square", "white", 15, -17)
        self.textTurtle=TurtleCreator("square","white",0,70)


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


class GameState:
    def __init__(self, screen: ScreenClass, state="idle"):
        self.currentState=state
        self.screen=screen


    def change_state(self, new_state):
        if self.currentState==new_state:
            pass

        elif self.currentState=="running":
            if new_state=="pause":
                self.currentState=new_state
                self.screen.keymanager.function_caller()

            else:    
                pass
        
        elif self.currentState=="changeKeyBind":
            if new_state=="back":
                self.currentState="back"
                self.screen.keymanager.function_caller()

        else:
            self.currentState = new_state
            self.screen.keymanager.function_caller()

class FileManager:
    def __init__(self,scoreFile, keybindmanager:keyBindManager):   #CANNOT PASS A KEYBINDMANAGER OBJECT REFERENCE
        self.score_file=scoreFile
    

    def history_display(self):
            
            self.score_file= open("score_history.txt","r")

            his=self.score_file.read()
            self.scturtle=Turtle("square","white",0,-250)
            self.scturtle.write(his,align="center",font=("Arial",16,"normal"))
            self.scturtle.shapesize(1,16)
            self.scturtle.onclick(self.KeyBindManager.back_caller)     #CANNOT ACCESS THE KEYBIND MANAGER CLASS
            self.scturtle.write("Press B to go back to main menu",align="center",font=("Arial",16,"normal"))
            self.scturtle.color("")

    def file_sorter(self):
        self.score_file=open("score_history.txt")
        self.highest_arr=[]
        for x in range(4):
            self.score_file.readline()

        self.line=self.score_file.readline()
        while self.line:
            self.highest_arr.append(int(self.line))
            self.line= self.score_file.readline()
        self.score_file.close()
        for x in range(len(self.highest_arr)):
            for y in range(len(self.highest_arr)-1-x):
                if self.highest_arr[y]<self.highest_arr[y+1]:
                    self.highest_arr[y],self.highest_arr[y+1]=self.highest_arr[y+1],self.highest_arr[y]
        
        self.score_file=open("score_history.txt","w")
        

        self.score_file.write("ONLY TOP 5 SCORES ARE SHOWN\n\n\n\n")
        if len(self.highest_arr)>5:
            for x in range(5):
                self.score_file.write(str(self.highest_arr[x]))
                self.score_file.write("\n")
        else:
            for x in range(len(self.highest_arr)):
                self.score_file.write(str(self.highest_arr[x]))
                self.score_file.write("\n")

                
        self.score_file.close()



class Game:
    def __init__(self, state: GameState, sc:ScreenClass):
        self.screen=sc.screen
        self.score=0
        self.state=state.currentState
        self.time_elapsed=0
        self.selectExit=sc.selectExit
        self.selectHistory=sc.selectHistory
        self.selectStartGame=sc.selectStartGame
        self.timer_turtle=TurtleCreator("square","white",-750,370)
        self.score_turtle=TurtleCreator("","white",-550,370)
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
            self.keyBindManager.exit()  #CANNOT ACCES KEYBINDMANAGER CLASS


    def score_display(self,s):
        self.score_turtle.clear()
        self.score_turtle.write("Score:" +str(s),align="left",font=("Arial",24,"bold"))


class KeyBindManager:         #CONFUSION
    def __init__(self, screen: _Screen,state: GameState,game: Game, fileManager: FileManager):
        self.gameState=state
        self.state=state  #CONFUSION
        self.game=game
        self.file=fileManager
        self.screen = screen
        self.scturtle=TurtleCreator("circle","white")
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
            TurtleCreator.hideAllTurtles()
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
            self.scturtle=Turtle()
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
        self.startChangerTurtle=Turtle()
        self.historyDisplayChangerTurtle=Turtle()
        self.exitChanger=Turtle()
        self.pauseChanger=Turtle()
        self.resumeChanger=Turtle()
        self.backChanger=Turtle()
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

done()

#TEST