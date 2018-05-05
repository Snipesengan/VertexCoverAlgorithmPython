class Heap:
    """A class for a heap"""

    def __init__(self, type, get_key_callback):

        #check if *callback is a a function callback
        if not hasattr(get_key_callback, '__call__'):
            raise TypeError

        #check if type is valid
        if isinstance(type, str) and (type.lower() == "min" or type.lower() == "max"):
            self.heap_type = type
            self.callback = get_key_callback
            self.heap = []
        else:
            raise TypeError

    def insert(self, item):
        self.heap.append(item)
        self._trickleUp(len(self.heap) - 1)

    def extract(self, index=0):
        if(index < 0 or index >= len(self.heap)):
            raise IndexError

        value = self.heap[index]
        self.heap[index] = self.heap[len(self.heap) - 1]
        del self.heap[len(self.heap) - 1]
        self._trickleDown(index)

        return value

    def update(self, index):
        if(index < 0 or index >= len(self.heap)):
            raise IndexError

        if (((self.heap_type == "max") and self.callback(self.heap[index], self.heap[int(index/2)])) or
            ((self.heap_type == "min") and self.callback(self.heap[int(index/2)], self.heap[index]))):
                self._trickleUp(index)
        else:
                self._trickleDown(index)

    def isEmpty(self):
        return len(self.heap) == 0

    def _trickleDown(self, index):
        leftIdx = 2 * index + 1
        rightIdx = leftIdx + 1
        swapIdx = index;
        if leftIdx < len(self.heap):
            if (((self.callback(self.heap[leftIdx] ,self.heap[swapIdx])) and self.heap_type == "max") or
                ((self.callback(self.heap[swapIdx], self.heap[leftIdx])) and self.heap_type == "min")):
               swapIdx = leftIdx

        if rightIdx < len(self.heap):
            if (((self.callback(self.heap[rightIdx] , self.heap[swapIdx])) and self.heap_type == "max") or
                ((self.callback(self.heap[swapIdx] , self.heap[rightIdx])) and self.heap_type == "min")):
               swapIdx = rightIdx

        if swapIdx != index:
            self.heap[index],self.heap[swapIdx] = self.heap[swapIdx],self.heap[index]
            self._trickleDown(swapIdx)

    def _trickleUp(self, index):

        if (index >= 0) and (index < len(self.heap)):
            while (index > 0 and (((self.heap_type == "min") and self.callback(self.heap[int(index/2)], self.heap[index])) or
                                  ((self.heap_type == "max") and self.callback(self.heap[index], self.heap[int(index/2)])))):
                self.heap[int(index/2)],self.heap[index] = self.heap[index],self.heap[int(index/2)]
                index = int(index/2)

    def __str__(self):
        str = [i.__str__() for i in self.heap]
        return "[" + ','.join(str) + "]"

def main():
    #testing
    intArr = [4,1,3,2,9,16,10,14,8,7]
    heap = Heap("max", lambda x: x)
    for i in intArr:
        heap.insert(i)

    print(heap)
    print(heap.extract(2))
    print(heap)
    print(heap.extract())
    print(heap)


if __name__ == "__main__":
    main()
