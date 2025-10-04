from turtle import *
from PIL import Image
from time import time, sleep
import random
from threading import Thread
import os
class TurtleSpaceGame:
    def __init__(self):
        self.state ="idle"
        self.t=Turtle()
        self.s=Screen()
        self.timer_turtle=Turtle()
        self.score_turtle=Turtle()
        self.selectExit=Turtle()
        self.selectHistory=Turtle()
        self.selectStartGame=Turtle()
        self.changeKeyBindTurtle=Turtle()
        self.time_elapsed=0
        self.timer_turtle.hideturtle()
        self.score_turtle.hideturtle()

        self.startKey="s"
        self.pauseKey="p"
        self.historyKey="h"
        self.backKey="b"
        self.resumeKey="r"
        self.exitKey="Escape"
        self.s.listen()
        
        img=Image.open("stars.gif")
        img=img.resize((1920, 1080))
        img.save("stars.gif")

        img=Image.open("thumb.gif")
        img=img.resize((1920, 1080))
        img.save("thumb.gif")
        
        img=Image.open("history.gif")
        img=img.resize((1920, 1080))
        img.save("history.gif")


        self.s.title("STAR CHASER")
        self.s.setup(width=1.0,height=1.0)
        
        self.s.onkeypress(self.run_caller, self.startKey)
        self.s.onkeypress(self.exit_caller, self.exitKey)
        self.s.onkeypress(self.back_caller, self.backKey)
        self.s.onkeypress(self.history_display_caller,self.historyKey)
        self.s.onkeypress(self.resume_caller,self.resumeKey)
        self.s.onkeypress(self.pause_caller, self.pauseKey)
        self.s.onkeypress(self.keyBindChange_caller,"c")

        self.selectExit.onclick(self.exit_caller)
        self.selectHistory.onclick(self.history_display_caller)
        self.selectStartGame.onclick(self.run_caller)
        self.changeKeyBindTurtle.onclick(self.keyBindChange_caller)
        


        self.start_screen()
    
    def keyBindChange_caller(self,x=None,y=None):

        if self.state=="idle":
            for x in ([self.selectHistory,self.changeKeyBindTurtle,self.selectHistory,self.selectExit,self.selectStartGame]):
                x.hideturtle()
            self.t.clear()
            self.change_state("changeKeyBind")
            


    def keyChange(self, attr_name, func):

        for x in [self.startChangerTurtle,self.historyDisplayChangerTurtle,self.pauseChanger, self.resumeChanger,self.backChanger, self.exitChanger]:
            x.clear()
            x.hideturtle()
        new_key = self.s.textinput("Key Bind Change", "Enter the new button to set (single key or special: enter, escape): ")
        if not new_key:
            self.t.write("No change made. Keeping old key.", align="center", font=("Courier", 16))
            return
        new_key = new_key.strip()
        mapping = {"enter": "Return", "return": "Return", "esc": "Escape", "escape": "Escape", "space": "space", " ": "space"}
        mapped_key = mapping.get(new_key.lower(), new_key)
        old_key = getattr(self, attr_name, None)
        if old_key:
            self.s.onkeypress(None, old_key)
        self.s.onkeypress(func, mapped_key)
        setattr(self, attr_name, mapped_key)
        self.s.listen()
        self.t.clear()
        self.t.teleport(20, -80)
        self.t.write(f"New key set: {mapped_key}", align="center", font=("Courier", 16))
        self.t.teleport(20, -110)
        self.t.write("Press B or click here to go back to settings", align="center", font=("Courier", 14))

        


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
            self.s.listen()


    def function_caller(self):
        if self.state == "idle":
            self.start_screen()

        elif self.state == "running":
            self.run_game()

        elif self.state=="changeKeyBind":
            self.changeKeyBind()




        elif self.state=="back":
            self.go_back()

        elif self.state=="history":
            self.history_display()

        elif self.state=="pause":
            self.pause()

        elif self.state=="resume":
            self.state="running"
            self.run_game()
    

    def pause(self):

        self.t.shape("square")
        self.t.onclick(self.resume_caller)
        self.t.shapesize(2,16)
        self.t.teleport(-30,0)
        self.t.write("Game paused, press R to resume",align="center",font=("Arial",16,"normal"))
        self.t.color("")


    

    def change_state(self, new_state):
        if self.state==new_state:
            pass

        elif self.state=="running":
            if new_state=="pause":
                self.state=new_state
                self.function_caller()

            else:    
                pass
        
        elif self.state=="changeKeyBind":
            if new_state=="back":
                for x in [self.startChangerTurtle,self.historyDisplayChangerTurtle,self.pauseChanger, self.resumeChanger,self.backChanger, self.exitChanger]:
                    x.clear()
                self.t.clear()
                self.state="back"
                self.function_caller()

        else:
            self.state = new_state
            self.function_caller()


    def resume_caller(self,x=None,y=None):
        if self.state=="pause":
            self.t.clear()
            self.change_state("running")

        else:
            pass

    def back_caller(self,x=None,y=None):
        
        if self.state=="history":
            self.scturtle.clear()
            self.scturtle.hideturtle()
            self.change_state("back")
        elif self.state=="changeKeyBind":
            self.change_state("back")

            
    
    def run_caller(self,x=None,y=None):
        if self.state=="idle" or self.state=="exit":
            return self.change_state("running")
        else:
            pass
    
    def exit_caller(self,x=None,y=None):
        return self.exit_game()

    def history_display_caller(self,x=None,y=None):
        if self.state=="idle" or self.state=="exit":
            return self.change_state("history")
        else:
            pass

        
    def pause_caller(self):
        if self.state == "running":
            self.change_state("pause")



    def go_back(self):
        self.change_state("idle")


    def history_display(self):
        if self.state!="running":
            
            self.selectExit.hideturtle()
            self.selectHistory.hideturtle()
            self.selectStartGame.hideturtle()
            self.s.bgpic("history.gif")
        
            self.t.clear()
            self.timer_turtle.clear()
            self.score_turtle.clear()
            self.t.hideturtle()
            self.timer_turtle.hideturtle()
            self.score_turtle.hideturtle()
        
            self.file_sorter()
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

   
    def start_screen(self):

        

        self.s.bgpic("thumb.gif")
        self.t.color("white")
        self.t.teleport(70,0)
        self.t.write("PRESS S TO START GAME\n\nPRESS H TO DISPLAY SCORE HISTORY\n\nPRESS ESCAPE TO EXIT THE GAME\n\nPRESS C TO CHANGE KEY SETTINGS",align="center",font=("Arial",16,"normal"))
        self.t.hideturtle()

        self.selectStartGame.showturtle()
        self.selectExit.showturtle()
        self.selectHistory.showturtle()
        
        self.changeKeyBindTurtle.color("")
        self.changeKeyBindTurtle.shape("square")
        self.changeKeyBindTurtle.shapesize(1,19)
        self.changeKeyBindTurtle.teleport(60,10)

        
        self.selectStartGame.color("")
        self.selectStartGame.shape("square")
        self.selectStartGame.shapesize(1,13)
        self.selectStartGame.teleport(0,160)

        self.selectHistory.color("")
        self.selectHistory.shape("square")
        self.selectHistory.shapesize(1,20)
        self.selectHistory.teleport(67,110)

        self.selectExit.color("")
        self.selectExit.shape("square")
        self.selectExit.shapesize(1,17.8)
        self.selectExit.teleport(50,60)


    def exit_game(self):
        return self.s.bye()

    def tele(self):
        
        self.t.teleport(random.randint(-300, 300), random.randint(-300, 300))
        

    def click_on_turtle(self,x,y):

        if self.state=="running":
            self.score+=1
            self.score_display(self.score)
            self.inner_timer=max(0.5,self.inner_timer-0.2)
            self.tele()

    def time_display(self,x):
        while self.time_elapsed<10 and self.state=="running":
            self.time_elapsed+=1
            sleep(1)
            self.timer_turtle.clear()
            self.timer_turtle.write(("Time:" + str(self.time_elapsed)), align="left",font=("Arial",24,"bold"))

    def score_display(self,sc):
        self.score_turtle.clear()
        self.score_turtle.write("Score:" +str(sc),align="left",font=("Arial",24,"bold"))

    def run_game(self):
        if self.time_elapsed==0:
            self.t.clear()
            
            self.selectExit.hideturtle()
            self.selectHistory.hideturtle()
            self.selectStartGame.hideturtle()
            self.s.bgpic("thumb.gif")
            self.score=0
            self.inner_timer=3

            self.t.shape("circle")
            self.t.shapesize(1,1)
            self.t.color("white")
            self.t.penup()
        
            self.timer_turtle.color("white")
            self.timer_turtle.hideturtle()
            self.timer_turtle.penup()
            self.timer_turtle.goto(-750,370)

            self.score_turtle.color("white")
            self.score_turtle.hideturtle()
            self.score_turtle.penup()
            self.score_turtle.goto(-550,370)
        
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

    def end_game(self):
        if not os.path.exists("score_history.txt"):
            self.score_file= open("score_history.txt","x")
            self.score_file.close()

            self.score_file=open("score_history.txt","w")
            self.score_file.write("ONLY TOP 5 SCORES ARE SHOWN\n\n\n\n")
            self.score_file.write(str(self.score))
            self.score_file.close()
        else:
            self.score_file=open("score_history.txt","a")
            self.score_file.write(str(self.score))
            self.score_file.close()
        
        self.state="exit"
        self.t.teleport(0,0)
        self.t.hideturtle()
        self.timer_turtle.clear()
        self.score_turtle.clear()
        self.t.write("Game Over! Your score is:" +str(self.score)+"\n\n\n\n\n\n\n\n\n\n", align="center", font=("Arial", 16, "normal"))
        self.start_screen()

newgame = TurtleSpaceGame()
done()
