class RingBufferException(Exception):
    ...

class RingBuffer:
    def __init__(self, memorySize : int) -> None:
        if(not isinstance(memorySize, int)):
            raise RingBufferException(f"Invalid RingBuffer memorySize, expect int, given {type(memorySize)}")
        
        if(memorySize <= 0):
            raise RingBufferException(f"Memory size < 0")
            
        self.memorySize = memorySize

        self.memory = [0 for i in range(0, memorySize)]
        
        self.currentCell = 0

    def next(self) -> None:
        if self.currentCell == self.memorySize:
            self.currentCell = 0
        else:
            self.currentCell += 1
    
    def forward(self) -> None:
        if(self.currentCell == 0):
            self.currentCell = self.memorySize
        else:
            self.currentCell -= 1
        
    
    def set(self, value) -> None:
        self.memory[self.currentCell] = value
    
    def get(self):
        return self.memory[self.currentCell]