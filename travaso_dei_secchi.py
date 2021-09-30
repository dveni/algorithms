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

class State:
    def __init__(self, bucketA, bucketB, bucketC) -> None:
        self.bucketA = bucketA
        self.bucketB = bucketB
        self.bucketC = bucketC
        if not isValidState(self):
            raise ValueError('All initial volumes must be less than the maximun volumes')
    def getBuckets(self):
        return (self.bucketA, self.bucketB, self.bucketC)
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
    stateABuckets = stateA.getBuckets()
    stateBBuckets = stateB.getBuckets()
    same = True
    for bucketA, bucketB in zip(stateABuckets,stateBBuckets):
        if bucketA.level != bucketB.level:
            same = False
    return same

def allNodesExplored(table):
    bools = [item[1] for item in table.values()]
    return all(bools)

if __name__== "__main__":
    
    bA = Bucket("Bucket A", 8, 8)
    bB = Bucket("Bucket B", 5, 0)
    bC = Bucket("Bucket C", 3, 0)
    initialState = State(bA, bB, bC)
    
    goalA = Bucket("Bucket A", 8, 4)
    goalB = Bucket("Bucket B", 5, 2)
    goalC = Bucket("Bucket C", 3, 3)
    goalState = State(goalA, goalB, goalC)


    hashTable = {0: ["root", False]}
    nodes = [initialState]
    stateFound = False
    i = 1
    while not stateFound:
        if allNodesExplored(hashTable):
            print("State not possible")
            break
        for nodeId in list(hashTable):
            if not hashTable[nodeId][1]:
                states = generatePossibleStates(nodes[nodeId])
                hashTable[nodeId][1] = True
                for state in states:
                    
                    stateExist = False
                    for key in hashTable.keys():
                        if compareStates(state, nodes[key]):
                            stateExist = True
                            break  
                    if stateExist: continue

                    stateFound = compareStates(state, goalState)
                    #print(state)
                    hashTable[i] = [nodeId, False]
                    i+=1
                    nodes.append(state)
                    if stateFound: break
                if stateFound: break

if stateFound:
    previosNode = hashTable[len(nodes)-1][0]
    path=[nodes[-1]]
    while previosNode != "root":
        path.append(nodes[previosNode])
        previosNode = hashTable[previosNode][0]

    for node in path[::-1]:
        print(node)




# I suppose every node has only one parent,
# althoug much of the nodes can be reacher from multiple paths so we do not find the most short, just a path

# Assume there are finite states