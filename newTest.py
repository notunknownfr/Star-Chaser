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

class GameState:
    def __init__(self, state="idle"):
        self.currentState=state

    def changeState(self, newState:str):
        self.currentState=newState

        
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

class Game:
    def __init__(self, state: GameState, sc:ScreenClass, se:turtleCreator, sh:turtleCreator, ssg:turtleCreator, t:turtleCreator):
        self.screen=sc
        self.state=state
        self.time_elapsed=0
        self.selectExit=se
        self.selectHistory=sh
        self.selectStartGame=ScreenClass

    def start_game(self):

        if self.time_elapsed==0:
            self.timer_turtle=turtleCreator("square","white",-750,370)
            self.score_turtle=turtleCreator("","white",-550,370)
            
            self.selectExit.hideturtle()
            self.selectHistory.hideturtle()
            self.selectStartGame.hideturtle()
            self.screen.bgpic("thumb.gif")
            self.score=0
            self.inner_timer=3

            self.t.shape("circle")
            self.t.shapesize(1,1)
            self.t.color("white")
    

            self.timer_turtle.hideturtle()
            self.score_turtle.hideturtle()
        
            self.score_display(0)
            self.timer_turtle.write("Time:" + "0" ,align="left",font=("Arial",24,"bold"))
        else:
            self.t.shape("circle")
            self.t.color("white")
            self.t.shapesize(1,1)
            
            
        

        Thread(target=self.time_display,args=(self.time_elapsed,),daemon=True).start()
        self.t.showturtle()
        self.t.onclick(self.click_on_turtle)

        while self.time_elapsed< 10 and self.state =="running":
            current_time=time()
            next_move_time=current_time + self.inner_timer

            while time() < next_move_time and self.state=="running":
                self.s.update()
                sleep(0.01)

            if self.state=="running":
                self.tele()

        if self.state=="running":
            self.time_elapsed=0
            self.end_game()


class fileManager:
    def __init__(self,scoreFile):
        self.score_file=scoreFile
    

    def history_display(self):
            
            self.score_file= open("score_history.txt","r")

            his=self.score_file.read()
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

