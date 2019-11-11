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
    original = matrix[y][x]#todo
    length = len(var_matrix[y][x])

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
            if((y==(matrix_length-1))and(x==(matrix_length-1))): #base case
                return True
            if(x== matrix_length-1): #move onto next entry
                result = backtrack_search(matrix, var_matrix, y+1, 0, assign_count)
            else:
                result = backtrack_search(matrix, var_matrix, y, x+1, assign_count)
            if result:
                return result
    #not path found thus revert action and backtrack
    matrix[y][x] = original#todo
    return False

#backtracking version
if __name__=="__main__":
    average_list=[]
    average_list.insert(0,0)
    for f in range(1, 72):
        average = 0
        num = 10
        for o in range(1, 11):
            file = open("problems/"+ str(f) +"/" + str(o)  + ".sd" , "r")
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
            #var_matrix is the matrix of all constraint  [Yth row][Xth entry][Kth constraint]
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
    #

# Version A:
#
# backtrack_search:
# Choose a coordinate (x1,y1), get one of the available variable from var_matrix[y1][x1], if it does not have conflict with the blocks on the same row, column 3x3 square, then choose either coordinate(x1+1, y1) or (0, y1+1) to do recursion. If (x1,y1) = (8,8), return True.
# If recursion (child) failed and come back, choose the next available variable from var_matrix[y1][x1], if none available return False.
# If recursion (child) succeed and come back, return True.
#
# (stats: real 0m21.875s user 0m16.788s sys 0m0.351s)
