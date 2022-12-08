from RingBuffer import RingBuffer
from commands import Instructions 
class InterpreterException(Exception):
    ...

class Interpreter:
    def __init__(self, memorySize : int) -> None:
        self.buffer = RingBuffer(memorySize)
        self.cycles = []
        self.current_instruction = 0
    
    def prepare(self, program) -> list:
        prepared = program.copy()
        
        i = 0
        
        for command in program:
            if command not in Instructions.instructions.value:
                prepared.pop(i)
            else:
                i +=1     
        
        return prepared
    
    def execute(self, program):
        
        program = self.prepare(program)
        self.findCycles(program)
        
        while self.current_instruction < len(program):
            self.eval(program[self.current_instruction])
            self.current_instruction += 1
            
    def findCycles(self, program : list):
        
        t_program = program.copy()
        
        while 'MOO' in t_program and 'moo' in t_program:
            current_instruction = 0
            start = 0
            
            while True:
                match t_program[current_instruction]:
                    case 'MOO':
                        start = current_instruction
                    case 'moo':
                        self.cycles.append(start)
                        self.cycles.append(current_instruction)
                        t_program[start] = "-1"
                        t_program[current_instruction] = "-1"                        
                        break

                current_instruction += 1           
                    
        if 'moo' in t_program:
           raise InterpreterException("Unexpected moo") 
        if 'MOO' in t_program:
              raise InterpreterException("Unexpected MOO")   
        
    def eval(self, command:str):
            match(command):
                case 'MoO':
                    value = self.buffer.get() + 1
                    self.buffer.set(value)                    
                
                case 'MOo':
                    value = self.buffer.get() - 1
                    self.buffer.set(value) 
                
                case 'moO':
                    self.buffer.next() 
                
                case 'mOo': 
                    self.buffer.forward()
                        
                case 'OOM':
                    print(self.buffer.get(), end='')
                    
                case 'oom': 
                    self.buffer.set(int(input()))
                
                case 'mOO':    
                    c = self.buffer.get()
                    if(c != 8 and c < len(Instructions.instructions.value)):
                        self.eval(c)
                    else:
                        exit(-1)
                        
                case 'Moo':
                    value = self.buffer.get()
                    if (value):
                        print(chr(value), end='')
                    else:
                        self.buffer.set(input(int))
                
                case 'OOO': 
                    self.buffer.set(0)
                    
                case 'moo': 
                    pos = self.cycles.index(self.current_instruction) - 1
                    self.current_instruction = self.cycles[pos] - 1
                    
                case 'MOO':
                    if self.buffer.get() == 0:
                        pos = self.cycles.index(self.current_instruction) + 1
                        self.current_instruction = self.cycles[pos] 
                case _:
                    raise InterpreterException(f"SyntaxError in command {command}")
            