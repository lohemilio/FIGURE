# compilerResult: generate a json file with the compilation process results
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

from virtualMachine import VirtualMachine

## This function generates a file with program quadruples, function tables and constants
def genFile(program,varst,quads,consts):
    compFile = {
        "Quads" : quads,
        "FunDir" : varst,
        "tConstants": consts
    }

    with open(f'test/{program}_compiled.fi', 'w') as newFile:
        json.dump(compFile,newFile, separators = (',',':'))


    # send data to Virtual Machine
    VirtualMachine().getData(program)
