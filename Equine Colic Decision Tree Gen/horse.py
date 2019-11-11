import math

class Node:
  def __init__(self, parent, attr_pair, values, left, right):
    self.parent = parent
    self.attr_pair = attr_pair
    self.values = values
    self.left = left
    self.right = right
    #root has no parent
    #branch has parent and 2 children
    #leave has parent but no children and no attr_pair

def infoContent(p, n):
    p = float(p)
    n = float(n)
    if((p==0)and(n==0)):
        content = 0
    elif(p==0):
        content = (-p/(p+n))*0-(n/(p+n))*math.log((n/(p+n)),2)
    elif(n==0):
        content = (-p/(p+n))*math.log((p/(p+n)),2)-(n/(p+n))*0
    else:
        content = (-p/(p+n))*math.log((p/(p+n)),2)-(n/(p+n))*math.log((n/(p+n)),2)
    return content

def infoGain(p, n, p1, n1, p2, n2):
    p = float(p)
    n = float(n)
    p1 = float(p1)
    n1 = float(n1)
    p2 = float(p2)
    n2 = float(n2)
    if((p==0)and(n==0)):
        return 0
    content = infoContent(p, n)
    remainder = (p1+n1)/(p+n)*infoContent(p1,n1)+(p2+n2)/(p+n)*infoContent(p2,n2)
    gain = content - remainder
    return gain

def isSame(examples):
    #there is at least one example
    result = examples[0][16]
    length = len(examples)
    for i in range(1, length):
        if(examples[i][16]!=result):
            return None
    return result

def sortByIth(elem):
    global index
    return elem[index]

def classify(examples, attribute, threshold):
    length = len(examples)
    a=attribute
    p=[]
    n=[]
    for i in range(0, length):
        if(examples[i][a]<threshold):
            p.append(examples[i])
        else:
            n.append(examples[i])
    return [p,n]

def count(examples, attribute, threshold, binary):
    #< if binary=1, > if binary =2, count full examples if binary = 3
    #return a pair[numOfTrue, numOfFalse]
    length = len(examples)
    a = attribute
    P = 0
    N = 0
    for i in range(0, length):
        if(binary==1):
            if(examples[i][a]<threshold):

                if(examples[i][16]=="colic."):
                    P+=1
                else:
                    N+=1
        elif(binary==2):
            if(examples[i][a]>threshold):
                if(examples[i][16]=="colic."):
                    P+=1
                else:
                    N+=1
        elif(binary==3):
            if(examples[i][16]=="colic."):
                P+=1
            else:
                N+=1
    return [P, N]

def chooseAttribute(examples):
    #return [attribute, threshold] pair or None if
    global index
    max = 0
    attribute = -1
    threshold = -1
    #length cannot be 1
    length = len(examples)
    #count P and N from full examples
    pair1 = count(examples, -1, -1, 3)
    for i in range(0, 16): #for all 0-15 (16) attributes
        examples.sort(key=sortByIth) #sort examples by the attribute
        index+=1
        if(index==15):
            index=0
        j=0
        while j<(length-1):#for all examples except the last
            next_value = -1
            next_index = -1
            for k in range(j+1, length):
                if(examples[j][i]!=examples[k][i]): #found a different value for attribute
                    if(next_value==-1): #init next value and next index
                        next_value=examples[k][i]
                        next_index = k
                    elif(next_value!=examples[k][i]): #skip if the next value all have the same classification
                        break
                    if(examples[j][16]!=examples[k][16]):
                        #if neighbour example has different value for one attribute
                        #and different classification
                        #there is a possible threshold
                        ##count T and F from given threshold
                        smaller = float(examples[j][i])
                        bigger = float(examples[k][i])
                        possible_threshold = (smaller+bigger)/2
                        pair2 = count(examples, i, possible_threshold, 1) #count P and N for lesser parts of the examples
                        pair3 = count(examples, i, possible_threshold, 2) #count P and N from larger parts of the examples
                        gain = infoGain(pair1[0],pair1[1], pair2[0],pair2[1], pair3[0],pair3[1])
                        if(gain>max):
                            max = gain
                            attribute = i
                            threshold = possible_threshold
                        j=next_index-1
                        break
            j+=1
    result = [attribute, threshold]
    if(attribute==-1):
        result = None
    return result

