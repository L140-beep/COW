from commands import Instructions
from interpreter import Interpreter

inter = Interpreter(50)

# print(inter.buffer.memory)

file = open("files/fib.cow")


text = file.read()


commands = text.split()
file.close()

# print(commands[129])

inter.execute(commands)
