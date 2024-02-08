#DATA FORMAT ["name (input by user)", "duration  (input by user)", "immediate Predecessors (input by user)",  "immediate successors", EST, LFT, Height]
#tree = [['A',7, [], [], None, None, 0],
#        ['B', 6, [], [], None, None, 0],
#        ['C',  15, ['B'],[], None, None,0],
#        ['D',  9, ['B'],[], None, None,0],
#        ['E',  8, ['C'],[], None, None,0],
#        ['F', 6, ['A', 'E'],[], None, None, 0],
#        ['G',  7, ['F'],[], None, None,0],
#        ['H',  14, ['G','D'],[], None, None,0]]

#finds the successors for each task
def Immediate_Successors(tree):
  #loops through tree
    for node in tree:
      #finds the successors
        for i in range(len(tree)):
            for predecessors in tree[i][2]:
                if node[0] == predecessors:
                  #adds them to each task
                    node[3].append(tree[i][0])
    return tree

#adds start and end nodes
def StartEnd_Nodes(tree):
  #defines the start and end nodes
    start_node = ['START', 0, [], [], 0, None, 1, 0]
    end_node = ['END', 0, [], [], None, None, 0, 0]
  #finds the first and last nodes and gives them the start and end node
    for node in tree:
        if node[2] == []:
            node[2].append('START')
            start_node[3].append(node[0])
        if node[3] == []:
            node[3].append('END')
            end_node[2].append(node[0])
  #adds the start and end nodes
    tree.append(start_node)
    tree.append(end_node)

    return tree

#gives each task a height
def height(tree, level):
  #creates a list of successors
    sucessors = []
  #finds all the successors 
    for node in tree:
        if node[6] == level:
            for each in node[3]:
                sucessors.append(each)
  #break condition if the last task is reached
    if sucessors == []:
        print("height completed")
    else:
      #sets the height for all nodes in the successors array
        for node in tree:
            if node[0] in sucessors:
                if node[6] <= (level):
                    node[6] = level + 1
      #iterates to the next height
        height(tree, level+1)
    return tree

#finds the biggest height in the tree
def maxheights(tree):
    heights = []
    for node in tree:
        heights.append(node[6])
    return max(heights)

#performs the forward pass of the CPA algorithm
def forwardPass(tree, level, maxheight):
  #loops through each node
    for examinednode in tree:
      #sets empty "predecessor" and "largest" arrays
        predecessors = []
        Largest = []
      #checks if the node is at the right height
        if examinednode[6] == level:
          #adds the predecessors to the array
            for each in examinednode[2]:
                predecessors.append(each)
          #calculates the EST for all predecessors and adds to "Largest"
            for node in tree:
                if node[0] in predecessors:
                    Largest.append(node[4] + node[1])
          #picks the largest in "largest" to be the EST
            examinednode[4] = max(Largest)
        else:
            pass
          #break condition
    if level <= maxheight:
      #iterates to the next height
        forwardPass(tree, level+1, maxheight)
    else:
        print("finished")

    return tree

#calculates the LFT of the final task
def LFT_EndNode(tree, maxheight):
    for node in tree:
        if node[6] == maxheight:
            node[5] = node[4] + node[1]
    return tree

#performs the backward pass of the CPA algorithm
def backwardPass(tree, level):
  #loops through the tree
    for examinednode in tree:
      #sets the empty "successors" and "smallest" arrays
        sucessors = []
        Smallest = []
      #checks each task is at the examined node
        if examinednode[6] == level:
          #adds the successors to the array
            for each in examinednode[3]:
                sucessors.append(each)
          #adds the LFT of each successor to the array
            for node in tree:
                if node[0] in sucessors:
                    Smallest.append(node[5] - node[1])
          #sets the LFT to the smallest in the "smallest" array
            examinednode[5] = min(Smallest)
        else:
            pass
          #break condition
    if level == 0:
        pass
        print("finished")
    else:
      #iterates to the next height
        backwardPass(tree, level-1)

    return tree

#finds the critical path tree
def criticalPathTree(tree):
    CPtree = tree
    for node in CPtree:
        if (node[1] + node[4]) != node[5]:
            CPtree.remove(node)
    return CPtree

#removes the start and end tasks
def StripStartEnd(tree):
    tree = filter(lambda item: not(item[0] == "START" or item[0] == "END"), tree)
    return list(tree)

#runs each part of the CPA algorithm in sequence and returns the finished tree and maxheight
def CPA(tree):
  tree = Immediate_Successors(tree)
  tree = StartEnd_Nodes(tree)
  tree = height(tree, 1)
  maxheight = maxheights(tree)
  tree = forwardPass(tree, 2, maxheight)
  tree = LFT_EndNode(tree, maxheight)
  tree = backwardPass(tree, maxheight-1)
  tree = StripStartEnd(tree)
  return tree, maxheight

#THIS NEEDS DOING
def VerifyNoError(tree):
    pass

#output = CPA(tree)

#for each in output:
#    print(each)