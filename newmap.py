from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
from matplotlib.pyplot import grid
import numpy as np
# Define useful parameters
imagewidth = 2200
width = 2300
height = 902
horizontalStepCount = 100
verticalStepCount = height//(imagewidth//horizontalStepCount)
length = imagewidth//horizontalStepCount
Color = {0: "none", 1: "grey", 2: "green", 3: "red"}  # 열린목록 닫힌목록 길 등은 나중에 추가


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def heuristic(node, goal, D=1, D2=2 ** 0.5):  # Diagonal Distance
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


def aStar(maze, start, end):
    print('start end', start, end)
    # startNode와 endNode 초기화
    startNode = Node(None, start)
    endNode = Node(None, end)
    print('Nodes', startNode, endNode)

    # openList, closedList 초기화
    openList = []
    closedList = []

    # openList에 시작 노드 추가
    openList.append(startNode)
    print('init openList', openList)

    # endNode를 찾을 때까지 실행
    while openList:
        print(
            '============================================================================')
        print('openList', openList)
        # 현재 노드 지정
        currentNode = openList[0]
        currentIdx = 0

        # 이미 같은 노드가 openList에 있고, f 값이 더 크면
        # currentNode를 openList안에 있는 값으로 교체
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIdx = index
        #print('currentNode', currentNode)
        #print('currentIdx', currentIdx)
        print('currentNode', currentNode)
        print('currentNode.position', currentNode.position)
        # openList에서 제거하고 closedList에 추가
        openList.pop(currentIdx)
        closedList.append(currentNode)
        #print('closedList', closedList)
        #print('currentNode.position', currentNode.position)
        # 현재 노드가 목적지면 current.position 추가하고
        # current의 부모로 이동
        if currentNode.position == endNode.position:
            path = []
            current = currentNode
            while current is not None:
                # maze 길을 표시하려면 주석 해제
                # x, y = current.position
                # maze[x][y] = 7
                path.append(current.position)
                current = current.parent
            print('!!!!!!!!!!!!!!!!!!!!!!!!!path!!!!!!!!!!!!!!!!!!!!!!!!!', path)
            return path[::-1]  # reverse

        children = []
        # 인접한 xy좌표 전부
        for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            # 노드 위치 업데이트
            nodePosition = (
                currentNode.position[0] + newPosition[0],  # X
                currentNode.position[1] + newPosition[1])  # Y

            # 미로 maze index 범위 안에 있어야함
            within_range_criteria = [
                nodePosition[0] > (len(maze) - 1),
                nodePosition[0] < 0,
                nodePosition[1] > (len(maze[len(maze) - 1]) - 1),
                nodePosition[1] < 0,
            ]

            if any(within_range_criteria):  # 하나라도 true면 범위 밖임
                continue

            # 장애물이 있으면 다른 위치 불러오기
            if maze[nodePosition[0]][nodePosition[1]] == 1:
                continue

            new_node = Node(currentNode, nodePosition)
            #print('child new', new_node)
            children.append(new_node)

        # 자식들 모두 loop
        for child in children:

            # 자식이 closedList에 있으면 continue
            if child in closedList:
                continue

            # if child in openList:
            #     continue

            # f, g, h값 업데이트
            child.g = currentNode.g + 1
            child.h = ((child.position[0] - endNode.position[0]) **
                       2) + ((child.position[1] - endNode.position[1]) ** 2)
            # child.h = heuristic(child, endNode) 다른 휴리스틱
            # print("position:", child.position) 거리 추정 값 보기
            # print("from child to goal:", child.h)

            child.f = child.g + child.h
            #print('child', child.position, child.f)

            # 자식이 openList에 있으고, g값이 더 크면 continue
            if len([openNode for openNode in openList
                    if child == openNode and child.g > openNode.g]) > 0:
                continue

            openList.append(child)


