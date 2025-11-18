class Node:
    def __init__(self, pData=None):
        self.data = pData
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def IsEmpty(self) -> bool:
        return self.front is None

    def Enqueue(self, data) -> None:
        newNode = Node(data)
        newNode.next = None

        if (self.rear is None):
            self.front = self.rear = newNode
            return
        
        self.rear.next = newNode
        self.rear = newNode

    def Dequeue(self) -> any:
        if self.IsEmpty():
            return None
        
        curFront = self.front
        self.front = self.front.next

        if (self.front is None):
            self.rear = None

        return curFront.data

    def Peek(self) -> any:
        if self.IsEmpty():
            return None
        
        return self.front.data
    
    def PeekAt(self, pIndex: int) -> any:
        if (self.IsEmpty()):
            return None
        
        currentNode = self.front
        currentIndex = 0

        while (currentNode is not None):
            if (currentIndex == pIndex):
                return currentNode.data
            
            currentNode = currentNode.next
            currentIndex += 1

        return None
    
    def Size(self) -> int:
        currentNode = self.front
        size = 0

        while (currentNode is not None):
            size += 1
            currentNode = currentNode.next

        return size