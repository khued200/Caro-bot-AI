import random
from tkinter import *
from Constants import *

## turnXorO string chứa 'x' hoặc 'o' ( lượt tương ứng ), x, y là tọa độ của điểm vừa chọn
### Trả về 4 giá trị lần lượt là: 
    # - True / False : Kết thúc trò chơi hay không
    # - ['row', 'col', 'c1', 'c2']: Hướng của 5 x hoặc o liên tiếp. Tương đương 4 hướng [ -- , | , \ , /]
    # - d: Số phần tử đằng sau tọa độ vừa được chọn ( trong 5 x hoặc o liên tiếp )
    # - d1: Số phần tử đằng trước tọa độ vừa được chọn ( trong 5 x hoặc o liên tiếp )
    ## 3 giá trị cuối trả về nhằm mục tiêu bôi đỏ 5 x hoặc o liên tiếp
def checkEnd(turnXorO, x, y):
    roW = rowT[0]
    coL = colT[0]
    me = turnXorO #dấu của người chơi hiện tại
    opp = 'o' #dấu của đối thủ
    if me == 'o': opp = 'x'

    #KIỂM TRA ĐIỀU KIỆN 4 Ô LIÊN TIẾP KHÔNG BỊ CHẶN THẮNG

    # Kiểm tra hàng chứa 4 ô liên tiếp không bị chặn
    count = 1
    d = 1
    while y + d < coL and chessTable[x][y + d] == me:
        if count + d == 4:
            if (chessTable[x][y + d + 1] == " " and chessTable[x][y - 1] == " "):
                 return True, 'row', 3, 0
        d += 1
    d -= 1
    d1 = 1
    while y - d1 > -1 and chessTable[x][y - d1] == me:
        if count + d + d1 == 4:
            if (chessTable[x][y - d1 - 1] == " " and chessTable[x][y + d + 1] == " "):
                return True, 'row', d, d1
        d1 += 1

    # Kiểm tra cột chứa 4 ô liên tiếp không bị chặn
    count = 1
    d = 1
    while x + d < roW and chessTable[x + d][y] == me:
        if count + d == 4:
            if (chessTable[x + d + 1][y] == " " and chessTable[x -1][y] == " "):
                return True, 'col', 3, 0
        d += 1
    d -= 1
    d1 = 1
    while x - d1 > -1 and chessTable[x - d1][y] == me:
        if count + d + d1 == 4:
            if (chessTable[x - d1 - 1][y] == " " and chessTable[x + d + 1][y] == " "):
                return True, 'col', d, d1
        d1 += 1

    # Kiểm tra đường chéo C1 chứa 4 ô liên tiếp không bị chặn
    count = 1
    d = 1
    while x + d < roW and y + d < coL and chessTable[x + d][y + d] == me:
        if count + d == 4:
            if (chessTable[x + d + 1][y + d + 1] == " " and chessTable[x - 1][y - 1] == " "):
                return True, 'c1', 3, 0
        d += 1
    d -= 1
    d1 = 1
    while x - d1 > -1 and y - d1 > -1 and chessTable[x - d1][y - d1] == me:
        if count + d + d1 == 4:
            if (chessTable[x - d1 - 1][y - d1 - 1] == " " and chessTable[x + d + 1][y + d + 1] == " "):
                return True, 'c1', d, d1
        d1 += 1

    # Kiểm tra đường chéo C2 chứa 4 ô liên tiếp không bị chặn
    count = 1
    d = 1
    while x + d < roW and y - d > -1 and chessTable[x + d][y - d] == me:
        if count + d == 4:
            if (chessTable[x + d + 1][y - d - 1] == " " and chessTable[x - 1][y + 1] == " "):
                return True, 'c2', 3, 0
        d += 1
    d -= 1
    d1 = 1
    while x - d1 > -1 and y + d1 < coL and chessTable[x - d1][y + d1] == me:
        if count + d + d1 == 4:
            if (chessTable[x + d + 1][y - d - 1] == " " and chessTable[x - d1 -1][y + d1 + 1] == " "):
                return True, 'c2', d, d1
        d1 += 1

    #KIỂM TRA ĐIỀU KIỆN 5 Ô LIÊN TIẾP THẮNG

    # Kiểm tra hàng chứa 5 ô liên tiếp
    count = 1
    d = 1
    while y + d < coL and chessTable[x][y + d] == me:
        if count + d == 5:
            return True, 'row', 4, 0
        d += 1
    d -= 1
    d1 = 1
    while y - d1 > -1 and chessTable[x][y - d1] == me:
        if count + d + d1 == 5:
            return True, 'row', d, d1
        d1 += 1

    # Kiểm tra cột chứa 5 ô liên tiếp
    count = 1
    d = 1
    while x + d < roW and chessTable[x + d][y] == me:
        if count + d== 5:
            return True, 'col', 4, 0
        d += 1
    d -= 1
    d1 = 1
    while x - d1 > -1 and chessTable[x - d1][y] == me:
        if count + d + d1 == 5:
            return True, 'col', d, d1
        d1 += 1

    # Kiểm tra đường chéo C1 chứa 5 ô liên tiếp
    count = 1
    d = 1
    while x + d < roW and y + d < coL and chessTable[x + d][y + d] == me:
        if count + d == 5:
            return True, 'c1', 4, 0
        d += 1
    d -= 1
    d1 = 1
    while x - d1 > -1 and y - d1 > -1 and chessTable[x - d1][y - d1] == me:
        if count + d + d1 == 5:
            return True, 'c1', d, d1
        d1 += 1

    # Kiểm tra đường chéo C2 chứa 5 ô liên tiếp
    count = 1
    d = 1
    while x + d < roW and y - d > -1 and chessTable[x + d][y - d] == me:
        if count + d == 5:
            return True, 'c2', 4, 0
        d += 1
    d -= 1
    d1 = 1
    while x - d1 > -1 and y + d1 < coL and chessTable[x - d1][y + d1] == me:
        if count + d + d1 == 5:
            return True, 'c2', d, d1
        d1 += 1

    return False, None, None, None

# Hàm kiểm tra game kết thúc hay chưa
def gameOver(player, x, y):
    if x == -1 or y == -1:
        return False
    return checkEnd(HUMAN[0] if player == COMP[0] else COMP[0], x, y)[0]
# Hàm lấy tọa độ một điểm ngẫu nhiên ở các ô giữa
def get_random_middle_point():
    while True:
        x = random.randint(rowT[0] // 2 - 1, rowT[0] // 2)
        y = random.randint(colT[0] // 2 -1, colT[0] // 2)
        return x, y

# Hàm lấy hết ô trống còn lại trên bàn cờ
def get_remain_points(state):
    boxs = []
    for i in range(rowT[0]):
        for j in range(colT[0]):
            if state[i][j] == ' ':
                boxs.append([i, j])
    return boxs

def get_random_remain_point(state):
   boxs = get_remain_points(state)
   if boxs == []: return -1, -1
   return random.choice(boxs) 
