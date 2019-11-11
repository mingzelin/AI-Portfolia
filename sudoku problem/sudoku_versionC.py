from collections import defaultdict
import heapq,sys
import matplotlib.pyplot as plt
from math import log
import math


def getFrequency(var_matrix, y, x, count_list):
    matrix_length = 9
    #count num of occurance for each num on column nodes
    for k in range(matrix_length):
        if(k!=y):
            length = len(var_matrix[k][x])
            for i in range(length):
                num = var_matrix[k][x][i]
                count_list[num-1]+=1

    #count num of occurance for each num on column nodes
    for s in range(matrix_length):
        if((s!=x)):
            length = len(var_matrix[y][s])
            for i in range(length):
                num = var_matrix[y][s][i]
                count_list[num-1]+=1

    #count num of occurance for each num on column nodes
    group_x = x/3*3
    group_y = y/3*3
    for m in range(group_y, group_y+3):
        for n in range(group_x, group_x+3):
            if((m!=y)and(n!=x)):
                length = len(var_matrix[m][n])
                for i in range(length):
                    num = var_matrix[m][n][i]
                    count_list[num-1]+=1


def getConstraint(matrix, y, x):
    matrix_length = 9
    #check constraints on remaining variables on column nodes
    constraint_x = 0
    for k in range(matrix_length):
        if((k!=y)and(matrix[k][x]==0)):
            constraint_x+=1

    #check constraints on remaining variables on row nodes
    constraint_y = 0
    for s in range(matrix_length):
        if((s!=x)and(matrix[y][s]==0)):
            constraint_y+=1

    #check constraints on remaining variables on group nodes
    constraint_group = 0
    group_x = x/3*3
    group_y = y/3*3
    for m in range(group_y, group_y+3):
        for n in range(group_x, group_x+3):
            if((m!=y)and(n!=x)and(matrix[m][n]==0)):
                constraint_group+=1
    sum = constraint_x + constraint_y + constraint_group
    return sum


def has_conflict(matrix, value, y, x):
    matrix_length = 9
    #check column repitition
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

def backtrack_search(matrix, var_matrix, y, x, heap, diction, assign_count):
    matrix_length = 9
    original = matrix[y][x]#todo
    length = len(var_matrix[y][x])
    pop_stack = []
    used_num_list = []
    var_matrix_entry_len = len(var_matrix[y][x])
    todo = var_matrix_entry_len
    todo2 = str(var_matrix[y][x])
    #choose unassigned variable 'select'
    while(var_matrix_entry_len>0):
        var_matrix_entry_len-=1
        #least constraining value
        count_list = [0,0,0,0,0,0,0,0,0];
        getFrequency(var_matrix, y, x, count_list)
        least_cons_count = 100
        pick = 100
        for r in range(9):
            if((least_cons_count > count_list[r])and((r+1) in var_matrix[y][x])and(not (r+1) in used_num_list)):
                least_cons_count = count_list[r]
                pick = r+1
        assert(pick!=100)
        j = var_matrix[y][x].index(pick)
        used_num_list.append(pick)
        select = var_matrix[y][x][j]
        conflict = has_conflict(matrix, select, y, x)
        if(not conflict):
            assign_count[0]+=1
            if(assign_count[0]>=10000):
                return False
            matrix[y][x] = select
            pop_list = []
            forward_check_result = forward_check(select, var_matrix, y, x, pop_list,heap, diction, 1)
            if(forward_check_result):
                if(len(heap) == 0): #base case when heap is empty
                    return True
                #tie breaking process
                restricted_list = []
                node = heapq.heappop(heap)
                most_constrained = node
                restricted_list.append(node)
                while(heap!=[]): #pop all the same level restricted nodes
                    if(heap[0][0] == node[0]):
                        node = heapq.heappop(heap)
                        restricted_list.append(node)
                    else:
                        break

                restricted_len = len(restricted_list)
                #Choose variable with most constraints on remaining variables
                #choose the node that is affecting the most white blocks
                most_constrained = restricted_list[0]
                num_most_constraint = 0
                ind = 0
                for t in range(restricted_len):
                    constraint_num = getConstraint(matrix, restricted_list[t][1], restricted_list[t][2])
                    if(constraint_num > num_most_constraint):
                        most_constrained = restricted_list[t]
                        num_most_constraint = constraint_num
                        ind = t
                #put back rest of the restricted_list
                for w in range(restricted_len):
                    if(w!=ind):
                        heapq.heappush(heap, restricted_list[w])

                result = backtrack_search(matrix, var_matrix, most_constrained[1], most_constrained[2], heap, diction, assign_count)

                if result:
                    return result
                else: #recurse fail
                    undo_forward_check(select, var_matrix, pop_list,heap, diction) #undo pop_list
                    if(select!=var_matrix[y][x][j]):
                        #misplaced order
                        len_tmp = len(var_matrix[y][x])
                        for g in range(len_tmp):
                            if(select==var_matrix[y][x][g]):
                                pop_stack.append(select)
                                del var_matrix[y][x][g]
                                break
                #put recursed node back to heap
                node = []
                yy = most_constrained[1]
                xx = most_constrained[2]
                node.append(len(var_matrix[yy][xx]))
                node.append(yy)
                node.append(xx)
                heapq.heappush(heap, node)
            else:#forward check fail
                undo_forward_check(select, var_matrix, pop_list,heap, diction) #undo pop_list
                if(select!=var_matrix[y][x][j]):
                    #misplaced order
                    len_tmp = len(var_matrix[y][x])
                    for g in range(len_tmp):
                        if(select==var_matrix[y][x][g]):
                            pop_stack.append(select)
                            del var_matrix[y][x][g]
                            break
        else: #conflict fail
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
    #todo
    matrix[y][x] = original#todo
    return False

