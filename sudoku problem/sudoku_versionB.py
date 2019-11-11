import matplotlib.pyplot as plt
from math import log
import math

def has_conflict(matrix, value, y, x):
    #check column repitition
    matrix_length = 9
    for k in range(matrix_length):
        if(k!=y):
            if(matrix[k][x]==value):
                return True
    #check row repitition
    for s in range(matrix_length):
        if(s!=x):
            if(matrix[y][s]==value):
                return True
    group_x = x/3*3
    group_y = y/3*3
    #check group repitition
    for m in range(group_y, group_y+3):
        for n in range(group_x, group_x+3):
            if((m!=y)and(n!=x)):
                if(matrix[m][n]==value):
                    return True
    return False

def backtrack_search(matrix, var_matrix, y, x, assign_count):
    matrix_length = 9
    original = matrix[y][x]
    length = len(var_matrix[y][x])
    pop_stack = []

    #choose unassigned variable 'select'
    for i in range(length):
        j = length - 1 - i
        select = var_matrix[y][x][j]
        conflict = has_conflict(matrix, select, y, x)
        if(not conflict):
            assign_count[0]+=1
            if(assign_count[0]>=10000):
                return False
            matrix[y][x] = select
            pop_list = []
            forward_check_result = forward_check(select, var_matrix, y, x, pop_list)
            if(forward_check_result):
                if((y==(matrix_length-1))and(x==(matrix_length-1))): #base case
                    return True
                if(x== matrix_length-1): #move onto next entry
                    result = backtrack_search(matrix, var_matrix, y+1, 0, assign_count)
                else:
                    result = backtrack_search(matrix, var_matrix, y, x+1, assign_count)
                if result:
                    return result
                else: #continue loop
                    undo_forward_check(select, var_matrix, pop_list) #undo pop_list
                    if(select!=var_matrix[y][x][j]):
                        #misplaced order
                        len_tmp = len(var_matrix[y][x])
                        for g in range(len_tmp):
                            if(select==var_matrix[y][x][g]):
                                pop_stack.append(select)
                                del var_matrix[y][x][g]
                                break
            else:
                undo_forward_check(select, var_matrix, pop_list) #undo pop_list
                if(select!=var_matrix[y][x][j]):
                    #misplaced order
                    len_tmp = len(var_matrix[y][x])
                    for g in range(len_tmp):
                        if(select==var_matrix[y][x][g]):
                            pop_stack.append(select)
                            del var_matrix[y][x][g]
                            break
        else:
            if(select!=var_matrix[y][x][j]):
                #misplaced order
                len_tmp = len(var_matrix[y][x])
                for g in range(len_tmp):
                    if(select==var_matrix[y][x][g]):
                        pop_stack.append(select)
                        del var_matrix[y][x][g]
                        break
    #not path found thus revert action and backtrack
    length = len(pop_stack)
    for q in range(length):
        var_matrix[y][x].append(pop_stack[length - 1 - q])
    matrix[y][x] = original#todo
    return False

def forward_check(value, var_matrix, y, x, pop_list):
    #pop_list keep track of all the delete items, the structure is:
    #[ [Y, X] ...]
    matrix_length = 9
    if(value!=0):
        #reduce same row
        for s in range(matrix_length):
            if(s!=x):
                var_len = len(var_matrix[y][s])
                for i in reversed(range(var_len)): #reverse order del
                    if(var_matrix[y][s][i] == value):
                        node = []
                        node.append(y)
                        node.append(s)
                        node.append(value)
                        pop_list.append(node)
                        del var_matrix[y][s][i]
                if(len(var_matrix[y][s])==0):
                    return False

        #reduce same colum
        for k in range(matrix_length):
            if(k!=y):
                var_len = len(var_matrix[k][x])
                for j in reversed(range(var_len)): #reverse order del
                    if(var_matrix[k][x][j] == value):
                        node = []
                        node.append(k)
                        node.append(x)
                        node.append(value)
                        pop_list.append(node)
                        del var_matrix[k][x][j]
                if(len(var_matrix[k][x])==0):
                    return False
        #reduce same group
        group_x = x/3*3
        group_y = y/3*3
        #check group repitition
        for m in range(group_y, group_y+3):
            for n in range(group_x, group_x+3):
                if((m!=y)and(n!=x)):
                    var_len = len(var_matrix[m][n])
                    for v in reversed(range(var_len)): #reverse order del
                        if(var_matrix[m][n][v] == value):
                            node = []
                            node.append(m)
                            node.append(n)
                            node.append(value)
                            pop_list.append(node)
                            del var_matrix[m][n][v]
                    if(len(var_matrix[m][n])==0):
                        return False
        #if var_matrix entry is empty then previous assumption must be wrong,
        #should return false and backtrack! otherwise return true
        return True


