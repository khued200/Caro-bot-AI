from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox 
from Constants import *
from GameState import *
from Bot import *

# Widget root cho giao diện
parent = Tk()
parent.title('Tic tac toe')

# Frame chứa Entry lấy giá trị của cột
frCot = Frame(parent)
frCot.pack(pady = 5)
nCol = Label(frCot, text = "Nhập số cột:", width=15).grid(row = 0, column = 0)
e2 = Entry(frCot)
e2.insert(END, '10')
e2.grid(row = 0, column = 1)

# Frame chứa Entry lấy giá trị của hàng
frHang = Frame(parent)
frHang.pack()
nRow = Label(frHang, text = "Nhập số hàng:",width=15).grid(row = 0, column = 0)
e1 = Entry(frHang)
e1.insert(END, '10')
e1.focus()
e1.grid(row = 0, column = 1)

# Label tạo khoảng trống làm đẹp giao diện XD
clone_Label = Label(frCot, text = "", width=28)
clone_Label.grid(row = 0, column = 2)

# Combobox chọn chơi X hay O
cbb_X_O = Combobox(frCot)
cbb_X_O['values'] = ('Đánh X', 'Đánh O')
cbb_X_O.set('Đánh X')

# Hàm khi bấm núi chơi  
def btnPlay():
    turnWho.focus()
    # roW và coL lần lượt là hàng và cột của bàn cờ
    try:
        roW = int(e1.get())
        coL = int(e2.get())
    except:
        messagebox.showwarning('Show Warning', 'Vui lòng nhập đúng giá trị hàng và cột!')
        return
        
    if roW < 5 or coL < 5:
        messagebox.showwarning('Show Warning', 'Kích thước bảng quá bé, vui lòng nhập lại!')
        return
    
    if roW > 20 or coL > 40:
        messagebox.showwarning('Show Warning', 'Kích thước bảng quá to, vui lòng nhập lại!')
        return
    desChild()
    typeG[0] = cbb_Type_Play.get()
    if typeG[0] == 'Chơi với máy':
        choose_X_O[0] = cbb_X_O.get()
    # Khởi tạo toàn bộ giá trị ban đầu của trò chơi, bao gồm có:
    ## Số hàng, cột, tổng lượt đánh, lượt đánh tối đa, bàn cờ, store_ của máy và người
    numPlay[0] = -1
    rowT[0] = roW
    colT[0] = coL
    maxNumPlay[0] = roW * coL - 1
    play.config(text = 'Làm mới bàn cờ')
    print("restart")
    for i in range(roW):
        for j in range(coL):
            chessTable[i][j] = ' '
            checkChess[i][j] = False
    for i in range(roW * coL):
        store_Human[i] = [-1, -1]
        store_Comp[i] = [-1, -1]
    turnWho.config(text = 'Tới lượt của x', font=('Arial, 15'))
    if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh X':
        turnWho.config(text = 'Tới lượt của bạn')
    # Xây dựng giao diện trò chơi bằng mảng 2 chiều gồm roW * coL Button 
    buttons = [[Button(fr,font=('Arial', 15), width=5, height=2) for i in range(coL)] for i in range(roW)]
    for b in range(roW):
        for a in range(coL):
            buttons[b][a].config(bg = 'white', activebackground = 'white',width = 3, height = 1)
            buttons[b][a].bind("<Enter>", on_enter)
            buttons[b][a].bind("<Leave>", on_leave)
            buttons[b][a].config(command= lambda btn =  buttons[b][a], x = b, y = a: clicked(btn, x, y))
            buttons[b][a].grid( row = b, column = a)
    # Nếu chơi với máy lấy tọa độ ngẫu nhiên rồi đánh vào bàn cờ
    if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh O':
        COMP[0] = 'x'
        HUMAN[0] = 'o'
        x, y = get_random_middle_point()
        buttons = fr.winfo_children()
        btn = buttons[x * colT[0] + y]
        clicked(btn, x, y)

