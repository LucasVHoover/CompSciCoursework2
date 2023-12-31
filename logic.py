#DATA FORMAT ["name (input by user)", "duration  (input by user)", "immediate Predecessors (input by user)",  "immediate successors", EST, LFT, Height]
#tree = [['A',7, [], [], None, None, 0],
        #['B', 6, [], [], None, None, 0],
        #['C',  15, [],[], None, None,0],
        #['D',  9, ['A', 'B'],[], None, None,0],
        #['E',  8, ['D'],[], None, None,0],
        #['F', 6, ['C', 'D'],[], None, None, 0],
        #['G',  7, ['C'],[], None, None,0],
        #['H',  14, ['E'],[], None, None,0],
       # ['I',  17, ['F', 'G'],[], None, None,0],
       # ['J',  9, ['H','I'],[], None, None,0],
       # ['K',  8, ['I'],[], None, None,0],
       # ['L',  12, ['J', 'K'],[], None, None,0]]

#add total predecessors value

#go along path of sucession until a you have a point where on predecesor is unresolved. then you turn back

def Immediate_Successors(tree):
    for node in tree:
        for i in range(len(tree)):
            for predecessors in tree[i][2]:
                if node[0] == predecessors:
                    node[3].append(tree[i][0])
    return tree

def StartEnd_Nodes(tree):
    start_node = ['START', 0, [], [], 0, None, 1, 0]
    end_node = ['END', 0, [], [], None, None, 0, 0]
    for node in tree:
        if node[2] == []:
            node[2].append('START')
            start_node[3].append(node[0])
        if node[3] == []:
            node[3].append('END')
            end_node[2].append(node[0])

    tree.append(start_node)
    tree.append(end_node)

    return tree

def height(tree, level):
    sucessors = []
    for node in tree:
        if node[6] == level:
            for each in node[3]:
                sucessors.append(each)
    if sucessors == []:
        print("height completed")
    else:
        for node in tree:
            if node[0] in sucessors:
                if node[6] <= (level):
                    node[6] = level + 1
        height(tree, level+1)
    return tree

def maxheights(tree):
    heights = []
    for node in tree:
        heights.append(node[6])
    return max(heights)
  
def forwardPass(tree, level, maxheight):
    for examinednode in tree:
        predecessors = []
        Largest = []
        if examinednode[6] == level:
            for each in examinednode[2]:
                predecessors.append(each)
            for node in tree:
                if node[0] in predecessors:
                    Largest.append(node[4] + node[1])
            examinednode[4] = max(Largest)
        else:
            pass
    if level <= maxheight:
        forwardPass(tree, level+1, maxheight)
    else:
        print("finished")

    return tree

def LFT_EndNode(tree, maxheight):
    for node in tree:
        if node[6] == maxheight:
            node[5] = node[4] + node[1]
    return tree

def backwardPass(tree, level):
    for examinednode in tree:
        sucessors = []
        Smallest = []
        if examinednode[6] == level:
            for each in examinednode[3]:
                sucessors.append(each)
            for node in tree:
                if node[0] in sucessors:
                    Smallest.append(node[5] - node[1])
            examinednode[5] = min(Smallest)
        else:
            pass
    if level == 0:
        pass
        #print("finished")
    else:
        backwardPass(tree, level-1)

    return tree

def criticalPathTree(tree):
    CPtree = tree
    for node in CPtree:
        if (node[1] + node[4]) != node[5]:
            CPtree.remove(node)
    return CPtree

def StripStartEnd(tree):
    tree = filter(lambda item: not(item[0] == "START" or item[0] == "END"), tree)
    #print("output should be: ", list(tree))
    return list(tree)



#NON FUNCTIONAL

def identifyCriticalPaths(tree, position): 
    for node in tree:
        if node[0] == position:
            print(node[0])
            print(node[3])
            if node[3] == []:
                print("end")
            else:
                for each in node[3]:
                    identifyCriticalPaths(tree, each)
    return tree

def CPA(tree):
  tree = Immediate_Successors(tree)
  tree = StartEnd_Nodes(tree)
  tree = height(tree, 1)
  maxheight = maxheights(tree)
  tree = forwardPass(tree, 2, maxheight)
  tree = LFT_EndNode(tree, maxheight)
  tree = backwardPass(tree, maxheight-1)
  #tree = StripStartEnd(tree)
  return tree, maxheight

#THIS NEEDS DOING
def VerifyNoError(tree):
    pass

