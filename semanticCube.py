# semanticCube: generation of a semantic cube through a dictionary to specify allowed operations between the distinct operations
#
# @author: Emilio López Hernández
#
# A01651283
#
# Delivery date: 27/11/2019 
#
#


import sys
from enum import Enum

class Operators(Enum):
    PLUS = '+'
    MINUS = '-'
    MULT = '*'
    DIVIDE = '/'
    GREATERT = '>'
    GREATEREQT = '>='
    MINORT = '<'
    MINOREQT = '<='
    DIFFERENT = '!='
    ISEQUAL = '=='
    EQUAL = '='
    RETURN = 'return'

class SemanticCube:
    ## This function initializes the semantic cube and use a dictionary 
    def __init__(self):
        self.semantic_cube = {
            Operators.PLUS: {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'string': 'string'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'string': 'string'
                },
                'string': {
                    'int': 'string',
                    'float': 'string',
                    'string': 'string'
                }
            },
            Operators.MINUS: {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'string': 'err'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'err'
                }
            },
            Operators.MULT: {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'string': 'err'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'err'
                }
            },

            Operators.DIVIDE: {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'string': 'err'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'err'
                }
            },
            Operators.GREATERT: {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'err'
                }
            },

            Operators.MINORT: {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'err'
                }
            },
            Operators.GREATEREQT: {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'err'
                }
            },

            Operators.MINOREQT: {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'err'
                }
            },
            Operators.ISEQUAL: {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'string'
                }
            },
            Operators.DIFFERENT: {
                'int': {
                    'int': 'bool',
                    'float': 'err',
                    'string': 'err'
                },
                'float': {
                    'int': 'err',
                    'float': 'bool',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'bool'
                }
            },
            Operators.EQUAL: {
                'int': {
                    'int': 'int',
                    'float': 'int',
                    'string': 'err'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'string'
                }
            },
            Operators.RETURN: {
                'int': {
                    'int': 'int',
                    'float': 'err',
                    'string': 'err'
                },
                'float': {
                    'int': 'err',
                    'float': 'float',
                    'string': 'err'
                },
                'string': {
                    'int': 'err',
                    'float': 'err',
                    'string': 'string'
                }
            }


        }
    
    ## This function determines if an operation is valid taking in account the variable types
    def semantics(self, left_type, right_type, operator):
        if self.semantic_cube[operator][left_type][right_type] != 'err':
            return self.semantic_cube[operator][left_type][right_type]
        raise TypeError("Invalid operator {} for {} and {}".format(
            operator.name, left_type, right_type))