# Nút bắt đầu trò chơi
fr_Play_And_Depth = Frame(parent)
fr_Play_And_Depth.pack()
play = Button(fr_Play_And_Depth, text = "Bắt đầu chơi", command = btnPlay)
play.grid(row = 0, column = 0, padx = 30)
clone_Label1 = Label(fr_Play_And_Depth, text = "")
clone_Label1.grid(row = 0, column = 1, padx = 117)


# Hàm xuất hiện chọn đánh X hay O khi chơi với máy
def choose_Type(e):
    typeGame = e.widget.get()
    try:
        if typeGame == 'Chơi với máy':
            clone_Label.grid_forget()
            clone_Label1.grid_forget()
            clone_Label_Depth_X.grid_forget()
            clone_Label_Depth_O.grid_forget()
            cbb_Depth_X.grid_forget()
            cbb_Depth_O.grid_forget()
            cbb_X_O.grid(row = 0, column = 3 , padx = 30)
            clone_Label_Depth.grid(row = 0, column = 1, padx = 2)
            cbb_Depth.grid(row = 0, column = 2)
        elif typeGame == 'Máy đánh máy':
            clone_Label1.grid_forget()
            clone_Label_Depth.grid_forget()
            clone_Label_Depth_X.grid(row = 0, column = 1, padx = 2)
            cbb_Depth_X.grid(row = 0, column = 2)

            clone_Label_Depth_O.grid(row = 1, column = 1, padx = 2)
            cbb_Depth_O.grid(row = 1, column = 2)
        else:
            cbb_X_O.grid_forget()
            clone_Label_Depth.grid_forget()
            cbb_Depth.grid_forget()
            clone_Label.grid(row = 0, column = 2)
            clone_Label1.grid(row = 0, column = 1, padx = 117)
    except:
        pass

# Hàm xử lý độ khó trò chơi
def choose_Level(e):
    level_Game = e.widget.get()
    if level_Game == 'Dễ':
        depth[0] = 1
    elif level_Game == 'Trung bình':
        depth[0] = 2
    else:
        depth[0] = 3
def choose_Level_X(e):
    level_Game = e.widget.get()
    if level_Game == 'Dễ':
        depthX[0] = 1
    elif level_Game == 'Trung bình':
        depthX[0] = 2
    else:
        depthX[0] = 3
def choose_Level_O(e):
    level_Game = e.widget.get()
    if level_Game == 'Dễ':
        depthO[0] = 1
    elif level_Game == 'Trung bình':
        depthO[0] = 2
    else:
        depthO[0] = 3
