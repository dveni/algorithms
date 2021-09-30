""" 
You have three buckets:
- Bucket A, 8 litres
- Bucket B, 5 litres
- Bucket C, 3 litres
Bucket A is full, while buckets B and C are empty. As result, you need to have 4 litres in bucket
A and 4 litres in bucket B by emptying or filling entirely with each other.
Implement an algorithm in C/C++ that finds a solution to the problem and display as output the
sequence of pourings identified by the algorithm itself.
Please note:
The buckets have no scale, so it is not possible to pour a precise amount of water (es: a pouring
of 1 litre).
A given pouring:
- Will completely empty the starting bucket if the destination bucket has enough capacity
left
- Will partially empty the starting bucket (until the destination bucket is full), if the
destination bucket doesn’t have enough capacity to accept the entire content of the
starting bucket 
"""
PARENT_NODE = 0
EXPLORED_NODE = 1
NODE_ID = 2

class State:
    def __init__(self, bucketA, bucketB, bucketC) -> None:
        self.bucketA = bucketA
        self.bucketB = bucketB
        self.bucketC = bucketC
        if not isValidState(self):
            raise ValueError('All initial volumes must be less than the maximun volumes')
    def getBuckets(self):
        return (self.bucketA, self.bucketB, self.bucketC)
    def getBucketsLevels(self):
        return (self.bucketA.level, self.bucketB.level, self.bucketC.level)
    def numOfBuckets(self):
        return len(self.getBuckets())
    def __str__(self) -> str:
        return f"{self.bucketA} | {self.bucketB} | {self.bucketC}"

class Bucket:
    def __init__(self, name, capacity, level) -> None:
        self.name = name
        self.capacity = capacity
        self.level = level
    def __str__(self) -> str:
        #return f"{self.name}. Capacity: {self.capacity}. Level: {self.level}"
        return f"{self.level}"



def generatePossibleStates(initialState):
    """
    O(n*(n-1)) -> n=3 buckets
    """
    possibleStates = []

    for i in range(initialState.numOfBuckets()):
        for j in range(1, initialState.numOfBuckets()):
            newState = copyState(initialState)
            buckets = newState.getBuckets()
            if canGive(buckets[i]):
                pourWater(buckets[i],buckets[(i+j)%3])
                if isValidState(newState):
                    possibleStates.append(newState)
    
    return possibleStates

def pourWater(b1, b2):
    """
    O(1)
    """
    # Pour water from bucket b1 into bucket b2

    # Test both objects are buckets
    # Test edge cases
    if b1.level == 0: return b1, b2
    
    freeRoomB2 = max(b2.capacity - b2.level,0)
    
    if b1.level > freeRoomB2:
        b1.level -= freeRoomB2
        b2.level += freeRoomB2
    else:
        b2.level += b1.level 
        b1.level = 0
    return b1,b2

def copyState(state):
    bA = Bucket(state.bucketA.name, state.bucketA.capacity, state.bucketA.level)
    bB = Bucket(state.bucketB.name, state.bucketB.capacity, state.bucketB.level)
    bC = Bucket(state.bucketC.name, state.bucketC.capacity, state.bucketC.level)

    return State(bA,bB,bC)

def canGive(bucket):
    return bucket.level > 0

def isValidState(state):
    return not(state.bucketA.level > state.bucketA.capacity or
     state.bucketB.level > state.bucketB.capacity or state.bucketC.level > state.bucketC.capacity)

 
def compareStates(stateA, stateB):
    """
    O(1)
    """
    return hash(stateA.getBucketsLevels()) == hash(stateB.getBucketsLevels())

def getUnexploredNodes(table):
    """
    O(n) n -> #nodes in table
    """
    unexplored = [item for item in table if not table[item][EXPLORED_NODE]]
    return unexplored

def stateExist(state, table, nodes):
    """
    O(1)
    See https://stackoverflow.com/questions/17539367/python-dictionary-keys-in-complexity
    """
    return hash(state.getBucketsLevels()) in table



def getGoalStatePath(initialState, goalState):
    """
    O(n^3)
    statesUntilGoalState * unexploredNodes * possibleStates
    For this problem, max = 8*3*5 = 120
    """
    hashTable = {hash(initialState.getBucketsLevels()): ["root", False, 0]}
    nodes = [initialState]
    stateFound = False
    i = 1
    
    while not stateFound:
        # O(n)
        unexploredNodes = getUnexploredNodes(hashTable)
        if len(unexploredNodes) < 1:
            print("Goal state not possible")
            break
        """
        O(n^2) 
        unexploredNodes * possibleStates
        Typically, there are between 2-3 unexplored nodes
        """
        for nodeId in unexploredNodes:

            # O(n*(n-1)) n -> #buckets
            states = generatePossibleStates(nodes[hashTable[nodeId][NODE_ID]])
            hashTable[nodeId][EXPLORED_NODE] = True
            # O(n) n-> #possible states (empirically, max 5)
            for state in states:
                # O(n)
                if stateExist(state, hashTable,nodes): continue
                # O(1)
                stateFound = compareStates(state, goalState)
                hashTable[hash(state.getBucketsLevels())] = [nodeId, False, i]
                i+=1
                nodes.append(state)
                #print(state)
                if stateFound: break
            if stateFound: break

    if stateFound:
        previousNode = hashTable[hash(goalState.getBucketsLevels())][PARENT_NODE]
        path=[nodes[-1]]
        while previousNode != "root":
            path.append(nodes[hashTable[previousNode][NODE_ID]])
            previousNode = hashTable[previousNode][PARENT_NODE]

        for node in path[::-1]:
            print(node)

if __name__== "__main__":
    
    bA = Bucket("Bucket A", 8, 8)
    bB = Bucket("Bucket B", 5, 0)
    bC = Bucket("Bucket C", 3, 0)
    initialState = State(bA, bB, bC)
    
    goalA = Bucket("Bucket A", 8, 4)
    goalB = Bucket("Bucket B", 5, 4)
    goalC = Bucket("Bucket C", 3, 0)
    goalState = State(goalA, goalB, goalC)

    getGoalStatePath(initialState, goalState)
    




# I suppose every node has only one parent,
# althoug much of the nodes can be reacher from multiple paths so we do not find the most short, just a path

# Assume there are finite states

# Only 3 buckets