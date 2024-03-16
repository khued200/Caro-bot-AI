import math
from tkinter import *
from Constants import *
from GameState import *

# Kiểm tra xem điểm có tệ không
def checkBad_Point(xx, yy):
    # 1
    if xx + 1 < rowT[0] and chessTable[xx + 1][yy] != ' ':
        return False
    # 2
    if yy + 1 < colT[0] and chessTable[xx][yy + 1] != ' ':
        return False
    # 3
    if xx > 0 and chessTable[xx - 1][yy] != ' ':
        return False
    # 4
    if yy > 0 and chessTable[xx][yy - 1] != ' ':
        return False
    # 5
    if xx + 1 < rowT[0] and yy + 1 < colT[0] and chessTable[xx + 1][yy + 1] != ' ':
        return False
    # 6
    if xx + 1 < rowT[0] and yy > 0 and chessTable[xx + 1][yy - 1] != ' ':
        return False
    # 7
    if yy + 1 < colT[0] and xx > 0 and chessTable[xx - 1][yy + 1] != ' ':
        return False
    # 8
    if yy > 0 and xx > 0 and chessTable[xx - 1][yy - 1] != ' ':
        return False
    return True

# Hàm đánh giá nước đi
def evaluate(player, x, y):
    # Nếu hết cờ
    if x != -1 and y != -1 and checkEnd(HUMAN[0] if player == COMP[0] else COMP[0], x, y)[0]:
        # Trả về vô cùng nếu máy thắng
        if player == HUMAN[0]:
            return math.inf
        else:
            return -math.inf # Trả về âm vô cùng nếu người thắng
    bot_score = 0 # Tổng điểm của máy
    human_score = 0 # Tổng điểm của người

    bot_4 = 0 # Chuỗi 4 ký tứ của máy trên 5 ô liên tục không bị chặn( Ví dụ o xxx x )
    bot_block_4 = 0 # Chuỗi 4 ký tứ của máy trên 5 ô liên tục nhưng bị chặn 1 đầu ( Ví dụ xxx xo)
    human_4 = 0 # Chuỗi 4 ký tứ của người trên 5 ô liên tục không bị chặn( Ví dụ o xxx x )
    human_block_4 = 0 # Chuỗi 4 ký tứ của người trên 5 ô liên tục nhưng bị chặn 1 đầu ( Ví dụ xxx xo)
    
    bot_3 = 0 # Chuỗi 3 ký tứ của máy trên 5 ô liên tục không bị chặn( Ví dụ o x xx )
    bot_block_3 = 0 # Chuỗi 3 ký tứ của máy trên 5 ô liên tục nhưng bị chặn 1 đầu ( Ví dụ xx xo)
    human_3 = 0 # Chuỗi 3 ký tứ của người trên 5 ô liên tục không bị chặn( Ví dụ o xx x )
    human_block_3 = 0 # Chuỗi 3 ký tứ của người trên 5 ô liên tục nhưng bị chặn 1 đầu ( Ví dụ x x xo)

    bot_2 = 0 # Chuỗi 2 ký tứ của người trên 5 ô liên tục không bị chặn( Ví dụ o  x x )
    bot_block_2 = 0 # Chuỗi 2 ký tứ của máy trên 5 ô liên tục nhưng bị chặn 1 đầu ( Ví dụ x xo)
    human_2 = 0 # Chuỗi 2 ký tứ của máy trên 5 ô liên tục không bị chặn( Ví dụ o  x x )
    human_block_2 = 0 # Chuỗi 2 ký tứ của người trên 5 ô liên tục nhưng bị chặn 1 đầu ( Ví dụ x xo)

    bot_nearby = 0 # Số lượng các phần tử máy cạnh phần tử người
    human_nearby = 0 # Số lượng các phần tử người cạnh phần tử cạnh

    # Tính điểm cho Comp
    for xx, yy in store_Comp:
        if xx == -1 or yy == -1:
            break
        # ĐẾM THEO HÀNG NGANG --

        # Kiểm tra xem tọa độ của điểm có trong trường hợp "tệ" hay không
        ## Trường hợp 1 là đứng đằng trước nó đã có 1 điểm khác được xét rồi (sẽ bị trùng dữ liệu, dữ liệu trùng thậm chí không đem lại tác dụng gì)
        ## Trường hợp 2 là 2 ô liên tiếp phía trước nó không có chứa ký tự gì cả
        ### Cách giải thích trên sẽ xuyên suốt hàm heuristic!
        b = False
        if yy > 0 and chessTable[xx][yy - 1] == COMP[0]:
            b = True
        if not b and yy + 2 < colT[0] and chessTable[xx][yy + 1] == ' ' and chessTable[xx][yy + 2] == ' ':
            b = True

        # Kiểm tra xem đằng trước nó có phải cạnh của bàn cờ hoặc một ký tự của người hay không
        ## Nếu có thì những chuỗi sẽ xét tới đều nằm trong diện "bị chặn"
        ### Cách giải thích này cũng tổng quát với cả 4 đường ngang, thẳng, C1, C2
        a = False
        if yy > 0 and chessTable[xx][yy - 1] == HUMAN[0]:
            a = True
        if yy == 0:
            a = True
        # nSpace là số ký tự trắng trên 4 phần tử đằng sau phần tử đang xét
        nSpace = 0

        # Duyệt 4 phần tử đằng sau nó
        for i in range(1, 5):
            # Nếu tệ thì hủy duyệt
            if b:
                break
            # Nếu gặp phải ký tự của người
            if yy + i < colT[0] and chessTable[xx][yy + i] == HUMAN[0]:
                # Nếu bị chặn thì sẽ loại (chặn 2 đầu không thể giành chiến thắng)
                if a:
                    break
                else:
                    # Cấp nhật số lượng các chuỗi vừa định nghĩa
                    ## Nếu đằng trước ký tự người là ký tự máy thì chuỗi sẽ bị chặn 1 đầu ( __xx_xo )
                    if chessTable[xx][yy + i - 1] != ' ':
                        if i - nSpace - 1 == 1:
                            bot_block_2 += 1
                        elif i - nSpace - 1 == 2:
                            # Trường hợp luôn tạo thành num3_Bloc
                            ## _x_xxo
                            if nSpace == 1:
                                bot_block_3 += 1
                            # Trường hợp chỉ tạo thành num3_Block điều kiện đặc biệt
                            ## Ví dụ __xxxo (tạo thành),, o_xxxo (loại)
                            elif yy - 2 >= 0 and chessTable[xx][yy - 2] == ' ':
                                bot_block_3 += 1
                        elif i - nSpace - 1 == 3:
                            bot_block_4 += 1
                    ## Nếu không phải ký tự máy thì không bị chặn đầu nào ( _xxx_o__)
                    else:
                        if i - nSpace - 1 == 1:
                            human_2 += 1
                        elif i - nSpace - 1 == 2:
                            # Trường hợp tốt: bot_3 có thể mở rộng trực tiếp thành bot_4: __xxx_o
                            if yy - 2 >= 0 and chessTable[xx][yy - 2] == ' ':
                                bot_3 += 1
                            else:
                                bot_block_3 += 1 # num3 chỉ có thể mở rộng lên num4_Block: |_xxx_o hoặc o_xxx_o
                    break

            # Nếu gặp phần tử trắng thì cập nhật số lượng
            if yy + i < colT[0] and chessTable[xx][yy + i] == ' ':
                nSpace += 1
            
            # Sau khi duyện hết 4 phần tử, cập nhật số lượng các chuỗi
            if i == 4 and yy + i < colT[0]:
                # Trường hợp xấu nhất nếu phần tử thứ 4 rơi vào cột cuối cùng của bảng và có ký tự máy ( Ví dụ __xx_xx| ) -> Bị chặn 1 đầu
                if yy + i == colT[0] - 1 and chessTable[xx][yy + i] == COMP[0]:
                    if i - nSpace == 3:
                        bot_block_4 += 1
                    elif i - nSpace == 2:
                        bot_block_3 += 1
                    elif i - nSpace == 1:
                        bot_block_2 += 1

                else:
                    if i - nSpace == 1:
                        if a:
                            bot_block_2 += 1
                        else:
                            human_2 += 1
                    elif i - nSpace == 2:
                        # Trường hợp đặc biệt, kể cả có ký tự người ở trước hay không thì 3 ký tự trong 5 ô liên tiếp không thể chuyển thành bot_4
                        ## Ví dụ: __x_x_x__
                        if chessTable[xx][yy + i] == COMP[0]:
                            bot_block_3 += 1
                        else:
                            if a:
                                bot_block_3 += 1
                            else: 
                                bot_3 += 1
                    elif i - nSpace == 3:
                        # Trường hợp đặc biệt, kể cả có ký tự người ở trước hay không thì 4 ký tự máy trong 5 ô liên tiếp vẫn có thể bị block
                        ## Ví dụ __xx_xx___ -> __xxoxx___
                        if chessTable[xx][yy + i] == COMP[0]:
                            bot_block_4 += 1
                        else:
                            if a:
                                bot_block_4 += 1
                            else:
                                bot_4 += 1
            # Trường hợp mở rộng ra 4 ô đằng sau vượt quá ranh giới trò chơi ( chuỗi sẽ tự động bị chặn 1 đầu ở ranh giới )
            if yy + i >= colT[0]:
                # Nếu bị chặn nốt đầu còn lại thì thoát ( __oxxxx| )
                if a:
                    break
                else:
                    if i - nSpace - 1 == 1:
                        bot_block_2 += 1
                    elif i - nSpace - 1 == 2:
                        # Trường hợp đặc biệt: phần tử cuối cùng trước khi chạm thành bảng là phần tử trống -> chuỗi 3 liên tục có thể mở rộng thành num4
                        ## Ví dụ: __xxx_| -> _xxxx_|
                        if chessTable[xx][yy + i - 1] == ' ':
                            # Trường hợp tạo thành num 3 trong điều kiện đặc biệt
                            ## Ví dụ __xxx_|
                            if yy - 2 >= 0 and chessTable[xx][yy - 2] == ' ':
                                bot_3 += 1
                            ## Không tạo được thành num 3: o_xxx_|
                            else:
                                bot_block_3 += 1
                        else:
                            # Trường hợp nếu có khoảng trắng -> luôn luôn tạo num3_Block
                            ## Ví dụ o_xx_x|
                            if nSpace == 1:
                                bot_block_3 += 1
                            # Nếu không có khoảng trắng thì tạo num3_Block trong điều kiện đặc biệt
                            ## Ví dụ: __xxx| (tạo thành) ,, o_xxx| (loại)
                            elif yy - 2 >= 0 and chessTable[xx][yy - 2] == ' ':
                                bot_block_3 += 1
                    elif i - nSpace - 1== 3: # Duy nhất trường hợp: __xxxx|
                        bot_block_4 += 1
                    break


        # ĐẾM THEO HÀNG DỌC |
        b = False
        if xx > 0 and chessTable[xx - 1][yy] == COMP[0]:
            b = True
        if not b and xx + 2 < rowT[0] and chessTable[xx + 1][yy] == ' ' and chessTable[xx + 2][yy] == ' ':
            b = True

        a = False
        nSpace = 0
        if xx > 0 and chessTable[xx - 1][yy] == HUMAN[0]:
            a = True
        if xx == 0:
            a = True

        for i in range(1, 5):
            if b:
                break
            if xx + i < rowT[0] and chessTable[xx + i][yy] == HUMAN[0]:
                if a:
                    break
                else:
                    if chessTable[xx + i - 1][yy] != ' ':
                        if i - nSpace - 1 == 1:
                            bot_block_2 += 1
                        elif i - nSpace - 1 == 2:
                            if nSpace == 1:
                                bot_block_3 += 1
                            elif xx - 2 >= 0 and chessTable[xx - 2][yy] == ' ':
                                bot_block_3 += 1
                        elif i - nSpace - 1 == 3:
                            bot_block_4 += 1
                    else:
                        if i - nSpace - 1 == 1:
                            human_2 += 1
                        elif i - nSpace - 1 == 2:
                            if xx - 2 >= 0 and chessTable[xx - 2][yy] == ' ':
                                bot_3 += 1
                            else:
                                bot_block_3 += 1
                    break
            if xx + i < rowT[0] and chessTable[xx + i][yy] == ' ':
                nSpace += 1
            if i == 4 and xx + i < rowT[0]:
                if xx + i == rowT[0] - 1 and chessTable[xx + i][yy] == COMP[0]:
                    if i - nSpace == 3:
                        bot_block_4 += 1
                    elif i - nSpace == 2:
                        bot_block_3 += 1
                    elif i - nSpace == 1:
                        bot_block_2 += 1

                else:
                    if i - nSpace == 1:
                        if a:
                            bot_block_2 += 1
                        else:
                            human_2 += 1
                    elif i - nSpace == 2:
                        if chessTable[xx + i][yy] == COMP[0]:
                            bot_block_3 += 1
                        else:
                            if a:
                                bot_block_3 += 1
                            else:
                                bot_3 += 1
                    elif i - nSpace == 3:
                        if chessTable[xx + i][yy] == COMP[0]:
                            bot_block_4 += 1
                        else:
                            if a:
                                bot_block_4 += 1
                            else:
                                bot_4 += 1
            if xx + i >= rowT[0]:
                if a:
                    break
                else:
                    if i - nSpace - 1 == 1:
                        bot_block_2 += 1
                    elif i - nSpace - 1 == 2:
                        if chessTable[xx + i - 1][yy] == ' ':
                            if xx - 2 >= 0 and chessTable[xx - 2][yy] == ' ':
                                bot_3 += 1
                            else:
                                bot_block_3 += 1
                        else:
                            if nSpace == 1:
                                bot_block_3 += 1
                            elif xx - 2 >= 0 and chessTable[xx - 2][yy] == ' ':
                                bot_block_3 += 1
                    elif i - nSpace -1 == 3:
                        bot_block_4 += 1
                    break
        
        # ĐẾM THEO ĐƯỜNG CHÉO C1 \
        b = False
        if yy > 0 and xx > 0 and chessTable[xx - 1][yy - 1] == COMP[0]:
            b = True
        if not b and yy + 2 < colT[0] and xx + 2 < rowT[0] and chessTable[xx + 1][yy + 1] == ' ' and chessTable[xx + 2][yy + 2] == ' ':
            b = True

        a = False
        nSpace = 0
        if yy > 0 and xx > 0 and chessTable[xx - 1][yy - 1] == HUMAN[0]:
            a = True
        if yy == 0 or xx == 0:
            a = True

        for i in range(1, 5):
            if b:
                break
            if yy + i < colT[0] and xx + i < rowT[0] and chessTable[xx + i][yy + i] == HUMAN[0]:
                if a:
                    break
                else:
                    if chessTable[xx + i - 1][yy + i - 1] != ' ':
                        if i - nSpace - 1 == 1:
                            bot_block_2 += 1
                        elif i - nSpace - 1 == 2:
                            if nSpace == 1:
                                bot_block_3 += 1
                            elif xx - 2 >= 0 and yy - 2 >= 0 and chessTable[xx - 2][yy - 2] == ' ':
                                bot_block_3 += 1
                        elif i - nSpace - 1 == 3:
                            bot_block_4 += 1
                    else:
                        if i - nSpace - 1 == 1:
                            human_2 += 1
                        elif i - nSpace - 1 == 2:
                            if xx - 2 >= 0 and yy - 2 >= 0 and chessTable[xx - 2][yy - 2] == ' ':
                                bot_3 += 1
                            else:
                                bot_block_3 += 1
                    break
            if yy + i < colT[0] and xx + i < rowT[0] and chessTable[xx + i][yy + i] == ' ':
                nSpace += 1
            if i == 4 and yy + i < colT[0] and xx + i < rowT[0]:
                if (yy + i == colT[0] - 1 or xx + i == rowT[0] - 1) and chessTable[xx + i][yy + i] == COMP[0]:
                    if i - nSpace == 3:
                        bot_block_4 += 1
                    elif i - nSpace == 2:
                        bot_block_3 += 1
                    elif i - nSpace == 1:
                        bot_block_2 += 1

                else:
                    if i - nSpace == 1:
                        if a:
                            bot_block_2 += 1
                        else:
                            human_2 += 1
                    elif i - nSpace == 2:
                        if chessTable[xx + i][yy + i] == COMP[0]:
                            bot_block_3 += 1
                        else:
                            if a:
                                bot_block_3 += 1
                            else:
                                bot_3 += 1
                    elif i - nSpace == 3:
                        if chessTable[xx + i][yy + i] == COMP[0]:
                            bot_block_4 += 1
                        else:
                            if a:
                                bot_block_4 += 1
                            else:
                                bot_4 += 1
            if xx + i >= rowT[0] or yy + i >= colT[0]:
                if a:
                    break
                else:
                    if i - nSpace - 1 == 1:
                        bot_block_2 += 1
                    elif i - nSpace - 1 == 2:
                        if chessTable[xx + i - 1][yy + i - 1] == ' ':
                            if xx - 2 >= 0 and yy - 2 >= 0 and chessTable[xx - 2][yy - 2] == ' ':
                                bot_3 += 1
                            else:
                                bot_block_3 += 1
                        else:
                            if nSpace == 1:
                                bot_block_3 += 1
                            elif xx - 2 >= 0 and yy - 2 >= 0 and chessTable[xx - 2][yy - 2] == ' ':
                                bot_block_3 += 1
                    elif i - nSpace - 1 == 3:
                        bot_block_4 += 1
                    break
        
        # ĐẾM THEO ĐƯỜNG CHÉO C2 /
        b = False
        if yy + 1 < colT[0] and xx > 0 and chessTable[xx - 1][yy + 1] == COMP[0]:
            b = True
        if not b and yy - 2 >= 0 and xx + 2 < rowT[0]  and chessTable[xx + 1][yy - 1] == ' ' and chessTable[xx + 2][yy - 2] == ' ':
            b = True

        a = False
        nSpace = 0
        if yy < colT[0] - 1 and xx > 0 and chessTable[xx - 1][yy + 1] == HUMAN[0]:
            a = True
        if yy == colT[0] - 1 or xx == 0:
            a = True

        for i in range(1, 5):
            if b:
                break
            if yy - i >= 0 and xx + i < rowT[0] and chessTable[xx + i][yy - i] == HUMAN[0]:
                if a:
                    break
                else:
                    if chessTable[xx + i - 1][yy - i + 1] != ' ':
                        if i - nSpace - 1 == 1:
                            bot_block_2 += 1
                        elif i - nSpace - 1 == 2:
                            if nSpace == 1:
                                bot_block_3 += 1
                            elif xx - 2 >= 0 and yy + 2 < colT[0] and chessTable[xx - 2][yy + 2] == ' ':
                                bot_block_3 += 1
                        elif i - nSpace - 1 == 3:
                            bot_block_4 += 1
                    else:
                        if i - nSpace - 1 == 1:
                            human_2 += 1
                        elif i - nSpace - 1 == 2:
                            if yy + 2 < colT[0] and xx - 2 >= 0 and chessTable[xx - 2][yy + 2] == ' ':
                                bot_3 += 1
                            else:
                                bot_block_3 += 1
                    break
            if yy - i >= 0  and xx + i < rowT[0] and chessTable[xx + i][yy - i] == ' ':
                nSpace += 1
            if i == 4 and yy - i >= 0  and xx + i < rowT[0]:
                if (yy - i == 0 or xx + i == rowT[0] - 1) and chessTable[xx + i][yy - i] == COMP[0]:
                    if i - nSpace == 3:
                        bot_block_4 += 1
                    elif i - nSpace == 2:
                        bot_block_3 += 1
                    elif i - nSpace == 1:
                        bot_block_2 += 1

                else:
                    if i - nSpace == 1:
                        if a:
                            bot_block_2 += 1
                        else:
                            human_2 += 1
                    elif i - nSpace == 2:
                        if chessTable[xx + i][yy - i] == COMP[0]:
                            bot_block_3 += 1
                        else:
                            if a:
                                bot_block_3 += 1
                            else:
                                bot_3 += 1
                    elif i - nSpace == 3:
                        if chessTable[xx + i][yy - i] == COMP[0]:
                            bot_block_4 += 1
                        else:
                            if a:
                                bot_block_4 += 1
                            else:
                                bot_4 += 1
            if xx + i >= rowT[0] or yy - i < 0:
                if a:
                    break
                else:
                    if i - nSpace - 1== 1:
                        bot_block_2 += 1
                    elif i - nSpace - 1== 2:
                        if chessTable[xx + i - 1][yy - i + 1] == ' ':
                            if xx - 2 >= 0 and yy + 2 < colT[0] and chessTable[xx - 2][yy + 2] == ' ':
                                bot_3 += 1
                            else:
                                bot_block_3 += 1
                        else:
                            if nSpace == 1:
                                bot_block_3 += 1
                            elif xx - 2 >= 0 and yy + 2 < colT[0] and chessTable[xx - 2][yy + 2] == ' ':
                                bot_block_3 += 1
                    elif i - nSpace - 1== 3:
                        bot_block_4 += 1
                    break
        
        if xx + 1 < rowT[0] and chessTable[xx + 1][yy] == HUMAN[0]:
            human_nearby += 1
        if yy + 1 < colT[0] and chessTable[xx][yy + 1] == HUMAN[0]:
            human_nearby += 1
        if xx > 0 and chessTable[xx - 1][yy] == HUMAN[0]:
            human_nearby += 1
        if yy > 0 and chessTable[xx][yy - 1] == HUMAN[0]:
            human_nearby += 1
        if xx + 1 < rowT[0] and yy + 1 < colT[0] and chessTable[xx + 1][yy + 1] == HUMAN[0]:
            human_nearby += 1
        if xx + 1 < rowT[0] and yy > 0 and chessTable[xx + 1][yy - 1] == HUMAN[0]:
            human_nearby += 1
        if yy + 1 < colT[0] and xx > 0 and chessTable[xx - 1][yy + 1] == HUMAN[0]:
            human_nearby += 1
        if yy > 0 and xx > 0 and chessTable[xx - 1][yy - 1] == HUMAN[0]:
            human_nearby += 1

    # Tính điểm cho Người
    for xx, yy in store_Human:
        if xx == -1 or yy == -1:
            break
        # ĐẾM THEO HÀNG NGANG --
        # ĐẾM THEO HÀNG NGANG --
        b = False
        if yy > 0 and chessTable[xx][yy - 1] == HUMAN[0]:
            b = True
        if not b and yy + 2 < colT[0] and chessTable[xx][yy + 1] == ' ' and chessTable[xx][yy + 2] == ' ':
            b = True

        a = False
        if yy > 0 and chessTable[xx][yy - 1] == COMP[0]:
            a = True
        if yy == 0:
            a = True
        nSpace = 0

        for i in range(1, 5):
            if b:
                break
            if yy + i < colT[0] and chessTable[xx][yy + i] == COMP[0]:
                if a:
                    break
                else:
                    if chessTable[xx][yy + i - 1] != ' ':
                        if i - nSpace - 1 == 1:
                            human_block_2 += 1
                        elif i - nSpace - 1 == 2:
                            if nSpace == 1:
                                human_block_3 += 1
                            elif yy - 2 >= 0 and chessTable[xx][yy - 2] == ' ':
                                human_block_3 += 1
                        elif i - nSpace - 1 == 3:
                            human_block_4 += 1
                    else:
                        if i - nSpace - 1 == 1:
                            bot_2 += 1
                        elif i - nSpace - 1 == 2:
                            if yy - 2 >= 0 and chessTable[xx][yy - 2] == ' ':
                                human_3 += 1
                            else:
                                human_block_3 += 1 
                    break
            if yy + i < colT[0] and chessTable[xx][yy + i] == ' ':
                nSpace += 1
            
            if i == 4 and yy + i < colT[0]:
                if yy + i == colT[0] - 1 and chessTable[xx][yy + i] == HUMAN[0]:
                    if i - nSpace == 3:
                        human_block_4 += 1
                    elif i - nSpace == 2:
                        human_block_3 += 1
                    elif i - nSpace == 1:
                        human_block_2 += 1

                else:
                    if i - nSpace == 1:
                        if a:
                            human_block_2 += 1
                        else:
                            bot_2 += 1
                    elif i - nSpace == 2:
                        if chessTable[xx][yy + i] == HUMAN[0]:
                            human_block_3 += 1
                        else:
                            if a:
                                human_block_3 += 1
                            else: 
                                human_3 += 1
                    elif i - nSpace == 3:
                        if chessTable[xx][yy + i] == HUMAN[0]:
                            human_block_4 += 1
                        else:
                            if a:
                                human_block_4 += 1
                            else:
                                human_4 += 1
            if yy + i >= colT[0]:
                if a:
                    break
                else:
                    if i - nSpace - 1 == 1:
                        human_block_2 += 1
                    elif i - nSpace - 1 == 2:
                        if chessTable[xx][yy + i - 1] == ' ':
                            if yy - 2 >= 0 and chessTable[xx][yy - 2] == ' ':
                                human_3 += 1
                            else:
                                human_block_3 += 1
                        else:
                            if nSpace == 1:
                                human_block_3 += 1
                            elif yy - 2 >= 0 and chessTable[xx][yy - 2] == ' ':
                                human_block_3 += 1
                    elif i - nSpace - 1== 3: 
                        human_block_4 += 1
                    break


        # ĐẾM THEO HÀNG DỌC |
        b = False
        if xx > 0 and chessTable[xx - 1][yy] == HUMAN[0]:
            b = True
        if not b and xx + 2 < rowT[0] and chessTable[xx + 1][yy] == ' ' and chessTable[xx + 2][yy] == ' ':
            b = True

        a = False
        nSpace = 0
        if xx > 0 and chessTable[xx - 1][yy] == COMP[0]:
            a = True
        if xx == 0:
            a = True

        for i in range(1, 5):
            if b:
                break
            if xx + i < rowT[0] and chessTable[xx + i][yy] == COMP[0]:
                if a:
                    break
                else:
                    if chessTable[xx + i - 1][yy] != ' ':
                        if i - nSpace - 1 == 1:
                            human_block_2 += 1
                        elif i - nSpace - 1 == 2:
                            if nSpace == 1:
                                human_block_3 += 1
                            elif xx - 2 >= 0 and chessTable[xx - 2][yy] == ' ':
                                human_block_3 += 1
                        elif i - nSpace - 1 == 3:
                            human_block_4 += 1
                    else:
                        if i - nSpace - 1 == 1:
                            bot_2 += 1
                        elif i - nSpace - 1 == 2:
                            if xx - 2 >= 0 and chessTable[xx - 2][yy] == ' ':
                                human_3 += 1
                            else:
                                human_block_3 += 1
                    break
            if xx + i < rowT[0] and chessTable[xx + i][yy] == ' ':
                nSpace += 1
            if i == 4 and xx + i < rowT[0]:
                if xx + i == rowT[0] - 1 and chessTable[xx + i][yy] == HUMAN[0]:
                    if i - nSpace == 3:
                        human_block_4 += 1
                    elif i - nSpace == 2:
                        human_block_3 += 1
                    elif i - nSpace == 1:
                        human_block_2 += 1

                else:
                    if i - nSpace == 1:
                        if a:
                            human_block_2 += 1
                        else:
                            bot_2 += 1
                    elif i - nSpace == 2:
                        if chessTable[xx + i][yy] == HUMAN[0]:
                            human_block_3 += 1
                        else:
                            if a:
                                human_block_3 += 1
                            else:
                                human_3 += 1
                    elif i - nSpace == 3:
                        if chessTable[xx + i][yy] == HUMAN[0]:
                            human_block_4 += 1
                        else:
                            if a:
                                human_block_4 += 1
                            else:
                                human_4 += 1
            if xx + i >= rowT[0]:
                if a:
                    break
                else:
                    if i - nSpace - 1 == 1:
                        human_block_2 += 1
                    elif i - nSpace - 1 == 2:
                        if chessTable[xx + i - 1][yy] == ' ':
                            if xx - 2 >= 0 and chessTable[xx - 2][yy] == ' ':
                                human_3 += 1
                            else:
                                human_block_3 += 1
                        else:
                            if nSpace == 1:
                                human_block_3 += 1
                            elif xx - 2 >= 0 and chessTable[xx - 2][yy] == ' ':
                                human_block_3 += 1
                    elif i - nSpace -1 == 3:
                        human_block_4 += 1
                    break
        
        # ĐẾM THEO ĐƯỜNG CHÉO C1 \
        b = False
        if yy > 0 and xx > 0 and chessTable[xx - 1][yy - 1] == HUMAN[0]:
            b = True
        if not b and yy + 2 < colT[0] and xx + 2 < rowT[0] and chessTable[xx + 1][yy + 1] == ' ' and chessTable[xx + 2][yy + 2] == ' ':
            b = True

        a = False
        nSpace = 0
        if yy > 0 and xx > 0 and chessTable[xx - 1][yy - 1] == COMP[0]:
            a = True
        if yy == 0 or xx == 0:
            a = True

        for i in range(1, 5):
            if b:
                break
            if yy + i < colT[0] and xx + i < rowT[0] and chessTable[xx + i][yy + i] == COMP[0]:
                if a:
                    break
                else:
                    if chessTable[xx + i - 1][yy + i - 1] != ' ':
                        if i - nSpace - 1 == 1:
                            human_block_2 += 1
                        elif i - nSpace - 1 == 2:
                            if nSpace == 1:
                                human_block_3 += 1
                            elif xx - 2 >= 0 and yy - 2 >= 0 and chessTable[xx - 2][yy - 2] == ' ':
                                human_block_3 += 1
                        elif i - nSpace - 1 == 3:
                            human_block_4 += 1
                    else:
                        if i - nSpace - 1 == 1:
                            bot_2 += 1
                        elif i - nSpace - 1 == 2:
                            if xx - 2 >= 0 and yy - 2 >= 0 and chessTable[xx - 2][yy - 2] == ' ':
                                human_3 += 1
                            else:
                                human_block_3 += 1
                    break
            if yy + i < colT[0] and xx + i < rowT[0] and chessTable[xx + i][yy + i] == ' ':
                nSpace += 1
            if i == 4 and yy + i < colT[0] and xx + i < rowT[0]:
                if (yy + i == colT[0] - 1 or xx + i == rowT[0] - 1) and chessTable[xx + i][yy + i] == HUMAN[0]:
                    if i - nSpace == 3:
                        human_block_4 += 1
                    elif i - nSpace == 2:
                        human_block_3 += 1
                    elif i - nSpace == 1:
                        human_block_2 += 1

                else:
                    if i - nSpace == 1:
                        if a:
                            human_block_2 += 1
                        else:
                            bot_2 += 1
                    elif i - nSpace == 2:
                        if chessTable[xx + i][yy + i] == HUMAN[0]:
                            human_block_3 += 1
                        else:
                            if a:
                                human_block_3 += 1
                            else:
                                human_3 += 1
                    elif i - nSpace == 3:
                        if chessTable[xx + i][yy + i] == HUMAN[0]:
                            human_block_4 += 1
                        else:
                            if a:
                                human_block_4 += 1
                            else:
                                human_4 += 1
            if xx + i >= rowT[0] or yy + i >= colT[0]:
                if a:
                    break
                else:
                    if i - nSpace - 1 == 1:
                        human_block_2 += 1
                    elif i - nSpace - 1 == 2:
                        if chessTable[xx + i - 1][yy + i - 1] == ' ':
                            if xx - 2 >= 0 and yy - 2 >= 0 and chessTable[xx - 2][yy - 2] == ' ':
                                human_3 += 1
                            else:
                                human_block_3 += 1
                        else:
                            if nSpace == 1:
                                human_block_3 += 1
                            elif xx - 2 >= 0 and yy - 2 >= 0 and chessTable[xx - 2][yy - 2] == ' ':
                                human_block_3 += 1
                    elif i - nSpace - 1 == 3:
                        human_block_4 += 1
                    break
        
        # ĐẾM THEO ĐƯỜNG CHÉO C2 /
        b = False
        if yy + 1 < colT[0] and xx > 0 and chessTable[xx - 1][yy + 1] == HUMAN[0]:
            b = True
        if not b and yy - 2 >= 0 and xx + 2 < rowT[0]  and chessTable[xx + 1][yy - 1] == ' ' and chessTable[xx + 2][yy - 2] == ' ':
            b = True

        a = False
        nSpace = 0
        if yy < colT[0] - 1 and xx > 0 and chessTable[xx - 1][yy + 1] == COMP[0]:
            a = True
        if yy == colT[0] - 1 or xx == 0:
            a = True

        for i in range(1, 5):
            if b:
                break
            if yy - i >= 0 and xx + i < rowT[0] and chessTable[xx + i][yy - i] == COMP[0]:
                if a:
                    break
                else:
                    if chessTable[xx + i - 1][yy - i + 1] != ' ':
                        if i - nSpace - 1 == 1:
                            human_block_2 += 1
                        elif i - nSpace - 1 == 2:
                            if nSpace == 1:
                                human_block_3 += 1
                            elif xx - 2 >= 0 and yy + 2 < colT[0] and chessTable[xx - 2][yy + 2] == ' ':
                                human_block_3 += 1
                        elif i - nSpace - 1 == 3:
                            human_block_4 += 1
                    else:
                        if i - nSpace - 1 == 1:
                            bot_2 += 1
                        elif i - nSpace - 1 == 2:
                            if yy + 2 < colT[0] and xx - 2 >= 0 and chessTable[xx - 2][yy + 2] == ' ':
                                human_3 += 1
                            else:
                                human_block_3 += 1
                    break
            if yy - i >= 0  and xx + i < rowT[0] and chessTable[xx + i][yy - i] == ' ':
                nSpace += 1
            if i == 4 and yy - i >= 0  and xx + i < rowT[0]:
                if (yy - i == 0 or xx + i == rowT[0] - 1) and chessTable[xx + i][yy - i] == HUMAN[0]:
                    if i - nSpace == 3:
                        human_block_4 += 1
                    elif i - nSpace == 2:
                        human_block_3 += 1
                    elif i - nSpace == 1:
                        human_block_2 += 1

                else:
                    if i - nSpace == 1:
                        if a:
                            human_block_2 += 1
                        else:
                            bot_2 += 1
                    elif i - nSpace == 2:
                        if chessTable[xx + i][yy - i] == HUMAN[0]:
                            human_block_3 += 1
                        else:
                            if a:
                                human_block_3 += 1
                            else:
                                human_3 += 1
                    elif i - nSpace == 3:
                        if chessTable[xx + i][yy - i] == HUMAN[0]:
                            human_block_4 += 1
                        else:
                            if a:
                                human_block_4 += 1
                            else:
                                human_4 += 1
            if xx + i >= rowT[0] or yy - i < 0:
                if a:
                    break
                else:
                    if i - nSpace - 1== 1:
                        human_block_2 += 1
                    elif i - nSpace - 1== 2:
                        if chessTable[xx + i - 1][yy - i + 1] == ' ':
                            if xx - 2 >= 0 and yy + 2 < colT[0] and chessTable[xx - 2][yy + 2] == ' ':
                                human_3 += 1
                            else:
                                human_block_3 += 1
                        else:
                            if nSpace == 1:
                                human_block_3 += 1
                            elif xx - 2 >= 0 and yy + 2 < colT[0] and chessTable[xx - 2][yy + 2] == ' ':
                                human_block_3 += 1
                    elif i - nSpace - 1== 3:
                        human_block_4 += 1
                    break
        
        if xx + 1 < rowT[0] and chessTable[xx + 1][yy] == COMP[0]:
            bot_nearby += 1
        if yy + 1 < colT[0] and chessTable[xx][yy + 1] == COMP[0]:
            bot_nearby += 1
        if xx > 0 and chessTable[xx - 1][yy] == COMP[0]:
            bot_nearby += 1
        if yy > 0 and chessTable[xx][yy - 1] == COMP[0]:
            bot_nearby += 1
        if xx + 1 < rowT[0] and yy + 1 < colT[0] and chessTable[xx + 1][yy + 1] == COMP[0]:
            bot_nearby += 1
        if xx + 1 < rowT[0] and yy > 0 and chessTable[xx + 1][yy - 1] == COMP[0]:
            bot_nearby += 1
        if yy + 1 < colT[0] and xx > 0 and chessTable[xx - 1][yy + 1] == COMP[0]:
            bot_nearby += 1
        if yy > 0 and xx > 0 and chessTable[xx - 1][yy - 1] == COMP[0]:
            bot_nearby += 1
    

    # Công thức tính điểm bàn cờ của hàm heuristic h(n)
    ## Trong trường hợp player là người, tức nước đi vừa rồi là của máy đánh
    if player == HUMAN[0]:
        # Nếu máy đánh xong mà bàn cờ vẫn còn 3 ký tự người liên tục không bị chặn hoặc 4 ký tự bị chặn thì người thắng
        if human_3 > 0 or human_4 > 0 or human_block_4 > 0:
            return -5555555555555555555
        # Nếu máy đánh được nước dẫn tới 4 ký tự máy liên tục không bị chặn thì máy thắng
        if bot_4 > 0:
            return 5555555555555555555
        # Nếu máy đánh được nước dẫn tới nước đôi 4 ký tự máy liên tục bị chặn thì máy thắng
        if bot_block_4 >= 2:
            return 5555555555555555555
        # Nếu máy không có nước 4 nào và người có nước 3 không bị chặn thì người thắng
        ## Giải thích: tới phiên của người sẽ đánh biến nước 3 thành nước 4 không bị chặn, khi ấy người sẽ thắng
        if bot_block_4 == 0 and human_3 > 0:
            return -555555555555555555
        # Nếu máy có nước đôi 3 ký tự không bị chặn trong khi đó người không có nước 3 nào thì máy sẽ thắng
        ## Trong trường hợp người có nước 3 chưa chắc máy đã thắng
        ### Ví dụ: xxx          ->       xxx        ->         xxx        ->       oxxx
                #    x                     x                     x                    x
                #    x                     x                     x                    x
                #    _ooox                 oooox                xoooox               xooox
        ### Thậm chí máy còn có thể thua ngược nếu như không có quân x ở cuối chuỗi 3 
        if bot_3 >= 2 and human_3 == 0 and human_block_3 == 0:
            return 555555555555555555
        
        # Công thức tính điểm tổng quát dưới đây trong trường hợp 2 bên chưa chắc ai thắng có thể sẽ gặp nhiều sai sót, trong quá trình làm việc sẽ tiếp tục cập nhật
        # và đánh giá thay đổi hệ số của các chuỗi mỗi quân cờ
        bot_score = 2 * human_nearby + 20 * bot_block_2 + 100 * human_2 + 3000 * bot_block_3 + 300000 * bot_3 + bot_block_4 * 30000000
        human_score = bot_nearby + 70 * human_block_2 + 250 * bot_2 + 4000 * human_block_3  + human_3 * 30000000
        return bot_score - human_score
    ## Trường hợp với bot cũng tương tự
    else:
        if bot_3 > 0 or bot_4 > 0 or bot_block_4 > 0:
            return 5555555555555555555
        if human_4 > 0:
            return -5555555555555555555
        if human_block_4 >= 2:
            return -5555555555555555555
        if human_block_4 == 0 and bot_3 > 0:
            return 555555555555555555
        if human_3 >= 2 and bot_3 == 0 and bot_block_3 == 0:
            return -555555555555555555
        human_score = 2 * bot_nearby + 70 * human_block_2 + 250 * bot_2 + 3000 * human_block_3 + 300000 * human_3 + human_block_4 * 30000000
        bot_score = human_nearby + 20 * bot_block_2 + 100 * human_2 + 4000 * bot_block_3 + bot_3 * 30000000
        return bot_score - human_score