# Hàm khi nhấn vào button giao diện trò chơi
def clicked(btn, x, y):
    if x == -1 or y == -1:
        return
    if checkChess[x][y]:
        return
    buttons = fr.winfo_children()
    if btn_Clicked[0] == -1:
        btn_Clicked[0] = x
        btn_Clicked[1] = y
    else:
        buttons[btn_Clicked[0] * colT[0] + btn_Clicked[1]].config(bg = 'white')
        btn_Clicked[0] = x
        btn_Clicked[1] = y
    # Đánh dấu vị trí bàn cờ trên giao diện đã được chọn
    checkChess[x][y] = True
    # Cập nhật các giá trị
    # Bổ sung nước đi vừa đánh vào store_ của player tương ứng
    numPlay[0] += 1
    if numPlay[0] % 2 == 0:
        if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh O':
            store_Comp[numPlay[0]//2] = [x, y]
        if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh X':
            store_Human[numPlay[0]//2] = [x, y]
        # Một số hàm xử lý giao diện của bàn cờ khi được nhấn vào
        btn.unbind("<Leave>")
        btn.unbind("<Enter>")
        chessTable[x][y] = 'x'
        btn.config(text = 'X',font=('Arial',15), bg = '#FFEFD5', fg = 'red')

        # Kiểm tra điều kiện thắng của X
        checkE, typeWin, sT, eN = checkEnd('x', x, y)
        if checkE:
            sT = int(sT)
            eN = int(eN)

            if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh O':
                turnWho.config(text='Máy giành chiến thắng!')
            elif typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh X':
                turnWho.config(text='Người giành chiến thắng!')
            else:
                turnWho.config(text='X giành chiến thắng!')

            play.config(text = 'Chơi lại')
            buttons = fr.winfo_children()

            # Tô màu đánh dấu chiến thắng cho X
            buttons[x * colT[0] + y].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
            if typeWin == 'row':
                for i in range(sT):
                    buttons[x * colT[0] + y + i + 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
                for i in range(eN):
                    buttons[x * colT[0] + y - i - 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
            elif typeWin == 'col':
                for i in range(sT):
                    buttons[(x + i + 1) * colT[0] + y].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
                for i in range(eN):
                    buttons[(x - i - 1) * colT[0] + y].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
            elif typeWin == 'c1':
                for i in range(sT):
                    buttons[(x + i + 1) * colT[0] + y + i + 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
                for i in range(eN):
                    buttons[(x - i - 1) * colT[0] + y - i - 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
            else:
                for i in range(sT):
                    buttons[(x + i + 1) * colT[0] + y - i - 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
                for i in range(eN):
                    buttons[(x - i - 1) * colT[0] + y + i + 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')

            # Vô hiệu hóa các nút còn lại khi kết thúc trò chơi
            for i in range(rowT[0]):
                for j in range(colT[0]):
                    checkChess[i][j] = True
            for btnChild in buttons:
                try:
                    btnChild.unbind("<Leave>")
                    btnChild.unbind("<Enter>")
                except:
                    pass
            return

        # Nếu bàn cờ hết chỗ đánh thì thông báo hòa
        if numPlay[0] == maxNumPlay[0]:
            turnWho.config(text='Hòa!')
            return
        # Tính toán tới lượt đánh của ai
        if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh O':
            turnWho.config(text = 'Tới lượt của bạn', font=('Arial, 15'))

        elif typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh X':
            turnWho.config(text = 'Tới lượt của máy', font=('Arial, 15'))
            x, y = AI_smartMove(chessTable)
            buttons = fr.winfo_children()
            btn = buttons[x * colT[0] + y]
            clicked(btn, x, y)
        elif typeG[0] == 'Máy đánh máy':
            x, y = AI_smartMove_O(chessTable)
            if(x == -1 and y == -1): x, y = get_random_remain_point(chessTable)
            buttons = fr.winfo_children()
            btn = buttons[x * colT[0] + y]
            clicked(btn, x, y)

            x, y = AI_smartMove_X(chessTable)
            if(x == -1 and y == -1): x, y = get_random_remain_point(chessTable)
            buttons = fr.winfo_children()
            btn = buttons[x * colT[0] + y]
            clicked(btn, x, y)
        else:
            turnWho.config(text = 'Tới lượt của o', font=('Arial, 15'))

    # Cũng tương tự như trên   
    else:
        if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh X':
            store_Comp[numPlay[0]//2] = [x, y]
        if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh O':
            store_Human[numPlay[0]//2] = [x, y]

        btn.unbind("<Leave>")
        btn.unbind("<Enter>")
        chessTable[x][y] = 'o'
        btn.config(text = 'O',font=('Arial',15), bg = '#FFEFD5', fg = 'blue')

        # Kiểm tra điều kiện thắng của O
        checkE, typeWin, sT, eN = checkEnd('o', x, y)
        if checkE:
            sT = int(sT)
            eN = int(eN)
            
            if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh O':
                turnWho.config(text='Người giành chiến thắng!')
            elif typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh X':
                turnWho.config(text='Máy giành chiến thắng!')
            else:
                turnWho.config(text='O giành chiến thắng!')

            play.config(text = 'Chơi lại')
            buttons = fr.winfo_children()

            # Tô màu đánh dấu chiến thắng cho O
            buttons[x * colT[0] + y].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
            if typeWin == 'row':               
                for i in range(sT):
                    buttons[x * colT[0] + y + i + 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
                for i in range(eN):
                    buttons[x * colT[0] + y - i - 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
            elif typeWin == 'col':
                for i in range(sT):
                    buttons[(x + i + 1) * colT[0] + y].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
                for i in range(eN):
                    buttons[(x - i - 1) * colT[0] + y].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
            elif typeWin == 'c1':
                for i in range(sT):
                    buttons[(x + i + 1) * colT[0] + y + i + 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
                for i in range(eN):
                    buttons[(x - i - 1) * colT[0] + y - i - 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
            else:
                for i in range(sT):
                    buttons[(x + i + 1) * colT[0] + y - i - 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')
                for i in range(eN):
                    buttons[(x - i - 1) * colT[0] + y + i + 1].config(fg = 'white', bg = 'green', activebackground = 'green', activeforeground = 'white')

            # Vô hiệu hóa các button còn lại khi kết thúc trò chơi
            for i in range(rowT[0]):
                for j in range(colT[0]):
                    checkChess[i][j] = True
            for btnChild in buttons:
                try:
                    btnChild.unbind("<Leave>")
                    btnChild.unbind("<Enter>")
                except:
                    pass
            return
            
        if numPlay[0] == maxNumPlay[0]:
            turnWho.config(text='Hòa!')
            return
        if typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh O':
            turnWho.config(text = 'Tới lượt của máy', font=('Arial, 15'))
            x, y = AI_smartMove(chessTable)
            buttons = fr.winfo_children()
            btn = buttons[x * colT[0] + y]
            clicked(btn, x, y)
        elif typeG[0] == 'Chơi với máy' and choose_X_O[0] == 'Đánh X':
            turnWho.config(text = 'Tới lượt của bạn', font=('Arial, 15'))
        else:
            turnWho.config(text = 'Tới lượt của x', font=('Arial, 15'))
    
# Hàm hover button
def on_enter(e):
    e.widget.config(bg='#99FFFF',fg = '#99FFFF')

#Hàm leave button
def on_leave(e):
    e.widget.config(bg='white', fg = 'white')

# Hàm xóa hết giao diện bàn cờ khi ấn núi chơi 
def desChild():
    for widget in fr.winfo_children():
        widget.destroy()

# Combobox chọn chế đệ chơi
cbb_Type_Play = Combobox(frHang)
cbb_Type_Play['values'] = ('Chơi với người', 'Chơi với máy', 'Máy đánh máy')
cbb_Type_Play.grid(row = 0, column = 2, padx = 30)
cbb_Type_Play.set('Chơi với người')
cbb_Type_Play.bind('<<ComboboxSelected>>', choose_Type)

# Chọn độ sâu của trò chơi (PVB)
clone_Label_Depth = Label(fr_Play_And_Depth, text = "Độ khó trò chơi: ")
cbb_Depth = Combobox(fr_Play_And_Depth)
cbb_Depth['values'] = ('Dễ', 'Trung bình', 'Khó')
cbb_Depth.set('Dễ')
cbb_Depth.bind('<<ComboboxSelected>>', choose_Level)

# Chọn độ sâu của trò chơi (BVB)
clone_Label_Depth_X = Label(fr_Play_And_Depth, text = "Độ khó X: ")
cbb_Depth_X = Combobox(fr_Play_And_Depth)
cbb_Depth_X['values'] = ('Dễ', 'Trung bình', 'Khó')
cbb_Depth_X.set('Dễ')
cbb_Depth_X.bind('<<ComboboxSelected>>', choose_Level_X)

clone_Label_Depth_O = Label(fr_Play_And_Depth, text = "Độ khó O: ")
cbb_Depth_O = Combobox(fr_Play_And_Depth)
cbb_Depth_O['values'] = ('Dễ', 'Trung bình', 'Khó')
cbb_Depth_O.set('Dễ')
cbb_Depth_O.bind('<<ComboboxSelected>>', choose_Level_O)
# Label cho biết lượt của ai
turnWho = Label(parent)
turnWho.pack()

# Frame chứa giao diện chính của trò chơi
fr = Frame(parent, padx = 20, pady = 20)
fr.pack()
