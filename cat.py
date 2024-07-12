import asyncio
import flet as ft
from cat_helper import CatHelper

cp = CatHelper()
#主页面参数
async def main(page: ft.Page):
    #设置主页面
    cp.set_main_page(page)
    page.title = "扫喵屎"
    page.bgcolor="#EEEEEE"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    page.spacing=0
    page.window_resizable= False
    page.window_height = 800
    page.window_width = 800
    page.update()



    #创建计时器 
    time_label = ft.ElevatedButton(text=f"游戏时间：{0}", disabled=True)
    cp.time_label_function(time_label)
    page.add(time_label)

    #展示剩余未标记的猫屎数量
    biaoji_label = ft.TextButton(text=f"剩余猫屎数量：{cp.biaoji}")
    cp.biaoji_label_function(biaoji_label)
    page.add(biaoji_label)

    #创建按钮
    for i in range(cp.rol):#行
        row=[]
        row_gd1=[]
        for j in range(cp.col):#每一行的列
            #创建按钮
            btn=ft.FilledButton(
                style=ft.ButtonStyle(
                    bgcolor="#2E53C1",
                    shape=ft.RoundedRectangleBorder(radius=0),
                    side=ft.border.BorderSide(color="#000000",width=1)
                ),
                opacity=0.5,
                height=40,
                width=40,
                on_long_press=lambda e, x = j, y = i: cp.tip_function(x, y),
                on_click=lambda e, x = j, y = i: cp.click(x, y)
            )
            #增加右键功能
            gd1 = ft.GestureDetector(
                on_secondary_tap_up=lambda e, x = j, y = i: cp.right_press(x, y),
                content=btn,
            )
            row.append(btn)#把每一列的按钮添加到行
            row_gd1.append(gd1)
       
        
        #设置行格式
        row_layout= ft.Row(controls=row_gd1,vertical_alignment=ft.CrossAxisAlignment.CENTER, 
            alignment=ft.MainAxisAlignment.CENTER,spacing=0)
        #储存每个按钮
        cp.buttons.append(row)
        #添加行
        page.add(row_layout)
    page.update()
    
    #重启按钮
    restart_btn = ft.FilledButton(
        text="重新开始",
        style=ft.ButtonStyle(
            bgcolor="#79BAEC",
            shape=ft.RoundedRectangleBorder(radius=0),
            side=ft.border.BorderSide(color="#151B54",width=1)
        ),
        on_click=lambda e: cp.restart_game(),
    )
    page.add(restart_btn)
    page.update()


    #创建协程更新计时器
    loop = asyncio.get_event_loop()
    loop.create_task(cp.gtime())

    #调用重启功能
    cp.restart_game()
    
ft.app(target=main)


  
