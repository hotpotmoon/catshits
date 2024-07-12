import asyncio
import random
import flet as ft
import time

class CatHelper:
    def __init__(self):
        #游戏设定等
        self.rol = 10
        self.col = 10
        self.cshit = round(1*(self.rol+self.col))
        self.buttons = []
        #标记的猫屎的数量
        self.biaoji = self.cshit

        self.biaoji_label = None
        self.main_page = None
        self.time_label = None
        self.stgm = False
        self.game_time = 0


    #引入全局page
    def set_main_page(self, page):
        self.main_page = page

    #引入猫屎计数器
    def biaoji_label_function(self, label):
        self.biaoji_label = label

    #引入计时器
    def time_label_function(self, label):
        self.time_label = label

    #计时功能
    before = time.time()
    async def gtime(self):
        while True:
            await asyncio.sleep(1)
            if self.stgm == True:
                continue
            self.update_time_label()

    def update_time_label(self):
        self.game_time = round(time.time() - self.before)
        self.time_label.text = f"游戏时间：{self.game_time}"
        self.main_page.update()

    def restart_game(self):
        #创建猫屎图
        self.grid = []
        for y in range(self.rol):
            grid_row = []
            for x in range(self.col):
                grid_row.append(0)
            self.grid.append(grid_row)
        #创建玩家图
        self.player_grid=[]
        for y in range(self.rol):
            player_grid_rol = []
            for x in range(self.col):
                player_grid_rol.append("*")
            self.player_grid.append(player_grid_rol)
        #分配猫屎
        i= self.cshit
        while i >0 :                  
            x = random.randint(0, self.col-1)
            y = random.randint(0, self.rol-1)
            if self.grid[x][y] == 1:
                continue
            self.grid[x][y] = 1
            i = i-1
        #重置计时器
        self.before = time.time()
        self.update_time_label()

        #重置按钮
        for y in range(self.rol):
            for x in range(self.col):
                self.buttons[y][x].text = ""
                self.buttons[y][x].style.bgcolor="#2E53C1"
                self.buttons[y][x].style.opacity = 0.5
                self.buttons[y][x].style.side = ft.border.BorderSide(color="#000000",width=1)
        self.main_page.update()
        self.stgm = False

        #重置猫屎数量
        self.biaoji = self.cshit
        self.update_biaoji_label()



    #定义数猫屎函数
    def count(self, x,y):
        n = 0
        for a in [x-1,x,x+1]:
            if a < 0 or a >= self.col:
                continue
            for b in [y-1,y,y+1]:
                if b < 0 or b >= self.rol:
                    continue
                if self.grid[b][a] == 1:
                    n = n+1

        return n   

    #更新猫屎数量展示
    def update_biaoji_label(self):
        self.biaoji_label.text = f"剩余猫屎数量：{self.biaoji}"
        self.main_page.update()

    #定义右键功能
    def right_press(self, x, y):    
        if x < 0 or x >= self.col or y < 0 or y >= self.rol:
            return
        btn = self.buttons[y][x]
        if self.stgm == True:
            return

        if self.player_grid[y][x] != "*":
            if self.player_grid[y][x] == "$":
                return
            if self.player_grid[y][x] == "💩":
                btn.text = "?"
                self.player_grid[y][x]="?"
            else:
                btn.text = " "
                self.player_grid[y][x]="*"
                self.biaoji = self.biaoji + 1
        else:
            btn.text = "💩"
            self.player_grid[y][x]="💩"
            self.biaoji = self.biaoji - 1
        self.update_biaoji_label()


    #定义点击功能 
    def click (self, x, y):
        if self.stgm == True:
            return

        #判断点击的格子是否超出棋盘边界
        if x < 0 or x >= self.col or y < 0 or y >= self.rol:
            return
        btn = self.buttons[y][x]
        #判断是否已经点击过或标记过
        if self.player_grid[y][x] != "*":
            return
        #判断是否踩到猫屎
        if self.grid[y][x] == 1:
            btn.style.bgcolor="#FB0000"
            print("You stepped on shit")
            self.stgm = True
        
        else:
            c = self.count(x,y)
            #表示点击过且没有雷
            if c == 0:
                self.player_grid[y][x] = "$"
                btn.text=" "
                btn.style.bgcolor="#668AF4"

            #展示周围雷的数量
            else:
                self.player_grid[y][x] = "$"
                btn.text=f"{c}"
                btn.style.bgcolor="#668AF4"

            #点击过，没有雷，继续开周围的格子
            if c == 0:
                self.click(x,y-1)
                self.click(x,y+1)
                self.click(x+1,y-1)
                self.click(x+1,y)
                self.click(x+1,y+1)
                self.click(x-1,y-1)
                self.click(x-1,y)
                self.click(x-1,y+1)

        self.main_page.update()

    #定义提醒点击功能
    def tip_function (self, x,y):
    #刨除边界外
        if x < 0 or x >= self.col or y < 0 or y >= self.rol:
            return
        btn = self.buttons[y][x]
        if self.stgm == True:
            return
        if self.player_grid[y][x] == "?" or self.player_grid[y][x] =="💩" or btn.text == " " :
            return
        
        shit_number=0
        if self.player_grid[y][x] == "$":
            for a in (x-1,x,x+1):
                for b in (y-1,y,y+1):
                    if a < 0 or a >= self.col or b < 0 or b >= self.rol:
                        continue
                    if self.player_grid[b][a] == "💩":
                        shit_number = shit_number+1
            for a in (x-1,x,x+1):
                for b in (y-1,y,y+1):
                    if a < 0 or a >= self.col or b < 0 or b >= self.rol:
                        continue
                    if shit_number == int(self.buttons[y][x].text):
                        self.click(a,b)

                    if self.player_grid[b][a] == "*":
                        self.buttons[b][a].style.bgcolor="#FFB045"
                    
                    
            self.main_page.update()
            time.sleep(0.2)
            for a in (x-1,x,x+1):
                for b in (y-1,y,y+1):
                    if a < 0 or a >= self.col or b < 0 or b >= self.rol:
                        continue
                    if self.player_grid[b][a] == "*":
                        self.buttons[b][a].style.bgcolor="#2E53C1"
            self.main_page.update()

        self.main_page.update()

    #检测游戏是否结束
    def check_end(self):
        for y in range(self.rol):
            for x in range(self.col):
                if self.grid[y][x] != 1:
                    if self.player_grid[y][x] == "*" or self.player_grid[y][x] == "💩":
                        return False
        return True


    #是否满足胜利条件
    def victory(self):
        if self.check_end()== False:
            return
        print("You found all catshits!")
        self.main_page.update()