class AStarPathFinding:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("AStarPathFinding")
        imgpath = "campusCapture.png"
        img = Image.open(imgpath)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas = Canvas(self.window, width=width, height=height)
        self.canvas.pack()
        self.reset()
        self.window.bind("<Button-1>", self.click)
        Button(self.window, text="none", font=36, fg="black",
               command=self.BTnone).place(x=2220, y=50)
        Button(self.window, text="wall", font=36, fg="black",
               command=self.BTwall).place(x=2220, y=150)
        Button(self.window, text="start", font=36, fg="black",
               command=self.BTstart).place(x=2220, y=250)
        Button(self.window, text="goal", font=36, fg="black",
               command=self.BTgoal).place(x=2220, y=350)
        Button(self.window, text="astar", font=36, fg="black",
               command=self.BTastar).place(x=2220, y=450)
        Button(self.window, text="reset", font=36, fg="black",
               command=self.reset).place(x=2220, y=550)
        Button(self.window, text="save", font=36, fg="black",
               command=self.BTsave).place(x=2220, y=650)
        Button(self.window, text="load", font=36, fg="black",
               command=self.BTload).place(x=2220, y=750)

    # initialize the board matrix to 0
    def boardZero(self):
        self.board = []
        for i in range(verticalStepCount):
            for j in range(horizontalStepCount):
                self.board = np.zeros(
                    shape=(verticalStepCount, horizontalStepCount))  # fixed

    # fill board regard to matrix and create line
    def initialize_board(self):
        for i in range(verticalStepCount):
            for j in range(horizontalStepCount):
                tagname = "rect"+self.convertRecNum(j)+self.convertRecNum(i)
                if(self.board[i][j] == 0):  # none #fixed
                    self.canvas.create_rectangle(
                        j*length, i*length, (j+1)*length, (i+1)*length, tag=tagname)
                elif(self.board[i][j] == 1):  # wall #fixed
                    self.canvas.create_rectangle(
                        j*length, i*length, (j+1)*length, (i+1)*length, tag=tagname, fill="grey")
                elif(self.board[i][j] == 2):  # start #fixed
                    self.canvas.create_rectangle(
                        j*length, i*length, (j+1)*length, (i+1)*length, tag=tagname, fill="green")
                elif(self.board[i][j] == 3):  # goal #fixed
                    self.canvas.create_rectangle(
                        j*length, i*length, (j+1)*length, (i+1)*length, tag=tagname, fill="red")

        for i in range(horizontalStepCount+1):  # horizontal line
            self.canvas.create_line(
                imagewidth/horizontalStepCount*i, 0, imagewidth/horizontalStepCount*i, height,
            )

        for i in range(verticalStepCount+1):  # vertical line
            self.canvas.create_line(
                0, i * height / verticalStepCount, imagewidth, i * height / verticalStepCount,
            )

    # reset board
    def reset(self):
        self.boardZero()
        self.canvas.create_image(1093, 451, image=self.photo)
        self.initialize_board()
        self.modenumber = 0
        self.startcount = 0
        self.goalcount = 0

    def mainloop(self):
        self.window.mainloop()

    # ---------------------------------------------------------
    # Button Command function
    # ---------------------------------------------------------
    def BTnone(self):
        self.modenumber = 0
        print(self.board)

    def BTwall(self):
        self.modenumber = 1
        self.initialize_board()

    def BTstart(self):
        self.modenumber = 2

    def BTgoal(self):
        self.modenumber = 3

    # def aStar(self):
    #     class Node:
    #         def __init__(self, parent=None, position=None):
    #             self.parent = parent
    #             self.position = position

    #             self.g = 0
    #             self.h = 0
    #             self.f = 0

    #         def __eq__(self, other):
    #             return self.position == other.position
    #     maze = self.board
    #     print('=======maze=======\n', maze)
    #     start = (np.where(self.board == 2)[0].tolist()[0],
    #              np.where(self.board == 2)[1].tolist()[0])
    #     end = (np.where(self.board == 3)[0].tolist()[0],
    #            np.where(self.board == 3)[1].tolist()[0])
    #     print('start end', start, end)
    #     # startNode와 endNode 초기화
    #     startNode = Node(None, start)
    #     endNode = Node(None, end)
    #     print('Nodes', startNode, endNode)

    #     # openList, closedList 초기화
    #     openList = []
    #     closedList = []

    #     # openList에 시작 노드 추가
    #     openList.append(startNode)
    #     print('init openList', openList)

    #     # endNode를 찾을 때까지 실행
    #     while openList:
    #         print(
    #             '============================================================================')
    #         #print('openList', openList)
    #         # 현재 노드 지정
    #         currentNode = openList[0]
    #         currentIdx = 0

    #         # 이미 같은 노드가 openList에 있고, f 값이 더 크면
    #         # currentNode를 openList안에 있는 값으로 교체
    #         for index, item in enumerate(openList):
    #             if item.f < currentNode.f:
    #                 currentNode = item
    #                 currentIdx = index
    #         # openList에서 제거하고 closedList에 추가
    #         openList.pop(currentIdx)
    #         closedList.append(currentNode)
    #         #print('closedList', closedList)
    #         print('currentNode', currentNode)
    #         print('currentNode.position', currentNode.position)
    #         self.canvas.create_rectangle(
    #             (currentNode.position[1])*length, (currentNode.position[0])*length, (currentNode.position[1]+1)*length, (currentNode.position[0]+1)*length, tag="sth", fill="yellow")
    #         # 보드에 createRec (초록색)

    #         # 현재 노드가 목적지면 current.position 추가하고
    #         # current의 부모로 이동
    #         if currentNode == endNode:
    #             path = []
    #             print('!!!!!!!!!!!!!!!!!!!!!!!!!path!!!!!!!!!!!!!!!!!!!!!!!!!', path)
    #             current = currentNode
    #             while current is not None:
    #                 # maze 길을 표시하려면 주석 해제
    #                 # x, y = current.position
    #                 # maze[x][y] = 7
    #                 path.append(current.position)
    #                 current = current.parent
    #             return path[::-1]  # reverse

    #         children = []
    #         # 인접한 xy좌표 전부
    #         for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

    #             # 노드 위치 업데이트
    #             nodePosition = (
    #                 currentNode.position[0] + newPosition[0],  # X
    #                 currentNode.position[1] + newPosition[1])  # Y

    #             # 미로 maze index 범위 안에 있어야함
    #             within_range_criteria = [
    #                 nodePosition[0] > (len(maze) - 1),
    #                 nodePosition[0] < 0,
    #                 nodePosition[1] > (len(maze[len(maze) - 1]) - 1),
    #                 nodePosition[1] < 0,
    #             ]

    #             if any(within_range_criteria):  # 하나라도 true면 범위 밖임
    #                 continue

    #             # 장애물이 있으면 다른 위치 불러오기
    #             if maze[nodePosition[0]][nodePosition[1]] != 0:
    #                 continue

    #             new_node = Node(currentNode, nodePosition)
    #             #print('child new', new_node)
    #             children.append(new_node)

    #         # 자식들 모두 loop
    #         for child in children:
    #             # 자식이 closedList에 있으면 continue
    #             if child in closedList:
    #                 continue

    #             # f, g, h값 업데이트
    #             child.g = currentNode.g + 1
    #             child.h = ((child.position[0] - endNode.position[0]) **
    #                        2) + ((child.position[1] - endNode.position[1]) ** 2)
    #             # child.h = heuristic(child, endNode) 다른 휴리스틱
    #             # print("position:", child.position) 거리 추정 값 보기
    #             # print("from child to goal:", child.h)

    #             child.f = child.g + child.h
    #             #print('child', child.position, child.f)

    #             # 자식이 openList에 있으고, g값이 더 크면 continue
    #             if len([openNode for openNode in openList
    #                     if child == openNode and child.g > openNode.g]) > 0:
    #                 continue

    #             openList.append(child)
    #             self.drawRec(child.position)
    #             # self.canvas.create_rectangle(
    #             #     (child.position[1])*length, (child.position[0])*length, (child.position[1]+1)*length, (child.position[0]+1)*length, tag="sth", fill="blue")

    #     #print('closedList\n', closedList)

    def BTastar(self):
        start = (np.where(self.board == 2)[0].tolist()[0],
                 np.where(self.board == 2)[1].tolist()[0])
        end = (np.where(self.board == 3)[0].tolist()[0],
               np.where(self.board == 3)[1].tolist()[0])
        aStar(self.board.tolist(), start, end)

    def BTsave(self):
        self.newWindow = Toplevel(self.window)
        self.newWindow.title("file save")
        self.newWindow.geometry("350x250")
        self.newWindow.resizable(False, False)
        Label(self.newWindow, text="filename").place(x=30, y=50)
        self.filename = Entry(self.newWindow, width=20)
        self.filename.place(x=100, y=50)
        Button(self.newWindow, text="Ok",
               command=self.filesave).place(x=30, y=130)

    def filesave(self):
        np.save(self.filename.get()+".npy", self.board, 'x')
        messagebox.showinfo("Notion", "save completed")
        self.newWindow.destroy()

    def BTload(self):
        self.newWindow = Toplevel(self.window)
        self.newWindow.title("file load")
        self.newWindow.geometry("350x250")
        self.newWindow.resizable(False, False)
        Label(self.newWindow, text="filename").place(x=30, y=50)
        self.filename = Entry(self.newWindow, width=20)
        self.filename.place(x=100, y=50)
        Button(self.newWindow, text="Ok",
               command=self.fileload).place(x=30, y=130)

    def fileload(self):
        self.board = np.load(self.filename.get()+".npy")
        messagebox.showinfo("Notion", "load completed")
        self.newWindow.destroy()
        self.canvas.delete("all")
        self.canvas.create_image(1093, 451, image=self.photo)
        self.initialize_board()
        self.loadcount()

    def loadcount(self):
        startflag = np.any(self.board == 2)
        goalflag = np.any(self.board == 3)
        if startflag:
            self.startcount = 1
        else:
            self.startcount = 0
        if goalflag:
            self.goalcount = 1
        else:
            self.goalcount = 0
    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def drawRec(self, logical_position):
        logical_position = np.array(logical_position)
        x = int(logical_position[0])
        y = int(logical_position[1])
        tagname = "rect"+self.convertRecNum(x)+self.convertRecNum(y)
        if not self.modenumber == 0:
            self.canvas.create_rectangle(
                x*length, y*length, (x+1)*length, (y+1)*length, tag=tagname, fill=Color[self.modenumber])
            self.board[logical_position[1]][logical_position[0]
                                            ] = self.modenumber  # fixed

    def deleteRec(self, logical_position):
        if not self.modenumber == 0:
            x = int(logical_position[0])
            y = int(logical_position[1])
            tagname = "rect"+self.convertRecNum(x)+self.convertRecNum(y)
            self.canvas.delete(tagname)
            self.board[logical_position[1]][logical_position[0]] = 0  # fixed

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
        if self.board[logical_position[1]][logical_position[0]] == 0:  # fixed
            return False
        else:
            return True

    # to make number 3 digit ex) 1 -> 001, 13 -> 013
    def convertRecNum(self, num):
        if(num//100 != 0):
            return str(num)
        elif(num//10 != 0):
            return "0"+str(num)
        else:
            return "00"+str(num)

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        # 버튼 눌렀을 때 사각형이 클릭되었다고 인식하지않기 위해
        if logical_position[0] > 3 or logical_position[1] > 3:
            if not self.is_grid_occupied(logical_position):
                if self.modenumber == 2:
                    if self.startcount == 0:
                        self.drawRec(logical_position)
                        self.startcount += 1
                elif self.modenumber == 3:
                    if self.goalcount == 0:
                        self.drawRec(logical_position)
                        self.goalcount += 1
                else:
                    self.drawRec(logical_position)
            else:
                # fixed
                if self.modenumber == self.board[logical_position[1]][logical_position[0]]:
                    if self.modenumber == 2:
                        if self.startcount == 1:
                            self.deleteRec(logical_position)
                            self.startcount -= 1
                    elif self.modenumber == 3:
                        if self.goalcount == 1:
                            self.deleteRec(logical_position)
                            self.goalcount -= 1
                    else:
                        self.deleteRec(logical_position)


game_instance = AStarPathFinding()
game_instance = mainloop()
