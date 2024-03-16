# Bàn cờ mặc định chessTable
chessTable = [[' ' for i in range(100)] for i in range(100)]
# Đánh dấu các điểm đã chọn
checkChess = [[False for i in range(100)] for i in range(100)]
# Số lượt đã chơi trong ván hiện tại
numPlay = [-1]
# Số lượt đi tối đa
maxNumPlay = [0]
# Giá trị số hàng và cột của bàn cờ
rowT = [0]
colT = [0]
# Thể loại chơi
typeG = [0]
# Đánh X hay O
choose_X_O = [0]
# Độ sâu của trò chơi
depth = [1]
# Độ sâu của trò chơi (máy đánh máy)
depthX = [1]
depthO = [1]
# Chữ cái của Computer và Human
COMP = ['o']
HUMAN = ['x']
# Biến lưu trữ vị trí đã đi qua của người và máy
store_Comp = [[-1, -1] for i in range(1000)]
store_Human = [[-1, -1] for i in range(1000)]
# Biến lưu trữ button vừa chọn
btn_Clicked = [-1, -1]
