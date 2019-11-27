# For Virtual Machine creation
#
# @author: Emilio López Hernández
#
# A01651283
#
# Delivery date: 27/11/2019 
#
#

import json
import sys
from memory import Memory
from turtle import Turtle, Screen, Shape

class VirtualMachine:
    def __init__(self):

        self.programa = None
        self.memory = Memory()
        
        self.pointer = None
        self.screen = None
        self.turtle_activa = False

        self.contextStack = []

    ## This function receives quadruple files and the function and constants directory
    ## program -> name of the compiled program
    def getData(self,program):
        compilado = f"test/{program}_compiled.fig"
        arch_compilado = open(compilado, 'r')
        todito = json.load(arch_compilado)
        
        self.contextStack.append('mainF')
        self.programa = program

        self.haz_constantes(todito['tConstantes'])
        self.haz_quads(todito['Quads'],todito['FunDir'])

    ## This function process each quad until finds END
    ## quads -> list of quads, fun_dir -> function directory
    def haz_quads(self,quads,fun_dir,sig=0):
        parametros = []
        retornado = None

        while True:            
            operador = quads[sig][0]
            op_izq = quads[sig][1]
            op_der = quads[sig][2]
            res = quads[sig][3]

            # verify if contain () and get value
            if isinstance(op_izq,str) and op_izq[0] == '(':
                op_izq = self.dame_contenido(op_izq)
            if isinstance(op_der,str) and op_der[0] == '(': 
                op_der = self.dame_contenido(op_der)
            if isinstance(res,str) and res[0] == '(':
                res = self.dame_contenido(res)

            if operador == '=':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                tipo_res = self.dame_tipo(res)
                
                mem_r[res] = tipo_res(mem1[op_izq])
                sig += 1

            elif operador == '+':

                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                
                # Sum of string with something else
                if(isinstance(mem1[op_izq], str) and not isinstance(mem2[op_der], str)) or (isinstance(mem2[op_der],str) and not isinstance(mem1[op_izq],str)):
                    mem_r[res] = str(mem1[op_izq]) + str(mem2[op_der])
                else:
                    
                    mem_r[res] = mem1[op_izq] + mem2[op_der]
                sig += 1

            elif operador == '-':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                mem_r[res] = mem1[op_izq] - mem2[op_der]
                sig += 1

            elif operador == '*':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                mem_r[res] = mem1[op_izq] * mem2[op_der]
                sig += 1

            elif operador == '/':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                tipo_res = self.dame_tipo(res)

                if mem2[op_der] == 0:
                    raise TypeError(f"Error: Cannot divide by 0")

                mem_r[res] = tipo_res(mem1[op_izq] / mem2[op_der])
                sig += 1

            elif operador == '>':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                mem_r[res] = mem1[op_izq] > mem2[op_der]
                sig +=1

            elif operador == '<':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                
                mem_r[res] = mem1[op_izq] < mem2[op_der]
                sig +=1
            
            elif operador == '>=':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                mem_r[res] = mem1[op_izq] >= mem2[op_der]
                sig +=1

            elif operador == '<=':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                mem_r[res] = mem1[op_izq] <= mem2[op_der]
                sig +=1


            elif operador == '!=':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                mem_r[res] = mem1[op_izq] != mem2[op_der]

                sig +=1

            elif operador == '==':
                mem1, mem2, mem_r = self.dame_memorias(op_izq, op_der, res)
                mem_r[res] = mem1[op_izq] == mem2[op_der]
                
                sig +=1

            elif operador == 'print':
                mem = self.dame_mem(res)
                print(mem[res])
                sig +=1

            elif operador == 'read':
                mem = self.dame_mem(res)
                mem[res] = input()
                sig += 1

            elif operador == 'GotoF':
                # Memory of boolean value
                mem_b = self.dame_mem(op_izq)
                if not mem_b[op_izq]:
                    sig = int(res) - 1
                else:
                    sig += 1
                    
            elif operador == 'GotoV':
                mem_b = self.dame_mem(op_izq)
                if mem_b[op_izq]:
                    sig = int(res) - 1
                else:
                    sig += 1

            elif operador == 'Goto_main' or operador == 'Goto':
                sig = int(res) - 1
                # mainF memory activation

            elif operador == 'END':
                
                self.memory.throat()
                self.contextStack.pop()
    
                break

            elif operador == 'down':
                if not self.turtle_activa:
                    self.activa_tortuga()
                    
                self.pointer.pd()
                sig += 1

            elif operador == 'up':
                if not self.turtle_activa:
                    self.activa_tortuga()
                    
                self.pointer.pu()
                sig += 1

            
            elif operador == 'exit':
                if not self.turtle_activa:
                    self.activa_tortuga()
                    
                self.screen.exitonclick()
                sig += 1
            
            elif operador == 'start_f':
                if not self.turtle_activa:
                    self.activa_tortuga()
                
                self.pointer.begin_fill()
                sig += 1

            elif operador == 'end_f':
                if not self.turtle_activa:
                    self.activa_tortuga()

                self.pointer.end_fill()
                sig += 1


            ## GRAPH 
            elif operador == 'circle':
                mem = self.dame_mem(op_izq)
                if not self.turtle_activa:
                    self.activa_tortuga()
                    
                self.pointer.circle(mem[op_izq])
                sig += 1
            
            elif operador == 'left':
                mem = self.dame_mem(op_izq)
                angle = float(mem[op_izq])
                if not self.turtle_activa:
                    self.activa_tortuga()
                    
                if angle > 360:
                    raise TypeError(f"Value cannot be greater than 360")
                self.pointer.lt(angle)
                sig += 1

            elif operador == 'right':
                mem = self.dame_mem(op_izq)
                angle = float(mem[op_izq])
                if not self.turtle_activa:
                    self.activa_tortuga()
                    
                if angle > 360:
                    raise TypeError(f"Value cannot be greater than 360")
                self.pointer.rt(angle)
                sig += 1
            
            elif operador == 'back':
                mem = self.dame_mem(op_izq)
                if not self.turtle_activa:
                    self.activa_tortuga()
                    
                self.pointer.bk(mem[op_izq])
                sig += 1

            elif operador == 'go':
                mem = self.dame_mem(op_izq)
                if not self.turtle_activa:
                    self.activa_tortuga()
                    
                self.pointer.fd(mem[op_izq])
                sig += 1
            
            elif operador == 'square':
                mem = self.dame_mem(op_izq)

                if not self.turtle_activa:
                    self.activa_tortuga()

                # Graph square
                self.pointer.forward(mem[op_izq])
                self.pointer.left(90) 
                self.pointer.forward(mem[op_izq])
                self.pointer.left(90)
                self.pointer.forward(mem[op_izq])
                self.pointer.left(90)
                self.pointer.forward(mem[op_izq])
                self.pointer.left(90)
                sig += 1
            
            elif operador == 'rectangle':
                mem1 = self.dame_mem(op_izq) # base
                mem2 = self.dame_mem(op_der) # height
                
                base = mem1[op_izq]
                altura = mem2[op_der]

                if not self.turtle_activa:
                    self.activa_tortuga()

                # Graph rectangle
                self.pointer.fd(base)
                self.pointer.lt(90) 
                self.pointer.fd(altura)
                self.pointer.lt(90)
                self.pointer.fd(base)
                self.pointer.lt(90)
                self.pointer.fd(altura)
                self.pointer.lt(90)
                sig += 1

            elif operador == 'triangle':
                mem = self.dame_mem(op_izq)

                if not self.turtle_activa:
                    self.activa_tortuga()

                # Graph equi triangle
                self.pointer.fd(mem[op_izq])
                
                self.pointer.lt(120)
                self.pointer.fd(mem[op_izq])

                self.pointer.lt(120)
                self.pointer.fd(mem[op_izq])

                sig += 1
            
            elif operador == 'speed':
                mem = self.dame_mem(op_izq)

                if not self.turtle_activa:
                    self.activa_tortuga()
                speed = mem[op_izq]
                if self.dame_tipo(op_izq) is not str:
                    if not 1 <= speed <= 10:
                        raise TypeError(f"Speed value between 0 and 10")
                elif speed not in ['fastest','fast','normal','slow','slowest']:
                    raise TypeError(f"{speed} not valid speed")
                self.pointer.speed(mem[op_izq])
                sig += 1
            
            elif operador == 'pointer_color':
                mem = self.dame_mem(op_izq)

                if not self.turtle_activa:
                    self.activa_tortuga()
                color = mem[op_izq]
                self.pointer.color(color)
                sig += 1
            
            elif operador == 'pointer_size':
                mem = self.dame_mem(op_izq)

                if not self.turtle_activa:
                    self.activa_tortuga()
                
                size = mem[op_izq]
                self.pointer.pensize(size)
                sig += 1

           
            elif operador == 'position':
                mem1 = self.dame_mem(op_izq)
                mem2 = self.dame_mem(op_der)

                if not self.turtle_activa:
                    self.activa_tortuga()
                    

                self.pointer.setpos(mem1[op_izq],mem2[op_der])
                sig += 1



            elif operador == 'VER':
                
                mem1 = self.dame_mem(op_izq)
                mem2 = self.dame_mem(op_der)
                if not(0 <= mem1[op_izq] < mem2[op_der]):
                    raise TypeError(f"OUT OF BOUNDS")
                
                sig += 1
            
            
            ## FUNCTIONS 

            elif operador == 'ERA':
                fun = fun_dir[res]
                
                if self.memory.active is not None:
                    superior = self.memory.active
                else:
                    superior = self.memory
                self.memory.recordActivation(superior, fun['vars'])
                sig += 1

            elif operador == 'GOSUB':
                self.memory.active = self.memory.mem_exec[list(self.memory.mem_exec.keys())[-1]]
                
                self.contextStack.append(res)

                self.memory.active.matcheo(parametros)
                parametros.clear()
                val = self.haz_quads(quads, fun_dir, int(res)-1)

                # Return
                if val is not None:
                    mem = self.dame_mem(op_izq)
                    mem[op_izq] = val
                
                sig += 1
                

            elif operador == 'RETURN':
                mem = self.dame_mem(res)
                retornado = mem[res]

                sig += 1
            
            elif operador == 'param':
                mem = self.dame_mem(res)
                parametros.append(mem[res])

                sig += 1
            
            elif operador == 'ENDPROC':
                
                self.memory.throat()
                self.contextStack.pop()

                if retornado is not None:
                    return retornado
                else:
                    break
    

    ## This function generates constants table and charges it to memory
    ## t -> constants table   
    ## GLOBAL
    ## i [1000  -  5999]
    ## f [6000  - 10999]
    ## s [11000 - 15999]
    ## b [16000 - 20999]
    ## LOCAL
    ## i [21000 - 25999]
    ## f [26000 - 30999]
    ## s [31000 - 35999]
    ## b [36000 - 40999]
    ## CONSTANTS
    ## c [41000 - 51999]           
    def haz_constantes(self, t):
        for const in t:
            dir = const[0]
            val = const[1]
            self.memory.mem_constants[dir] = val

    ##This function returns the direction of quadruple elements with exception of the operator
    ##op_i -> left operator from quad, op_d -> right operator from quad, res -> quad result
    def dame_memorias(self, op_i, op_d, res):
        return self.dame_mem(op_i) , self.dame_mem(op_d), self.dame_mem(res)

    ## This function returns the direction of global, local variable or constants
    def dame_mem(self, dir):
        if dir is None:
            return None
        elif 1000 <= dir < 21000:
            return self.memory.mem_global
        elif 21000 <= dir < 41000:
            return self.memory.active.mem_local if self.memory.active is not None else self.memory.mem_local
        else:
            return self.memory.mem_constants

    ## This function returns the variable type, dir -> variable direction
    def dame_tipo(self,dir):
        if 1000 <= dir < 6000 or 21000 <= dir < 26000:
            return int
        elif 6000 <= dir < 11000 or 26000 <= dir < 31000:
            return float
        elif 11000 <= dir < 16000 or 31000 <= dir < 36000:
            return str
        elif dir >= 41000:
            return type(self.memory.mem_constants[dir])
        else:
            return bool

    def activa_tortuga(self):
        self.turtle_activa = True
        
        s = Turtle()
        self.screen = Screen()
        self.dibuja_pointer(s)

        self.screen.title(self.programa)
        self.screen.clear()
        self.pointer = Turtle(shape="pointer")
        

    ## Defines pointer as the pencil for drawing
    def dibuja_pointer(self,lapiz):
        fig = Shape("compound")
        lapiz.setx(0)
        lapiz.sety(4)

        lapiz.begin_poly()
        lapiz.goto(1,0)
        lapiz.goto(1,-1)
        lapiz.goto(-1,-1)
        lapiz.goto(-1,1)
        lapiz.goto(1,1)
        lapiz.goto(1,0)
        lapiz.end_poly()

        fig.addcomponent(lapiz.get_poly(),"blue","blue")
        self.screen.register_shape("pointer",fig)
        lapiz.reset()

    def dame_contenido(self, dir):
        dir_aux = int(dir[1:-1])
        dir_mem = self.dame_mem(dir_aux)
        return dir_mem[dir_aux]