def induceTree(examples):
    #if no examples is left, return None parent should catch and assign majority vote
    if(examples==[]):
        node = Node(None, None, None, None, None)
        return node
    #if all examples are the same, return a leaf node with that decision
    result = isSame(examples)
    if(result!=None):
        node = Node(None, None, result, None, None)
        return node

    chosen_pair = chooseAttribute(examples)
    if(chosen_pair==None):
        #no attribute is available
        #return majority vote
        pn_pair = count(examples, -1, -1, 3)
        if(pn_pair[0]>pn_pair[1]):
            node = Node(None, None, "colic.", None, None)
        else:
            node = Node(None, None, "healthy.", None, None)
        return node
    else:
        node = Node(None, None, None, None, None)

        classified = classify(examples, chosen_pair[0], chosen_pair[1])
        #left side
        left_node = induceTree(classified[0])
        left_node.parent = node
        if((left_node.values==None) and (left_node.attr_pair==None)): ##left child ask for majority vote
            pn_pair = count(examples, -1, -1, 3)
            if(pn_pair[0]>pn_pair[1]):
                left_node.values = "colic."
            else:
                left_node.values = "healthy."
        #right side
        right_node = induceTree(classified[1])
        right_node.parent = node
        if((right_node.values==None)and (right_node.attr_pair==None)): ##right child ask for majority vote
            pn_pair = count(examples, -1, -1, 3)
            if(pn_pair[0]>pn_pair[1]):
                right_node.values = "colic."
            else:
                right_node.values = "healthy."
        node.left  = left_node
        node.right  = right_node
        node.attr_pair = chosen_pair
        return node

def draw(node, num):
    space='    '
    print(num*space+str([node.attr_pair, node.values, node.left, node.right]))
    if(node.left!=None):
        draw(node.left, num+1)
    if(node.right!=None):
        draw(node.right, num+1)

if __name__ == '__main__':
    #####
    #####
    ##construct decision tree
    #####
    #####
    index = 0
    file = open("horseTrain.txt", 'r')
    num = 0
    list = [] #training list
    line = file.readline()
    while(line):
        num+=1
        innerList = []
        if(len(line) != 0):
            for j in range(0,17):
                if(j==16):
                    innerList.append(line.split(",")[j].split(".")[0]+".")
                else:
                    innerList.append(float(line.split(",")[j]))

            list.append(innerList)
        line = file.readline()
    root = induceTree(list)
    #####
    #####
    ##make classification
    #####
    #####
    file = open("horseTrain.txt", 'r')
    num = 0
    list2 = [] #testing list
    line = file.readline()
    while(line):
        num+=1
        innerList = []
        if(len(line) != 0):
            for j in range(0,17):
                if(j==16):
                    innerList.append(line.split(",")[j].split(".")[0]+".")
                else:
                    innerList.append(float(line.split(",")[j]))

            list2.append(innerList)
        line = file.readline()
    length = len(list2)
    correct = 0
    wrong = 0
    ##walk each examples through the decision tree classifier
    for i in range(0, length):
        node = root
        while(node.values==None): #not leave
            #print(i)
            a = node.attr_pair[0] #attribute
            t = node.attr_pair[1] #threshold
            if(list2[i][a] < t):
                node = node.left
            else:
                node = node.right
        if(node.values==list2[i][16]):
            correct += 1
        else:
            wrong += 1

    print("num of correct: "+str(correct))
    print("num of wrong: "+str(wrong))
    print("The rate of correction is: " + str(float(correct)/length))

    #####
    #####
    ##draw tree FOR UNDERSTANDING PURPOSE, THE SUBMITTED GRAPH IS MANUALLY DRAWN
    #####
    #####
    draw(root, 0)
