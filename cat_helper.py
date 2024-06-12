import asyncio
import random
import flet as ft
import time


#游戏设定等
rol = 10
col = 10
cshit = round(1*(rol+col))
buttons = []
#标记的猫屎的数量
biaoji = cshit

biaoji_label = None
main_page = None
time_label = None
stgm = False


#引入全局page
def set_main_page(page):
    global main_page
    main_page = page

#引入猫屎计数器
def biaoji_label_function(label):
    global biaoji_label
    biaoji_label = label

#引入计时器
def time_label_function(label):
    global time_label
    time_label = label

#计时功能
before = time.time()
async def gtime():
    global game_time, main_page
    while True:
        await asyncio.sleep(1)
        update_time_label()

def update_time_label():
    game_time = round(time.time() - before)
    time_label.text = f"游戏时间：{game_time}"
    main_page.update()

def restart_game():
    global main_page,buttons, grid, player_grid, stgm, before

    #创建猫屎图
    grid = []
    for y in range(rol):
        grid_row = []
        for x in range(col):
            grid_row.append(0)
        grid.append(grid_row)
    #创建玩家图
    player_grid=[]
    for y in range(rol):
        player_grid_rol = []
        for x in range(col):
            player_grid_rol.append("*")
        player_grid.append(player_grid_rol)
    #分配猫屎
    i= cshit
    while i >0 :                  
        x = random.randint(0, col-1)
        y = random.randint(0, rol-1)
        if grid[x][y] == 1:
            continue
        grid[x][y] = 1
        i = i-1
    #重置计时器
    before = time.time()
    update_time_label()

    #重置按钮
    for y in range(rol):
        for x in range(col):
            buttons[y][x].text = ""
            buttons[y][x].style.bgcolor="#2E53C1"
            buttons[y][x].style.opacity = 0.5
            buttons[y][x].style.side = ft.border.BorderSide(color="#000000",width=1)
    main_page.update()
    stgm = False



#定义数猫屎函数
def count(x,y):
    global grid, rol, col
    n = 0
    for a in [x-1,x,x+1]:
        if a < 0 or a >= col:
            continue
        for b in [y-1,y,y+1]:
            if b < 0 or b >= rol:
                continue
            if grid[b][a] == 1:
                n = n+1

    return n   


#定义右键功能
def right_press(x, y):
    global stgm, player_grid, buttons, main_page, biaoji, biaoji_label
   
    if x < 0 or x >= col or y < 0 or y >= rol:
        return
    btn = buttons[y][x]
    if stgm == True:
        return

    if player_grid[y][x] != "*":
        if player_grid[y][x] == "$":
            return
        if player_grid[y][x] == "💩":
            btn.text = "?"
            player_grid[y][x]="?"
        else:
            btn.text = " "
            player_grid[y][x]="*"
            biaoji = biaoji + 1
    else:
        btn.text = "💩"
        player_grid[y][x]="💩"
        biaoji = biaoji - 1
    biaoji_label.text = f"剩余猫屎数量：{biaoji}"
    main_page.update()



#定义点击功能 
def click (x, y):
    global stgm, player_grid, buttons, main_page, grid
    if stgm == True:
        return

    #判断点击的格子是否超出棋盘边界
    if x < 0 or x >= col or y < 0 or y >= rol:
        return
    btn = buttons[y][x]
    #判断是否已经点击过或标记过
    if player_grid[y][x] != "*":
        return
    #判断是否踩到猫屎
    if grid[y][x] == 1:
        btn.style.bgcolor="#FB0000"
        print("You stepped on shit")
        stgm = True
    
    else:
        c = count(x,y)
        #表示点击过且没有雷
        if c == 0:
            player_grid[y][x] = "$"
            btn.text=" "
            btn.style.bgcolor="#668AF4"

        #展示周围雷的数量
        else:
            player_grid[y][x] = "$"
            btn.text=f"{c}"
            btn.style.bgcolor="#668AF4"

        #点击过，没有雷，继续开周围的格子
        if c == 0:
            click(x,y-1)
            click(x,y+1)
            click(x+1,y-1)
            click(x+1,y)
            click(x+1,y+1)
            click(x-1,y-1)
            click(x-1,y)
            click(x-1,y+1)

    main_page.update()

#定义提醒点击功能
def tip_function (x,y):
    global stgm, player_grid, buttons, main_page,c
   #刨除边界外
    if x < 0 or x >= col or y < 0 or y >= rol:
        return
    btn = buttons[y][x]
    if stgm == True:
        return
    if player_grid[y][x] == "?" or player_grid[y][x] =="💩" or btn.text == " " :
        return
    
    shit_number=0
    if player_grid[y][x] == "$":
        for a in (x-1,x,x+1):
            for b in (y-1,y,y+1):
                if a < 0 or a >= col or b < 0 or b >= rol:
                    continue
                if player_grid[b][a] == "💩":
                    shit_number = shit_number+1
        for a in (x-1,x,x+1):
            for b in (y-1,y,y+1):
                if a < 0 or a >= col or b < 0 or b >= rol:
                    continue
                if shit_number == int(buttons[y][x].text):
                    click(a,b)

                if player_grid[b][a] == "*":
                    buttons[b][a].style.bgcolor="#FFB045"
                
                
        main_page.update()
        time.sleep(0.2)
        for a in (x-1,x,x+1):
            for b in (y-1,y,y+1):
                if a < 0 or a >= col or b < 0 or b >= rol:
                    continue
                if player_grid[b][a] == "*":
                    buttons[b][a].style.bgcolor="#2E53C1"
        main_page.update()

    main_page.update()

#检测游戏是否结束
def check_end():
    for y in range(rol):
        for x in range(col):
            if grid[y][x] != 1:
                if player_grid[y][x] == "*" or player_grid[y][x] == "💩":
                    return False
    return True


#是否满足胜利条件
def victory():
    if check_end()== False:
        return
    print("You found all catshits!")



    
            


    main_page.update()