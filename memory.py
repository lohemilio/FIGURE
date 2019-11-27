# memory: For execution memory
#
# @author: Emilio López Hernández
#
# A01651283
#
# Delivery date: 27/11/2019 
#
#

from collections import OrderedDict

class Memory:

    def __init__(self):
        self.mem_global = {}
        self.mem_local = {}
        self.mem_constants = {}

        self.mem_exec = OrderedDict()
        self.active = None
        self.base_fun = 40000
        self.counter = 0
    ## This function activates function memory when is called
    ## superior -> function where it is called, size -> quantity of variables of the called function
    def recordActivation(self, superior, size):
        actual = localMemory(superior, size)

        if self.counter + size > 40000:
            raise TypeError(f'Stack Overflow: Execution Stack')

        dir = self.base_fun + self.counter
        self.counter = self.counter + size
        self.mem_exec[dir] = actual
    
    ## This function deletes scope from actual local memory
    def throat(self):
        if self.active is not None:
            if self.active.superior is not self:
                self.active = self.active.superior
            else:
                self.active = None
            fun = list(self.mem_exec.keys())[-1]
            self.counter -= self.mem_exec[fun].tam
            del self.mem_exec[fun]


class localMemory:
    def __init__(self, superior, size):
        self.mem_local = {}
        self.counter = 21000 # base local

        self.c_int = 0
        self.c_str = 10000
        self.c_float = 5000
        
        self.superior = superior
        self.size = size

    ## This function assigns parameter values to variables of that function
    ## params -> list of parameters
    def matcheo(self,params):
        for p in params:
            if type(p) is int:
                self.mem_local[self.counter + self.c_int] = p
                self.c_int += 1

            elif type(p) is float:
                self.mem_local[self.counter + self.c_float] = p
                self.c_float += 1
            
            elif type(p) is str:
                self.mem_local[self.counter + self.c_str] = p
                self.c_str += 1