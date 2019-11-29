# execute: For compiling and executing our .FIG file
#
# @author: Emilio López Hernández
#
# A01651283
#
# Delivery date: 27/11/2019 
#
#

import sys
import json
import parser

from varTable import VarTable
from intermediateCode import IntermediateCode

varsTable = VarTable()
codeGeneration = IntermediateCode()

if __name__ == '__main__':
    
    args = sys.argv[1:]
    fileName = args[0] 
    
    try:
        path = 'test/'

        path += fileName
        arch = open(path, 'r')
        info = arch.read()
        arch.close()

        if(parser.yacc.parse(info, tracking=True) == 'PROGRAM COMPILED'):
            print(f"{fileName} successfully compiled")
        else:
            print("Compilation errors")
    
    except FileNotFoundError:
        print(f"{fileName} not found")

    except EOFError:
        print(EOFError)