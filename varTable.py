# varTable: Generates the function directory and its respective variable tables
#
# @author: Emilio López Hernández
#
# A01651283
#
# Delivery date: 27/11/2019 
#
#

class VarTable:

    def __init__(self):
        self.table = {
            'global': {
                'program': '',
                'vars': {},
            },
            'mainF': {
                'type': 'void',
                'vars': {},
                'begin': None,
            }
        }
        self.current_type = ''
        self.current_scope = 'global'
        self.initialized = False
    
    ## This function creates main directory to store alll created functions,
    ## The current scope is global, fun_id refers to the program, function or main function name
    ## type referes to the type of function (np = program, mainF = void)
    def functionDirectory(self, fun_id, type, start):
        if type == 'np':
            self.current_scope = 'global'
            self.current_type = type
            self.table['global']['program'] = fun_id

        elif type == 'mainF':
            self.current_scope = 'mainF'
            self.current_type = type
            self.table['mainF']['begin'] = start

        elif fun_id not in self.table:
            vt_name = 'vars-' + fun_id
            self.table[fun_id] = {
                'type': type,
                'vars': {},
                'params': [],
                'begin': start,
            }
            self.current_scope = fun_id
            self.current_type = type
        else:
            raise TypeError(f'Function {fun_id} already declared')
        self.initialized = True

    ## This function adds a new variable to the var table in the actual scope
    ## var_id -> variable name, var_type -> variable type, dir -> assigned direction to the variable
    ## b_dim -> boolean if is a dimension variable, dim -> variable size (dimension case)
    def insertVar(self, var_id, var_type, dir, b_dim, dim):
        scope = self.current_scope

        # New Function
        if var_id not in self.table[scope]['vars'] and var_id not in self.table['global']['vars'] and scope != 'global' and scope != 'mainF' and var_id not in self.table[scope]['params']:
            new_var = {
                'id': var_id,
                'type': var_type,
                'dir': dir,
                'esdimensionada': b_dim,
                'var_dim':dim
            }
            self.table[scope]['vars'][var_id] = new_var

        # Global or mainF
        elif var_id not in self.table[scope]['vars'] and var_id not in self.table['global']['vars'] and (scope == 'global' or scope == 'mainF'):
            new_var = {
                'id': var_id,
                'type': var_type,
                'dir': dir,
                'esdimensionada':b_dim,
                'var_dim':dim
            }
            self.table[scope]['vars'][var_id] = new_var

        else:
            raise TypeError(f'Variable {var_id} already declared')

    ## This function inserts a given parameter 
    def insertParam(self,param_id,param_type):
        scope = self.current_scope
        if param_id not in self.table[scope]['params'] and param_id not in self.table['global']['vars']:
            self.table[scope]['params'].append(param_type)
        else:
            raise TypeError(f'Parameter {param_id} already declared')
    
    ## This function search variables to detect multiple declaration
    def searchVar(self, var_id):
        scope = self.current_scope

        if var_id in self.table[scope]['vars']:
            return self.table[scope]['vars'][var_id]
        elif var_id in self.table['global']['vars']:
            return self.table['global']['vars'][var_id]
        else:
            raise TypeError(f"Variable {var_id} has not been declared")
    
    ## This function deletes vars tables after each function is finished and the table is no longer needed

    def deleteVar(self, table_id):
        if table_id in self.table:
            del self.table[table_id]['vars']
        else:
            raise TypeError(f"Table {table_id} was not found")