def undo_forward_check(value, var_matrix, pop_list):
    length = len(pop_list)
    for i in reversed(range(length)):
        y = pop_list[i][0]
        x = pop_list[i][1]
        v = pop_list[i][2]
        var_matrix[y][x].append(v)

if __name__=="__main__":
    average_list=[]
    average_list.insert(0,0)
    for f in range(1, 72):
        average = 0
        num = 10
        for o in range(1, 11):
            file = open("problems/"+ str(f) +"/1.sd" , "r")
            #file = open("problems/18/1.sd" , "r")
            #file = open("test" , "r")
            matrix_length = 9
            #matrix is the list of given entries  [Yth row][Xth entry]
            matrix = []
            for y in range(matrix_length):
                given_row = []
                line = file.readline()
                if(len(line) != 0):
                    for x in range(matrix_length):
                        entry = int(line.split(" ")[x])
                        given_row.append(entry)
                matrix.append(given_row)
            #matrix is generated

            var_matrix = []
            #var_matrix is the matrix of all var  [Yth row][Xth entry][Kth var]

            for s in range(matrix_length):
                constraint_row = []
                for k in range(matrix_length):
                    constraint_entry = []
                    if(matrix[s][k]!=0):
                        constraint_entry.append(matrix[s][k])
                    else:
                        for m in range(9):
                            constraint_entry.append(m+1)
                    constraint_row.append(constraint_entry)
                var_matrix.append(constraint_row)
            #var_matrix is generated

            #forward check
            pop_list = []
            for a in range(matrix_length):
                for b in range(matrix_length):
                    value = matrix[a][b]
                    forward_check(value, var_matrix, a, b, pop_list)

            #find soln by backtrack search
            assign_count = [0]
            result = backtrack_search(matrix, var_matrix, 0, 0, assign_count)
            print ("result is " +str(result) + " " + str(f)+ "-" + str(o))
            for row in matrix:
                print row
            average+=assign_count[0]
        average = round(average/num)
        average_list.append(average)
    print(average_list)
    plt.plot(average_list)
    plt.ylabel('average number of variable assignments')
    plt.xlabel('number of initial values')
    plt.show()

# Version B:
#
# backtrack_search:
# Choose a coordinate (x1,y1), get one of the available variable from var_matrix[y1][x1], if it does not have conflict with the blocks on the same row, column 3x3 square, then do forward_check, if forward_check return true, then choose either coordinate(x1+1, y1) or (0, y1+1) to do recursion. If (x1,y1) = (8,8), return True.
# If recursion (child) failed and come back, choose the next available variable from var_matrix[y1][x1], if none available return False.
# If recursion (child) succeed and come back, return True.
#
# forward_check:
# Say the current block is matrix[y][x] with value V, for each of the blocks on the same row, column 3x3 square, reduce V from their respective var_matrix[yi][xi], return true as long as none of var_matrix[yi][xi] is reduced to empty list, otherwise undo reduce (call undo_forward_check).
#
# (stats: real 0m22.879s user 0m18.365s sys 0m0.749s)