def forward_check(value, var_matrix, y, x, pop_list,heap, diction, status):
    #pop_list keep track of all the delete items, the structure is:
    #[ [Y, X] ...]
    #status indicates whether heap and diction is initiated
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
                        notmissing = any(elem == diction[y][s] for elem in heap)
                        if((status==1) and notmissing):
                            ###########
                            #update (y, x) length in heap
                            #rearrange heap
                            ind = heap.index(diction[y][s])
                            heap[ind] = heap[-1]
                            heap.pop()
                            heapq.heapify(heap)
                            node = diction[y][s]
                            node[0] -= 1
                            heapq.heappush(heap, node)
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
                        notmissing = any(elem == diction[k][x] for elem in heap)
                        if((status==1) and notmissing):
                            ###########
                            #update (y, x) length in heap
                            #rearrange heap
                            ind = heap.index(diction[k][x])
                            heap[ind] = heap[-1]
                            heap.pop()
                            heapq.heapify(heap)
                            node = diction[k][x]
                            node[0] -= 1
                            heapq.heappush(heap, node)
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
                            #here
                            del var_matrix[m][n][v]
                            notmissing = any(elem == diction[m][n] for elem in heap)
                            if((status==1) and notmissing):
                                ###########
                                #update (y, x) length in heap
                                #rearrange heap
                                ind = heap.index(diction[m][n])
                                heap[ind] = heap[-1]
                                heap.pop()
                                heapq.heapify(heap)
                                node = diction[m][n]
                                node[0] -= 1
                                heapq.heappush(heap, node)
                    if(len(var_matrix[m][n])==0):
                        return False
        #if var_matrix entry is empty then previous assumption must be wrong,
        #should return false and backtrack! otherwise return true
        return True


def undo_forward_check(value, var_matrix, pop_list, heap, diction):
    length = len(pop_list)
    for i in reversed(range(length)):
        y = pop_list[i][0]
        x = pop_list[i][1]
        v = pop_list[i][2]
        var_matrix[y][x].append(v)
        notmissing = any(elem == diction[y][x] for elem in heap)
        if(notmissing):
            ###########
            #update (y, x) length in heap
            #rearrange heap
            ind = heap.index(diction[y][x])
            heap[ind] = heap[-1]
            heap.pop()
            heapq.heapify(heap)
            node = diction[y][x]
            node[0] += 1
            heapq.heappush(heap, node)

if __name__=="__main__":
    average_list=[]
    average_list.insert(0,0)
    for f in range(1,72):
        average = 0
        num = 10
        for h in range(1,11):
            file = open("problems/"+ str(f) +"/"+ str(h)+".sd" , "r")
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
            for s in range(matrix_length): #var_matrix is generated
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


            #forward check
            pop_list = []
            for a in range(matrix_length):
                for b in range(matrix_length):
                    value = matrix[a][b]
                    forward_check(value, var_matrix, a, b, pop_list, [], [], 0)

            #heap keeps track of the num of remaining values for each entry in var_matrix
            #the structure is [ [(remain val num), X, Y] ...]
            heap = []
            diction = defaultdict(dict)
            for ff in range(matrix_length):
                for v in range(matrix_length):
                    length = len(var_matrix[ff][v])
                    node = []
                    node.append(length)
                    node.append(ff) #y
                    node.append(v) #x
                    heapq.heappush(heap, node)
                    diction[ff][v] = node

            #find soln by backtrack search
            most_constrained  = heapq.heappop(heap)
            most_constrained_y = most_constrained[1]
            most_constrained_x = most_constrained[2]
            assign_count = [0]
            result = backtrack_search(matrix, var_matrix, 0, 0, heap, diction, assign_count)
            print ("result is " +str(result) + " " + str(f)+ "-" + str(h))
            for row in matrix:
                print row
            average+=assign_count[0]
        average = round(average/num)
        average_list.append(average)
    plt.plot(average_list)
    plt.ylabel('average number of variable assignments')
    plt.xlabel('number of initial values')
    plt.show()

# Version C:
#
# Heap: priority queue that ranks by the smallest length(var_matrix[y][x])
# Heap will be changes whenever length(var_matrix[y][x]) is changed
#
# backtrack_search:
# Pop min from Heap (get the most restricted variable), if more than one has the same number of available variables, get the one that is affecting the most number white blocks by counting the number of white blocks on the same row, column 3x3 square (most constrained variable as tie breaker).
# Count the occurrence of each number from domain on the same row, column 3x3 square, choose the least occurred value (least constraining value), if it does not have conflict with the blocks on the same row, column 3x3 square, then do forward_check, if forward_check return true, then pop another min from Heap. If heap is empty, return True.
# If recursion (child) failed and come back, repeat.
# If recursion (child) succeed and come back, return True.
#
# forward_check:
# Say the current block is matrix[y][x] with value V, for each of the blocks on the same row, column 3x3 square, reduce V from their respective var_matrix[yi][xi], return true as long as none of var_matrix[yi][xi] is reduced to empty list, otherwise undo reduce (call undo_forward_check).
#
# (stats: real 0m25.082s user 0m21.536s sys 0m0.700s)
