from turtle import Turtle
from settings import KeyBindManager

class FileManager:
    def __init__(self,scoreFile,  keybindmanager:KeyBindManager):   #CANNOT PASS A KEYBINDMANAGER OBJECT REFERENCE 
        self.score_file=scoreFile
    

    def history_display(self):
            
            self.score_file= open("score_history.txt","r")

            his=self.score_file.read()
            self.scturtle=Turtle("square","white",0,-250)
            self.scturtle.write(his,align="center",font=("Arial",16,"normal"))
            self.scturtle.shapesize(1,16)
            self.scturtle.onclick(KeyBindManager.back_caller())     #CANNOT ACCESS THE KEYBIND MANAGER CLASS 
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

