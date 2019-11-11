import math
import copy
import random
import matplotlib.pyplot as plt

def distance(x1,y1, x2, y2):
    return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2)))


def annealing(list, value_max):
    plot_list = []
    size = len(list)###size of list
    T = 220 ###init annealing temperature
    ##calculate total distance of current config
    dist = 0
    for index in range(0, size-1):
        x1 = list[index][1]
        y1 = list[index][2]
        x2 = list[index+1][1]
        y2 = list[index+1][2]
        dist+=distance(x1, y1, x2, y2)

    #1. start with initial configs "list" (which is passed in) with value equal
    ##to maximum possible value deduct total distance
    ##we want to keep keep value as big as possible
    ##aka. keep distance as small as possible
    value = value_max - dist

    while(T>0.1):
        plot_list.append(dist)
        #print(T)
        #2. Moveset(list) = is any variation based on list
        ##where two of the distinct index are swapped (two of the cities' visited orders are mutually swapped)
        ##aka. list[i] & list[j] are swapped if i!=j & 0<=i<size & 0<=j<size

        #3. choose list2 randomly from Moveset(list)
        ###excluding the first and the last
        i = random.randint(1,size-2) ###choose index i
        j = random.randint(1,size-2) ###choose index j
        while(i==j):
            j = random.randint(1,size-2) ###i&j distinct

        list2 = copy.copy(list)
        tmp = list2[j]
        list2[j] = list2[i]
        list2[i] = tmp

        ###get sum of the randomly chosen list2
        dist = 0
        for index in range(0, size-1):
            x1 = list2[index][1]
            y1 = list2[index][2]
            x2 = list2[index+1][1]
            y2 = list2[index+1][2]
            dist+=distance(x1, y1, x2, y2)

        ### define value2
        value2 = value_max - dist

        #4. define delta_value
        delta_value = value2 - value

        #5. climb hill or move downhill by boltzmann distribution
        if(delta_value>0):
            list = list2
            value = value2
        else:
            ###with probability p, move downhill
            #todo   absolute value??
            p = round(math.pow(math.e, delta_value/T)*1000)
            r = random.randint(1,1000)
            if(r<=p):
                list = list2
                value = value2
                T-=0.05
        #6. Go to step2

    #7. eventually print list and distance
    print("The distance is: " + str(dist))
    print(list)

    #8. plot how the cost of the solution changes during one run of the algorithm
    plt.plot(plot_list)
    plt.ylabel('cost for TSP')
    plt.show()

if __name__=="__main__":
    file = open("randTSP/problem36", 'r')
    num = int(file.readline())
    list = []
    max_dist = 0
    for index in range(num):
      line = file.readline()
      if(len(line) != 0):
          triad = []
          name = line.split(" ")[0]
          triad.insert(0, name)
          x = int(line.split(" ")[1])
          triad.insert(1, x)
          y = int(line.split(" ")[2])
          dist = distance(x,y,0,0)
          if(dist>max_dist):
              max_dist=dist
      triad.insert(2, y)
      list.append(triad)
    list.append(copy.copy(list[0]))
    #the list is finished construction
    value_max = max_dist * len(list)
    #the initial configuration is argument "list"
    #the value of each configuration is value_max - total distance
    #the moveset of configuration list is any variation based on list
    ##where two of the distinct index are swapped (two of the cities' visited orders are mutually swapped)
    #probability p = boltzmann distribution
    annealing(list, value_max)
