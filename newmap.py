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
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
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
        self.nonebutton.place(x=2220,y=50)
        self.wallbutton=Button(self.window,text="wall", font=36, fg="black",command=self.BTwall)
        self.wallbutton.place(x=2220,y=150)
        self.startbutton=Button(self.window,text="start", font=36, fg="black",command=self.BTstart)
        self.startbutton.place(x=2220,y=250)
        self.goalbutton=Button(self.window,text="goal", font=36, fg="black",command=self.BTgoal)
        self.goalbutton.place(x=2220,y=350)
        self.astarbutton=Button(self.window,text="astar", font=36, fg="black",command=self.BTastar)
        self.astarbutton.place(x=2220,y=450)
        self.resetbutton=Button(self.window, text="reset",font=36,fg="black",command=self.reset)
        self.resetbutton.place(x=2220,y=550)
        self.savebutton=Button(self.window, text="save",font=36,fg="black",command=self.BTsave)
        self.savebutton.place(x=2220,y=650)
        self.loadbutton=Button(self.window, text="load",font=36,fg="black",command=self.BTload)
        self.loadbutton.place(x=2220,y=750)
        self.modenumber=0
        self.startcount=0
        self.goalcount=0

    #initialize the board matrix to 0
    def boardZero(self):
        self.board=[]
        for i in range(verticalStepCount):
            for j in range(horizontalStepCount):
                self.board=np.zeros(shape=(horizontalStepCount,verticalStepCount))

    #fill board regard to matrix and create line
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

    #reset board
    def reset(self):
        self.boardZero()
        self.canvas.create_image(1093,451,image=self.photo)
        self.initialize_board()

    def mainloop(self):
        self.window.mainloop()

    #---------------------------------------------------------
    #Button Command function
    #---------------------------------------------------------
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
    def BTsave(self):
        self.newWindow=Toplevel(self.window)
        self.newWindow.title("file save")
        self.newWindow.geometry("350x250")
        self.newWindow.resizable(False,False)
        Label(self.newWindow,text="filename").place(x=30,y=50)
        self.filename=Entry(self.newWindow,width=20)
        self.filename.place(x=100,y=50)
        Button(self.newWindow,text="Ok",command=self.filesave).place(x=30,y=130)
    def filesave(self):
        np.save(self.filename.get()+".npy",self.board,'x')
        messagebox.showinfo("Notion","save completed")
        self.newWindow.destroy()
    def BTload(self):
        self.newWindow=Toplevel(self.window)
        self.newWindow.title("file load")
        self.newWindow.geometry("350x250")
        self.newWindow.resizable(False,False)
        Label(self.newWindow,text="filename").place(x=30,y=50)
        self.filename=Entry(self.newWindow,width=20)
        self.filename.place(x=100,y=50)
        Button(self.newWindow,text="Ok",command=self.fileload).place(x=30,y=130)
    def fileload(self):
        self.board=np.load(self.filename.get()+".npy")
        messagebox.showinfo("Notion","load completed")
        self.newWindow.destroy()
        self.canvas.delete("all")
        self.canvas.create_image(1093,451,image=self.photo)
        self.initialize_board()
        
    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------   
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

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
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

    #to make number 3 digit ex) 1 -> 001, 13 -> 013
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
                self.drawRec(logical_position)
            else:
                self.deleteRec(logical_position)
    


game_instance=AStarPathFinding()
game_instance=mainloop()