import math
from tkinter import *
from Constants import *
from GameState import *
from Evaluate import *

#Hàm tìm kiếm minimax trả về tọa độ tốt nhất {x,y} và evaluation 
def minimax(state, depth, player, alpha, beta, x, y):
    if player == COMP[0]:
        best = [-1 , -1, -math.inf]
    else:
        best = [-1, -1, math.inf]
    check = best[2]
    # Nếu độ sâu giảm tới 0 ( đoán trước tối đa depth nước đi ) hoặc bàn cờ đã hết cờ thì trả về giá trị của bàn cờ
    if depth == 0 or gameOver(player, x, y):
        sc = evaluate(player, x, y)
        return [-1, -1, sc]
    # numMark là biến đánh dấu vị trí để có thể lưu trữ nước đi cho player tại vị trí đầu tiên tìm thấy [-1, -1] trong store_
    numMark = 0
    if player == COMP[0]:
        while store_Comp[numMark] != [-1, -1]:
            numMark += 1
    else:
        while store_Human[numMark] != [-1, -1]:
            numMark += 1
    # Duyệt hết các nước có thể đi, danh sách các điểm có thể đi lấy được qua hàm get_remain_points(state)
    emptyB = get_remain_points(state)
    if len(emptyB) == 0:
        return [-1, -1, 0]
    for box in emptyB:
        xx, yy = box[0], box[1]
        # Bỏ qua nếu tọa độ đưa vào đủ " tệ "
        if checkBad_Point(xx, yy):
            continue
        # Nhét nước đi này vào kho chứa các nước đã đi của player để có thể đánh giá bàn cờ ở hàm evaluate(state, player, x, y)
        if player == COMP[0]:
            store_Comp[numMark] = [xx, yy]
        else:
            store_Human[numMark] = [xx, yy]
        # Đánh dấu vào bàn cờ nước vừa đi
        state[xx][yy] = player
        score = minimax(state, depth - 1, HUMAN[0] if player == COMP[0] else COMP[0], alpha, beta, xx, yy)
        # Bỏ đánh dấu bàn cờ trong quay lui
        state[xx][yy] = ' '
        # Xóa nước đi vừa rồi của player khỏi store_
        if player == COMP[0]:
            store_Comp[numMark] = [-1, -1]
        else:
            store_Human[numMark] = [-1, -1]
        score[0], score[1] = xx, yy

        # Cập nhật alpha và beta sau mỗi lần tìm kiếm trong 1 nhánh của minimax
        if player == COMP[0]:
            if score[2] > best[2]:
                best = score
            alpha = max(alpha, best[2])
        else:
            if score[2] < best[2]:
                best = score
            beta = min(beta, best[2])
        if beta <= alpha:
            break  # Cắt tỉa alpha - beta
    return best

# Hàm trả về nước đi tối ưu cho AI
def AI_smartMove(state):
    move = minimax(state, depth[0], COMP[0], -math.inf, math.inf, -1, -1)
    x, y = move[0], move[1]
    print(str(x) + " " + str(y) + " eval: "+ str(move[2]))
    return x, y
# Cũng như trên nhưng đối với bvb
def AI_smartMove_X(state):
    move = minimax(state, depthX[0], 'x', -math.inf, math.inf, -1, -1)
    x, y = move[0], move[1]
    print("Bot X đánh: "+str(x) + " " + str(y) + " eval: "+ str(-move[2]))
    return x, y

def AI_smartMove_O(state):
    move = minimax(state, depthO[0], 'o', -math.inf, math.inf, -1, -1)
    x, y = move[0], move[1]
    print("Bot O đánh: "+str(x) + " " + str(y) + " eval: "+ str(move[2]))
    return x, y
