from turtle import *
from PIL import Image
from time import time, sleep
import random
from threading import Thread
import os

turtlesList=[]


class turtleCreator(Turtle):
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

    def TurtleTeleport(self,x,y):
            self.newTurtle.teleport(x,y)

    def TurtleRandomTeleport(self,x,y):
        self.newTurtle.teleport(random.randint(-300, 300), random.randint(-300, 300))

    def turtleDeletion(self):
         self.newTurtle.clear()

    def changeShape(self,shape):
         self.newTurtle.shape(shape)

    def changeSize(self,width,length):
         self.newTurtle.shapesize(width,length)

    def changeColor(self,newColor):
        self.newTurtle.color(newColor)

    def writeTurtle(self,text):
        self.newTurtle.write(text,font=("Arial",20,"normal"))



class ScreenClass:
    def __init__(self):
        
        self.newScreen=Screen()
        self.newScreen.setup(1.0,1.0)


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
        self.newScreen.bgpic("thumb.gif")

        t=turtleCreator("square","white",0,70)
        t.changeColor("white")
        t.TurtleTeleport(-230,-30)
        t.writeTurtle("PRESS S TO START GAME\n\nPRESS H TO DISPLAY SCORE HISTORY\n\nPRESS ESCAPE TO EXIT THE GAME\n\nPRESS C TO CHANGE KEY SETTINGS")
        t.hideTurtle()
        
        selectStartGame=turtleCreator("square","",-58,180)
        selectStartGame.changeSize(1.3,17)

        selectHistory=turtleCreator("square","",25.9,115)
        selectHistory.changeSize(1.3,25.8)

        selectExit=turtleCreator("square","",2,50)
        selectExit.changeSize(1.3,23.2)
        
        changeKeyBindTurtle=turtleCreator("square","",15,-17)
        changeKeyBindTurtle.changeSize(1.3,24.3)

        keymanager=KeyBindManager(self.newScreen)
        keymanager.setup_keybinds()


class KeyBindManager:
    def __init__(self,screen):
        self.screen=screen

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
    def __init__(self,sc,se,sh,ssg,t):
        self.screen=sc
        self.time_elapsed=0
        self.selectExit=se
        self.selectHistory=sh
        self.selectStartGame=ssg
        self.timer_turtle=turtleCreator("square","white",-750,370)
        self.t=t
        self.score_turtle=turtleCreator("","white",-550,370)


    def start_game(self,t):
        if self.time_elapsed==0:
            
            self.selectExit.hideTurtle()
            self.selectHistory.hideTurtle()
            self.selectStartGame.hideTurtle()
            self.screen.bgpic("thumb.gif")
            self.score=0
            self.inner_timer=3

            self.t.changeShape("circle")
            self.t.shapesize(1,1)
            self.t.changeColor("white")
    

            self.timer_turtle.hideTurtle()
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


x=ScreenClass()

x.StartScreenSetup()





done()