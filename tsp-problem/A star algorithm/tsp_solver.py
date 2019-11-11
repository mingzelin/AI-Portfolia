import math
import copy
import heapq
import matplotlib.pyplot as plt
from math import log

def distance(x1,y1, x2, y2):
    return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2)))


def heuristic(curr_node, list, len, head_node):
    #part 1 find the min distance from curr node
    min_dist_to_curr = -1;
    for i in range(len):
        dist = distance(curr_node[1], curr_node[2], list[i][1], list[i][2])
        if (min_dist_to_curr == -1):
            min_dist_to_curr = dist
        if (min_dist_to_curr > dist):
            min_dist_to_curr = dist
    #part 2 order all the distance in list
    connection_num = len - 1;
    dist_list = []
    for j in range(len):
        for k in range(len):
            if(j != k):
                dist = distance(list[j][1], list[j][2], list[k][1], list[k][2])
                dist_list.append(dist)
    dist_list.sort()
    sum = 0
    for s in range(connection_num):
        sum += dist_list[s]

    #part 3 find the min distance to start node
    min_dist_to_start = -1;
    for l in range(len):
        dist = distance(head_node[1], head_node[2], list[l][1], list[l][2])
        if (min_dist_to_start == -1):
            min_dist_to_start = dist
        if (min_dist_to_start > dist):
            min_dist_to_start = dist
    #part 4 bring together all three parts
    total = min_dist_to_curr + sum + min_dist_to_start;
    return total

def Astar(list, size, numOfNodes):
    #curr_index = random.randint(0,size-1)  #todo
    curr_index= 0
    curr_node = list[curr_index]
    head_node = list[curr_index]
    del list[curr_index]
    total_distance = 0
    #heap has structure:
    #[[f, g, name, X, Y, [ visited of nodes name]] [[unvisited nodes, X, Y ]...]...]
    heap = []
    node = []
    node.append(0)
    node.append(0)
    node.append(curr_node[0])
    node.append(curr_node[1])
    node.append(curr_node[2])
    node.append([])
    node[5].append(curr_node[0]) #append itself to visited list
    node.append(copy.copy(list)) #init unvisited list
    heapq.heappush(heap, node)
    numOfNodes[0]+=1
    curr_node = heapq.heappop(heap)
    numOfNodes[0]+=1

    while (len(curr_node[5]) != (size+1)): #one more go to get back to start point
        if (len(curr_node[5]) == size): #last step special case
            dist = distance(curr_node[3], curr_node[4], head_node[1], head_node[2])
            g = curr_node[1] + dist
            f = g + 0 #note h is 0
            node = []
            node.append(f)  #f
            node.append(g)  #g
            node.append(head_node[0])   #name
            node.append(head_node[1])   #X
            node.append(head_node[2])   #Y
            passed = copy.copy(curr_node[5])
            passed.append(head_node[0]) ##append head to visited
            node.append(passed) #visited list
            node.append([])#special: append start node to unvisited
            heapq.heappush(heap, node)
            numOfNodes[0]+=1
        else:
            unvisited = curr_node[6]
            length = len(unvisited)
            for i in range(length):
                dist = distance(curr_node[3], curr_node[4], unvisited[i][1], unvisited[i][2])
                g = curr_node[1] + dist
                unpassed = copy.copy(unvisited)
                del unpassed[i] ##pop itself from unvisited
                h = heuristic(unvisited[i], unpassed, length-1, head_node)
                f = g + h
                node = []
                node.append(f)  #f
                node.append(g)  #g
                node.append(unvisited[i][0])   #name
                node.append(unvisited[i][1])   #X
                node.append(unvisited[i][2])   #Y
                passed = copy.copy(curr_node[5])
                passed.append(unvisited[i][0]) ##append itself to visited
                node.append(passed) #visited list
                node.append(unpassed) #unvisited list
                heapq.heappush(heap, node)
                numOfNodes[0]+=1
        curr_node = heapq.heappop(heap)

    total_distance = curr_node[1]
    print ("The total distance is: " + str(total_distance))
    print "The path is: "
    print curr_node[5]
    return total_distance



if __name__=="__main__":
    average_list=[]
    for m in range(1,14):
        average = 0
        for n in range(1,11):
            file = open("randTSP/"+ str(m) +"/instance_"+ str(n) +".txt", 'r')
            #file = open("randTSP/problem36", 'r')
            num = int(file.readline())
            list = []
            for index in range(num):
              line = file.readline()
              if(len(line) != 0):
                  triad = []
                  name = line.split(" ")[0]
                  triad.insert(0, name)
                  x = int(line.split(" ")[1])
                  triad.insert(1, x)
                  y = int(line.split(" ")[2])
              triad.insert(2, y)
              list.append(triad)
            #the list is built
            numOfNodes = [0]
            dist = Astar(list, len(list), numOfNodes)
            average+=numOfNodes[0]
        average = round(average/10)
        print("The average of "+ str(m) +" cities is: " + str(average) + " nodes: " + str(numOfNodes[0]))
        average_list.append(average)
    print(average_list)
    average_list.insert(0,0)
    length = len(average_list)
    for k in range(1, length):
        average_list[k] = log(average_list[k])
    plt.plot(average_list)
    plt.ylabel('average nodes')
    plt.show()
#[3.0, 4.0, 8.0, 13.0, 27.0, 56.0, 213.0, 584.0, 1794.0, 5980.0, 12903.0, 80480.0, 172421.0, 480013.0, 942754*8+, 13.5]
