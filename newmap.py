from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageDraw,ImageTk
from matplotlib.pyplot import grid
import numpy as np
# Define useful parameters
imagewidth=2200
width=2300
height=902
horizontalStepCount=100
verticalStepCount=height//(imagewidth//horizontalStepCount)
length=imagewidth//horizontalStepCount
Color={0:"none",1:"grey",2:"green",3:"red"} #열린목록 닫힌목록 길 등은 나중에 추가

class AStarPathFinding:
    def __init__(self):
        self.window=Tk()
        self.window.resizable(False,False)
        self.window.title("AStarPathFinding")
        imgpath="campusCapture.png"
        img=Image.open(imgpath)
        self.photo=ImageTk.PhotoImage(img)
        self.canvas=Canvas(self.window,width=width,height=height)
        self.canvas.pack()
        self.reset()
        self.window.bind("<Button-1>", self.click)
        self.resetBoard=False # 리셋버튼 따로 만들어서 제어
        self.nonebutton=Button(self.window,text="none", font=36, fg="black",command=self.BTnone)
        self.nonebutton.place(x=2220,y=100)
        self.wallbutton=Button(self.window,text="wall", font=36, fg="black",command=self.BTwall)
        self.wallbutton.place(x=2220,y=200)
        self.startbutton=Button(self.window,text="start", font=36, fg="black",command=self.BTstart)
        self.startbutton.place(x=2220,y=300)
        self.goalbutton=Button(self.window,text="goal", font=36, fg="black",command=self.BTgoal)
        self.goalbutton.place(x=2220,y=400)
        self.astarbutton=Button(self.window,text="astar", font=36, fg="black",command=self.BTastar)
        self.astarbutton.place(x=2220,y=500)
        self.resetbutton=Button(self.window, text="reset",font=36,fg="black",command=self.reset)
        self.resetbutton.place(x=2220,y=600) 
        self.modenumber=0
        self.startcount=0
        self.goalcount=0
    def boardZero(self):
        self.board=[]
        for i in range(verticalStepCount):
            for j in range(horizontalStepCount):
                self.board=np.zeros(shape=(horizontalStepCount,verticalStepCount))

    def initialize_board(self):
        for i in range(verticalStepCount):
            for j in range(horizontalStepCount):
                tagname="rect"+self.convertRecNum(j)+self.convertRecNum(i)
                if(self.board[j][i]==0): # none
                    self.canvas.create_rectangle(j*length,i*length,(j+1)*length,(i+1)*length,tag=tagname)
                elif(self.board[j][i]==1):# wall
                    self.canvas.create_rectangle(j*length,i*length,(j+1)*length,(i+1)*length,tag=tagname,fill="grey")
                elif(self.board[j][i]==2):# start
                    self.canvas.create_rectangle(j*length,i*length,(j+1)*length,(i+1)*length,tag=tagname,fill="green")
                elif(self.board[j][i]==3):# goal
                    self.canvas.create_rectangle(j*length,i*length,(j+1)*length,(i+1)*length,tag=tagname,fill="red")

        for i in range(horizontalStepCount+1):#horizontal line
            self.canvas.create_line(
                imagewidth/horizontalStepCount*i,0,imagewidth/horizontalStepCount*i,height,
            )

        for i in range(verticalStepCount+1): #vertical line
            self.canvas.create_line(
                0, i * height / verticalStepCount , imagewidth, i * height / verticalStepCount,
            )

    def reset(self):
        self.boardZero()
        self.canvas.create_image(1093,451,image=self.photo)
        self.initialize_board()
    def mainloop(self):
        self.window.mainloop()
    def BTnone(self):
        self.modenumber=0
    def BTwall(self):
        self.modenumber=1
        self.initialize_board()
    def BTstart(self):
        self.modenumber=2
    def BTgoal(self):
        self.modenumber=3
    def BTastar(self):
        if self.startcount==1 and self.goalcount==1 :
            print() # astar 알고리즘 탐색
        else:
            messagebox.showinfo("Error","Start and Goal must have only one!!")
    def drawRec(self,logical_position):
        logical_position=np.array(logical_position)
        x=int(logical_position[0])
        y=int(logical_position[1])
        tagname="rect"+self.convertRecNum(x)+self.convertRecNum(y)
        if not self.modenumber==0 :
            self.canvas.create_rectangle(x*length,y*length,(x+1)*length,(y+1)*length,tag=tagname,fill=Color[self.modenumber])
            self.board[logical_position[0]][logical_position[1]]=self.modenumber
        if self.modenumber==2:
            self.startcount+=1
        if self.modenumber==3:
            self.goalcount+=1

    def deleteRec(self,logical_position):
        if not self.modenumber==0:
            x=int(logical_position[0])
            y=int(logical_position[1])
            tagname="rect"+self.convertRecNum(x)+self.convertRecNum(y)
            self.canvas.delete(tagname)
            self.board[logical_position[0]][logical_position[1]]=0
        if self.modenumber==2:
            self.startcount-=1
        if self.modenumber==3:
            self.goalcount-=1

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (imagewidth / horizontalStepCount) * logical_position + imagewidth / (horizontalStepCount*2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (imagewidth / horizontalStepCount), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True
    def convertRecNum(self,num):
        if(num//100!=0):
            return str(num)
        elif(num//10!=0):
            return "0"+str(num)
        else:
            return "00"+str(num)
    def click(self,event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        if logical_position[0]>3 or logical_position[1]>3: #버튼 눌렀을 때 사각형이 클릭되었다고 인식하지않기 위해
            if not self.is_grid_occupied(logical_position):
                self.drawRec(logical_position) # 나중에 draw안에 넣을것 
            else:
                self.deleteRec(logical_position)
    


game_instance=AStarPathFinding()
game_instance=mainloop()