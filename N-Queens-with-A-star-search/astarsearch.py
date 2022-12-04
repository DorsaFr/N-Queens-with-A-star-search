# import the numpy library
import numpy as np


#We implement Node class to have the g, h and f scores for each node
class Node():
    #to initialize the Node class, we need the __init__ method
    def __init__(self,g,h, state):
        self.g = g
        self.h = h
        self.state = state
        self.f = g + h
        
#the n_quuen class implementation        
class n_Queen():
    
    #initialize the n_queen class
    def __init__(self, n, init_state):
        self.n = n
        self.init_state = init_state 
    
    #this method return the index of each queen on the board in each state 
    def queen_index(self, state):
        index = []
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == 1:    #the 1s in the list would show the index of the queens on board 
                    index.append((i,j))    #we will return these indexes as a list of tuples
        return index
    
    #the actions method will generate the children by doing all the possible moves for a queen in a row
    def actions(self,state,g):
        children = []
        q_index = self.queen_index(state)   #calling the queen_index method to have the positions of the queens at the current state
        for index in q_index:
            q_i = index[0]  # index 0 is the i of the tuples 
            q_j = index[1]  # index 1 is the j of the tuples 
            state[q_i][q_j] = 0     # we make each position 0 and put 1s in the row and repeat this till we have all the possible states 
            for j in range(self.n):
                if j!= q_j:
                    state[q_i][j] = 1
                    children.append(Node(g,self.heuristic_function(np.copy(state)),np.copy(state)))     # we append each made state as a child in the children list 
                    state[q_i][j] = 0
            state[q_i][q_j] = 1 # we need to return to the main state, before changing the position of the queens of the next row
                
        return children
       
     
    def heuristic_function(self,state):
        attacks = 0     # counter of the threats for each queen
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j]==1:  #find the queen
                    q_i = i
                    q_j = j
                    temp_i = i + 1
                    temp_j = j + 1
                    temp_diagon_i = i - 1
                    temp_diagon_j = j - 1
                    
                    for t in range(self.n): # find the threats in the same column of a queen
                        if state[t][q_j] == 1 and q_i != t:
                            attacks +=1    # counting the thread 
    
                    while temp_i < self.n and temp_j < self.n:  # count the threats at the main diagon after the queen
                        if state[temp_i][temp_j] == 1:
                            attacks+=1
                        temp_i += 1
                        temp_j += 1
                    
                    # set the temp_i and temp_j as before, for futher use in other loops
                    temp_i = i + 1
                    temp_j = j + 1
                    
                    while temp_diagon_i >= 0 and temp_diagon_j >= 0:    # count the threats at the main diagon before the queen
                        if state[temp_diagon_i][temp_diagon_j] == 1:
                            attacks += 1 
                        temp_diagon_i -= 1
                        temp_diagon_j -= 1
                    
                    # set the temp_diagon_ i and temp_diagon_j as before 
                    temp_diagon_i = i - 1
                    temp_diagon_j = j - 1
                    
                    while temp_i < self.n and temp_diagon_j >= 0:   # count the threats at the other diagon of the queen, after it
                        if state[temp_i][temp_diagon_j] == 1:
                            attacks += 1
                        temp_i += 1
                        temp_diagon_j -= 1
                    
                    # set them as before 
                    temp_diagon_j = j - 1
                    temp_i = i + 1
                    
                    while temp_j < self.n and temp_diagon_i >= 0: # count the threats at the other diagon of the queen, before it 
                        if state[temp_diagon_i][temp_j] == 1:
                            attacks += 1
                        temp_diagon_i -= 1
                        temp_j += 1
                    
                    # set them as before 
                    temp_diagon_i = i - 1
                    temp_j = j + 1
        
        return attacks/2    # we can return attacks too, without dividing by two. the two algorithms have the same logic 
    

    
    # check whether we find the goal
    def is_it_goal(self,state):
        if self.heuristic_function(np.copy(state)) == 0: # if there are no threats left, we've reached the goal
            return True
        else: # otherwise we haven't 
            return False
    
    def update(self, child, frontier):  
        for i in range(len(frontier)):
            if sum(sum(child.state == frontier[i].state)) == self.n**2 and frontier[i].f >= child.f:    # check whether the child state is the same as the frontier and compare their f scores 
                frontier[i].f = child.f # if the child state has lower f score, we replace them 
                
    def is_it_in_frontier(self, state, frontier):
        for node in frontier:
            if sum(sum(node.state == state)) == self.n**2: # check if the given state is in the frontier or not, the sum will count the true instances 
                return True
        return False
    
    def is_it_in_explored(self, state, explored):
        for node in explored:
            if sum(sum(node.state == state)) == self.n**2: # check if the given state is explored before 
                return True
        return False

    # based on the pseudo code in the book  
    def a_star_search(self):
        explored = []
        frontier = []
        
        # set h, make the first root node, and append the node as the frontier for now 
        # we pass the copy of the state to methods each time to ensure there would be not an unwanted changes throughout the program
        h = self.heuristic_function(np.copy(self.init_state))   
        node = Node(0, h,np.copy(self.init_state))
        frontier.append(node)
        
        while len(frontier) != 0:   # till the list is not empty 
            frontier.sort(key= lambda x: x.f) # the list would be sorted by f, from the least to the most (priority queue)
            node = frontier.pop(0)      # pop the frontier, as we have sorted before, it would have the least f score 
            print(node.state, node.h)   # to check the process
            print("-----------------")
            
            if self.is_it_goal(np.copy(node.state)): # if we reach the goal we must stop 
                print("Solution is found: ")
                print(node.state)   # print the goal state
                return
            
            explored.append(node)   # we add the popped node to the explored list 
            state = np.copy(node.state)
            children = self.actions(np.copy(node.state), node.g + 1)    # we generate the children
            
            for child in children:
                if not self.is_it_in_frontier(child.state, frontier) and not self.is_it_in_explored(child.state, explored):     #   if the child is not in the frontier nor the explored list
                    frontier.append(child)  # add to the frontier
                elif self.is_it_in_explored(child.state, explored):     # if the child state has been explored before (it is already in the explored list)
                    self.update(child,frontier) # we call the method to compare the child and frontier f scores and make the necessary updates to the list
                    
            
                    
# an example of an initial state and n = 8 
state = [[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]]
n = 8
nq = n_Queen(n, state)
nq.a_star_search()



    
    
                        