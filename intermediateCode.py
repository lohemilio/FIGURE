# intermediateCode: generation of intermediate code; specifically quadruples
#
# @author: Emilio López Hernández
#
# A01651283
#
# Delivery date: 27/11/2019 
#
#

import json
from semanticCube import SemanticCube, Operators
from varTable import VarTable

class Quadruple:
    ## This function initializes the quadruple
    def __init__(self, operator,left_op, right_op, result):
        self.left_op = left_op
        self.right_op = right_op
        self.operator = operator
        self.result = result

    def __repr__(self):
        return f"\t{self.operator}\t{self.left_op}\t{self.right_op}\t{self.result}\n"

    def __str__(self):
        return f"\t{self.operator},{self.left_op},{self.right_op},{self.result}\n"

    ## This function change the result of each new quadruple. res -> new result
    def changeResult(self,res):
        self.result = res

class IntermediateCode:
    def __init__(self):
        # Stack of Pending Operators
        self.POper = []
        # Stack of Types
        self.PTypes = []
        # Stack of Pending Operands
        self.PilaO = []
        # Stack of Pending Jumps
        self.PJumps = []

        self.start_mainF = None
        self.gen_mainF = False
        self.era = None

        # Counters
        self.temps = 0

        # For saving booleans
        self.c_params = 0
        self.c_global = [0,0,0,0]
        self.c_local = [0,0,0,0]
        self.c_consts = [0,0,0,0]

        self.Quads = [] #Quadruples list
        self.counter = 1 
        self.cube = SemanticCube()
        self.PTemp = []  
        self.constants = {}

        # Bases for memory

        # GLOBAL
        # i [1000  -  5999]
        # f [6000  -  9999]
        # s [11000 - 15999]
        # b [16000 - 20999]
        # LOCAL
        # i [21000 - 25999]
        # f [26000 - 30999]
        # s [31000 - 35999]
        # b [36000 - 40999]
        # CONSTANTS
        # c [41000 - 51999]

        # Global
        self.base_global = 1000

        # Temp locals
        self.base_local = 21000
        self.base_constants = 41000

        self.b_int = 0
        self.b_float = 5000
        self.b_string = 10000
        self.b_bool = 15000
    ## This function resets the locals and temps counter
    def resetLocals(self):
        self.c_local = [0,0,0,0]

    ## This function saves variable in memory and returns the direction
    ## mem -> type of memory, type-> type of variable, size for vectors
    def memoryDirection(self, mem, type, size = 1, val = None):
        if type == 'int':
            t_start = self.b_int
            t_fin = self.b_float - 1
            index = 0
        elif type == 'float':
            t_start = self.b_float
            t_fin = self.b_string - 1
            index = 1
        elif type == 'string':
            t_start = self.b_string
            t_fin = self.b_bool
            index = 2
        elif type == 'bool':
            t_start = self.b_bool
            t_fin = self.base_constants
            index = 3
        else:
            raise TypeError(f"Type '{type}' unrecognized")

        if mem == 'global':
            dir = self.base_global + t_start + self.c_global[index]
            self.c_global[index] += size

            if dir + size > self.base_global + t_fin:
                raise TypeError(f"Stack Overflow: {mem} does not have space for {type}")


        elif mem == 'local':
            dir = self.base_local + t_start + self.c_local[index]
            self.c_local[index] += size
            if dir + size > self.base_local + t_fin:
                raise TypeError(f"Stack Overflow: {mem} does not have space for {type}")

        elif mem == 'constants':
            if val is None:
                raise TypeError(f"Constant value not specified")


            elif val in self.constants.values():
               return [x for x, y in self.constants.items() if y == val].pop()
            dir = self.base_constants + t_start + self.c_consts[index]

            if dir + size > self.base_constants + t_fin:
                raise TypeError(f"Stack Overflow: {mem} does not have space for {type}")

            if index == 2:
                val = val.strip('"')

            self.constants[dir] = val
            self.c_consts[index] += size

        else:
            raise TypeError(f"Memory type '{mem}' unrecognized")

        return dir

    def generateQuad(self,scope):
        right_op = self.PilaO.pop()
        right_type = self.PTypes.pop()

        left_op = self.PilaO.pop()
        left_type = self.PTypes.pop()

        operator = self.POper.pop()
        operator_s = Operators(operator)

        result_type = self.cube.semantics(left_type, right_type, operator_s)

        if result_type:
            if operator != '=':

                # Temp is generated
                if scope == 'global':
                    result = self.memoryDirection('global',result_type)
                else :
                    result = self.memoryDirection('local',result_type)

                quadruple = Quadruple(operator, left_op, right_op, result)
                self.PilaO.append(result)
                self.PTypes.append(result_type)

            else:
                result = left_op
                quadruple = Quadruple(operator, result, None, right_op)
        self.Quads.append(quadruple)

        return result_type

    ## This function generates the quadruple for print
    def generateQuadPrint(self):
        result = self.PilaO.pop()
        self.PTypes.pop()
        operator = self.POper.pop()
        quadruple = Quadruple(operator, None, None, result)
        self.Quads.append(quadruple)

    ## This function generates the quadruple for statement read
    def generateQuadRead(self):
        result = self.memoryDirection('local','string')

        operator = self.POper.pop()
        quadruple = Quadruple(operator, None, None, result)

        self.Quads.append(quadruple)
        self.POper.append(result)
        self.PTypes.append('string')

    ## This function generates the quadruple for GOTOF (condition)
    def generateGOTOF(self):
        exp_type = self.PTypes.pop()
        
        if exp_type != 'bool':
            raise TypeError("ERROR: Type-mismatch")
        else:
            result = self.PilaO.pop()
            quadruple = Quadruple('GotoF', result, None, None)
            self.Quads.append(quadruple)
            self.PJumps.append(len(self.Quads)-1)

    ## This function generates the quadruple for GOTOV
    def generateGOTOV(self):
        cond = self.PilaO.pop()
        self.PTypes.pop()


        print("cond", cond)

        quadruple = Quadruple('GotoV', cond, None, None)
        self.Quads.append(quadruple)

    ## This function fills the GOTOV for FOR
    def fill_gotoV(self, salto):
        position = self.PJumps.pop()
        print('position',position)

        self.Quads[position].changeResult(salto)

    def generateENDPROC(self):
        quadruple = Quadruple('ENDPROC',None,None,None)
        self.Quads.append(quadruple)

    ## This function generates the END quadruple that determines the enf of file
    def generateEND(self):
        quadruple = Quadruple('END',None,None,None)
        self.Quads.append(quadruple)

    ## This function generates GOTO for ELSE
    def generateElse(self):
        quadruple = Quadruple('Goto', None, None, None)
        self.Quads.append(quadruple)
        position = self.PJumps.pop()
        self.PJumps.append(len(self.Quads) - 1)
        self.fillQuad(position)

    ## This function generates GOTO; that will be filled after
    def generateGOTO(self):
        quadruple = Quadruple('Goto', None, None, None)
        self.Quads.append(quadruple)

    ## This function generates GOTO for the mainF
    def generateGOTOMainF(self):
        quadruple = Quadruple("Goto_main",None,None,None)
        self.Quads.append(quadruple)
        self.start_mainF = len(self.Quads) - 1


    ## This function fills the GOTO for the mainF. result-> position to be filled, where main starts
    def fillGOTOMainF(self,result):
        if self.start_mainF is not None:
            self.Quads[self.start_mainF].changeResult(result)
    
    ## This function fills the Quadruple. p-> position to be filled
    def fillQuad(self,p):
        self.Quads[p].changeResult(len(self.Quads)+1)

    ## This function fills GOTO with the result, result-> value to fill goto
    def fillGOTO(self, result):
        position = len(self.Quads) - 1
        self.Quads[position].changeResult(result)

    ## This function generates quadruple for graph without parameters
    ## type -> type of action for graph (up or down)
    def generateQuadGraph0(self, type):
        quadruple = Quadruple(type, None, None, None)
        self.Quads.append(quadruple)

    ## This function generates quadruple for graph with only one parameter
    def generateQuadGraph1(self,type):
        exp_type = self.PTypes.pop()

        if type == 'pointer_color' and exp_type != 'string':
            raise TypeError("ERROR: Type-mismatch")
        else:
            result = self.PilaO.pop()
            quadruple = Quadruple(type, result, None, None)
            self.Quads.append(quadruple)

    ## This function generates quadruple for graph with one parameter (two expressions)
    def generateQuadGraph2(self,type):
        expT_1 = self.PTypes.pop()
        expT_2 = self.PTypes.pop()

        if expT_1 != 'int' or expT_2 != 'int':
            raise TypeError("ERROR: Type-mismatch")
        else:
            exp_1 = self.PilaO.pop()
            exp_2 = self.PilaO.pop()
            quadruple = Quadruple(type, exp_2, exp_1, None)
            self.Quads.append(quadruple)

    ## This function generates quadruple for ERA (Function call)
    def generateERA(self):
        quadruple = Quadruple('ERA', None, None, None)
        self.Quads.append(quadruple)
        self.era = len(self.Quads)-1

    ## This function fills ERA with the number 
    def fillERA(self, funcName):
        if self.era is not None:
            self.Quads[self.era].changeResult(funcName)

    ## This function generates quadruple for parameters
    def generateParamQuad(self):
        quadruple = Quadruple('param', None, None, self.PilaO.pop())
        self.Quads.append(quadruple)

    ## This function generates quadruple for gosub
    def generateGOSUB(self, begin, type):
        if type != 'void':
            valor_retorno = self.memoryDirection('local', type)
            self.PilaO.append(valor_retorno)
            self.PTypes.append(type)
        else:
            valor_retorno = None

        quadruple = Quadruple('GOSUB', valor_retorno, None, begin)
        self.Quads.append(quadruple)
    ## This function generates quadruple for return of a function
    ## type -> function type
    def generateReturn(self,type):
        self.cube.semantics(self.PTypes.pop(),type,Operators.RETURN)

        quadruple = Quadruple('RETURN',None,None,self.PilaO.pop())

        self.Quads.append(quadruple)


    ## This function check parameter types 
    ## params_dec -> sended params
    ## params_fun -> defined params in function header
    def checkParamTypes(self, params_dec, params_fun):
        len1 = len(params_dec)
        len2 = len(params_fun)

        if len(params_fun) != len(params_dec):
            raise TypeError("ERROR: Expected "+str(len1)+" params, got "+str(len2)+" instead")
        elif params_dec != params_fun:
            raise TypeError("ERROR: Type mismatch in parameters")
    

    ## This function generates quadruples for matrix access
    ## base -> base direction, var_dim -> dimension variable
    def genMatrix(self, base, r, c, var_dim):
        base = self.memoryDirection('constants','int',val= base)
        ren = self.memoryDirection('constants','int',val=var_dim[0])
        col = self.memoryDirection('constants','int',val= var_dim[1])

        # Quadruples to verify ranges
        ver1 = Quadruple('VER', c, ren, None)
        ver2 = Quadruple('VER', r, col, None)

        self.Quads.append(ver1)
        self.Quads.append(ver2)

       
        # Quadruples for * aux mdim T
        auxmdim = self.memoryDirection('local','int')

        q_auxmdim = Quadruple('*',c,ren,auxmdim)
        self.Quads.append(q_auxmdim)

        # Quadruples for + aux1 aux2 T
        sumaux = self.memoryDirection('local','int')
        temp = Quadruple('+',auxmdim,r,sumaux)
        self.Quads.append(temp)

        # Quadruples for + T BASE T
        sumabase = self.memoryDirection('local','int')
        q_sumabase = Quadruple('+',sumaux, base, sumabase)
        self.Quads.append(q_sumabase)
        
        return sumabase

    ## This function generates quadruples for vector access
    ## base -> base direction, size -> array size, var_dim -> dimension variable
    def genArrays(self,base,size, var_dim):
        base = self.memoryDirection('constants','int',val=base)
        tsize = self.memoryDirection('constants','int',val= var_dim[1])

        # Quadruple to verify
        ver = Quadruple('VER', size, tsize, None)
        self.Quads.append(ver)

        # Sum Base
        sumabase = self.memoryDirection('local','int')
        q_sumabase = Quadruple('+',size, base, sumabase)
        self.Quads.append(q_sumabase)
        return sumabase


    def formatQuads(self):
        return [(quad.operator, quad.left_op, quad.right_op, quad.result) for quad in self.Quads]

    def formatConstants(self):
        return [(k, v) for k, v in self.constants.items()]