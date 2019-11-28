# parser: Parser for gramatic rules 
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
import compilerResult

from ply import yacc
from lexer import tokens
from varTable import VarTable
from intermediateCode import IntermediateCode

varsTable = VarTable()
interCode = IntermediateCode()

def p_program(p):
    '''
    program : PROGRAM ID SEMICOLON declara_vars program_fun mainF
    '''

    p[0] = "PROGRAM COMPILED"
    varsTable.deleteVar('global')
    
    f_quads = interCode.formatQuads()
    f_constantes = interCode.formatConstants()

    # Generates compiled file
    compilerResult.genFile(p[2],varsTable.table, f_quads, f_constantes)

def p_program_fun(p):
    '''
    program_fun : funs
    '''

def p_funs(p):
    '''
    funs : function_t funs
         | function_v funs
         | empty
    '''

def p_mainF(p):
    '''
    mainF : mainFI declara_vars mainF1 RCURBRA
    '''
    s_table = varsTable.table['mainF']

    mainF = interCode.PJumps.pop()
    interCode.fillGOTOMainF(mainF)

    count_vars = len(s_table['vars'])
    varsTable.deleteVar('mainF')
    
    s_table['vars'] = count_vars
    interCode.generateEND()


def p_mainFI(p):
    '''
    mainFI : mainF_sign LCURBRA
    '''
    interCode.resetLocals()
    varsTable.functionDirectory('mainF', 'mainF',p[1])

def p_mainF_sign(p):
    '''
    mainF_sign : MAINF
    '''
    beginMainF = len(interCode.Quads) + 1
    interCode.PJumps.append(beginMainF)
    p[0] = beginMainF


def p_mainF1(p):
    '''
    mainF1 : stmt_v mainF1
        | empty
    '''

def p_declara_vars(p):
    '''
    declara_vars : vars declara_vars
          | empty
    '''
    scope = varsTable.current_scope
    if scope == 'global' and not interCode.gen_mainF:
        interCode.generateGOTOMainF()
        interCode.gen_mainF = True

    if len(p) == 3:
        p[0] = p[1:]
        p[0] = flatten(p[0])

# Inside list
def p_vars(p):
    '''
    vars : type ID dimensionada equals exp SEMICOLON
         | type ID dimensionada SEMICOLON
    '''
    p[0] = (p[1], p[2])

    # dimension variables
    if isinstance(p[3], tuple):
        dimensionada = True
        var_dim = p[3]
        dim = var_dim[0] * var_dim[1]

    else:
        dimensionada = False
        var_dim = None
        dim = 1


    if not varsTable.initialized:
        varsTable.functionDirectory('global', 'np',None)

    if varsTable.current_scope == 'global':
        dir = interCode.memoryDirection('global',p[1],dim)

    else:
        dir = interCode.memoryDirection('local',p[1],dim)
    
    # Save ID and type
    # Indicate dimension

    varsTable.insertVar(p[2],p[1],dir,dimensionada,var_dim)

    if dimensionada:
        if interCode.POper and interCode.POper[-1] in ['=']:
            
            # verify tuple size
            if var_dim == p[5]:
                interCode.POper.pop()
                
                # assign directions
                for i in range(dim-1,-1,-1):
                    interCode.POper.append('=')
                    interCode.PilaO.append(dir + i)
                    interCode.PTypes.append(p[1])

                    interCode.generateQuad(varsTable.current_scope)
            else:
                raise TypeError(f"Dimension variable {p[2]} must be size {var_dim}")

        else:
            # blank array
            if p[1] == 'int':
                blanco = 0
            elif p[1] == 'float':
                blanco = 0.0
            elif p[1] == 'string':
                blanco = ""

            blanco = interCode.memoryDirection('constants',p[1],val=blanco)

            for i in range(dim - 1,-1,-1):
                
                interCode.PilaO.append(blanco)
                interCode.POper.append('=')
                interCode.PilaO.append(dir + i)

                interCode.PTypes.append(p[1])
                interCode.PTypes.append(p[1])

                interCode.generateQuad(varsTable.current_scope)

    else:

        if interCode.POper and interCode.POper[-1] in ['=']:
            interCode.PilaO.append(dir)
            interCode.PTypes.append(p[1])
            result = interCode.generateQuad(varsTable.current_scope)



# Dimension or not variable
def p_dimensionada(p):
    '''
    dimensionada : LBRACK CTE_INT RBRACK
           | LBRACK CTE_INT RBRACK LBRACK CTE_INT RBRACK
           | empty
    '''
    if len(p) == 2:
        p[0] = None

    elif len(p) == 4:
        p[0] = (1, int(p[2]))
    else:
        p[0] = (int(p[2]),int(p[5]))

# LOOP
def p_loop(p):
    '''
    loop : while
         | for_v2
    '''

# STMT
def p_stmt(p):
    '''
    stmt : assignment
        | condition
        | print
        | loop
        | read
        | graphstmt
        | funCall SEMICOLON
        | return
    '''

def p_stmt_v(p):
    '''
    stmt_v : assignment
        | condition
        | print
        | loop
        | read
        | graphstmt
        | funCall SEMICOLON
    '''

def p_assignment(p):
    '''
    assignment : id equals assignment3 SEMICOLON
    '''
    t = varsTable.searchVar(p[1][0])
    if t:
        if t['esdimensionada']:
            dir = f"({p[1][1]})"

        else:
            dir = t['dir']
        interCode.PilaO.append(dir)
        interCode.PTypes.append(t['type'])

    if interCode.POper and interCode.POper[-1] in ['=']:
        interCode.generateQuad(varsTable.current_scope)

def p_assignment3(p):
    '''
    assignment3 : exp
                | read
    '''
    p[0] = p[1]


# VAR_CTE
def p_vcte(p):
    '''
    vcte : cte_int
         | cte_float
         | cte_string
         | id
         | funCall
         | vectormatriz
    '''
    p[0] = p[1]


def p_vectormatriz(p):
    '''
    vectormatriz : LBRACK vm1 RBRACK
                 | vm1
    '''
    
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]
    

def p_vm1(p):
    '''
    vm1 : LBRACK vm2 RBRACK COMMA vm1
        | LBRACK vm2 RBRACK
    '''
    if len(p) > 4:
        if p[5][1] == p[2]:
            p[0] = (p[5][0] + 1, p[2])
        else:
            raise TypeError(f"Matrices need same array size")
    else:
        p[0] = (1,p[2])
        

def p_vm2(p):
    '''
    vm2 : exp COMMA vm2
        | exp
        | empty
    '''
    if len(p) > 2:
        p[0] = 1 + p[3]
    else:
        p[0] = 1

# FUNCTION
def p_functionI(p):
    '''
    functionI : type ID
    '''

    p[0] = p[2]

    interCode.resetLocals()
    beginFun = len(interCode.Quads) + 1
    varsTable.functionDirectory(p[2],p[1],beginFun)
    # functions as global variables
    varsTable.table['global']['vars'][p[0]] = { 'id': p[0], 'type':p[1]}

def p_functionV(p):
    '''
    functionV : VOID ID
    '''
    p[0] = p[2]

    interCode.resetLocals()
    beginFun = len(interCode.Quads) + 1
    varsTable.functionDirectory(p[2],p[1],beginFun)

    # functions as global variables
    varsTable.table['global']['vars'][p[0]] = { 'id': p[0], 'type':p[1]}

def p_function_t(p):
    '''
    function_t : FUNCTION functionI function2 inicia_fun declara_vars function4 termina_fun
    '''

    table = varsTable.table[p[2]]

    if p[7] is not None:
        vars = p[7]
        vars = vars[:-1]
        p[0] = vars

    interCode.generateENDPROC()
    count_vars = len(table['vars'])
    varsTable.deleteVar(p[2])

    

    table['vars'] = count_vars



def p_function_v(p):
    '''
    function_v : FUNCTION functionV function2 inicia_fun declara_vars function9 termina_fun
    '''

    table = varsTable.table[p[2]]

    if p[7] is not None:
        vars = p[7]
        vars = vars[:-1]
        p[0] = vars

    interCode.generateENDPROC()
    count_vars = len(table['vars'])
    varsTable.deleteVar(p[2])

    table['vars'] = count_vars

def p_inicia_fun(p):
    '''
    inicia_fun : LCURBRA
    '''


def p_termina_fun(p):
    '''
    termina_fun : RCURBRA
    '''

def p_function2(p):
    '''
    function2 : LPARENT function3 RPARENT
    '''

def p_function3(p):
    '''
    function3 : funParam function5
              | empty
    '''
    if p[1] is not None:
        p[0] = [p[1]]
        p[0].append(p[2])


def p_function4(p):
    '''
    function4 : stmt function4
              | empty
    '''
    if p[1] is not None:
        p[0] = p[1:]
        p[0] = flatten(p[0])

def p_function9(p):
    '''
    function9 : stmt_v function9
              | empty
    '''
    if p[1] is not None:
        p[0] = p[1:]
        p[0] = flatten(p[0])

def p_function5(p):
    '''
    function5 : COMMA funParam function5
              | empty
    '''
    if p[1] is not None:
        p[0] = p[2:]
        p[0] = flatten(p[0])

def p_funParam(p):
    '''
    funParam : type ID
    '''
    p[0] = (p[1],p[2])

    dir = interCode.memoryDirection('local', p[1])

    varsTable.insertVar(p[2], p[1], dir, False,None)
    varsTable.insertParam(p[2],p[1])
    interCode.PTemp.append(p[1])

# TYPE
def p_type(p):
    '''
    type : INT
         | FLOAT
         | STRING
    '''
    p[0] = p[1]


# PRINT
def p_print(p):
    '''
    print : PRINT LPARENT expression RPARENT SEMICOLON
    '''
    interCode.POper.append('print')
    interCode.generateQuadPrint()

# READ
def p_read(p):
    '''
    read : READ LPARENT id read1 RPARENT SEMICOLON
    '''
    interCode.POper.append('read')
    interCode.generateQuadRead()

# array
def p_read1(p):
    '''
    read1 : LBRACK exp RBRACK LBRACK exp RBRACK
          | LBRACK exp RBRACK
          | empty
    '''

def p_equals(p):
    '''
    equals : EQUAL
    '''
    interCode.POper.append(p[1])

# ASSIGNMENT
def p_indice_dimensionada(p):
    '''
    indice_dimensionada : LBRACK exp RBRACK LBRACK exp RBRACK
                        | LBRACK exp RBRACK
                        | empty

    '''

    if len(p) == 4:
        p[0] = (0,p[2])
    elif len(p) == 7:
        p[0] = (p[2],p[5])
    
def p_aidi(p):
    '''
    aidi : ID
    '''
    p[0] = p[1]
    interCode.POper.append('(')

def p_id(p):
    '''
    id : aidi indice_dimensionada
    '''

    interCode.POper.pop()
    t = varsTable.searchVar(p[1])

    if t:
        if t['esdimensionada']:
            # dimension without indexes
            if p[2] is None:
                raise TypeError(f"Dimension variable {p[1]} need indexes")
            base = t['dir']
            var_dim = t['var_dim']

            lim1 = interCode.PilaO.pop()
            interCode.PTypes.pop()

            # array
            if var_dim[0] == 1:
                dir = interCode.genArrays(base, lim1, var_dim)
            else:
                if len(interCode.PilaO) == 0:
                    raise TypeError(f"Dimension variable {p[1]} need two dimensions [[],[]]")
                lim2 = interCode.PilaO.pop()
                interCode.PTypes.pop()

                dir = interCode.genMatrix(base,lim1,lim2,var_dim)

            # return dir for quads
            interCode.PilaO.append(f"({dir})")
            interCode.PTypes.append(t['type'])
            p[0] = p[1] , dir
        else:
            interCode.PilaO.append(t['dir'])
            interCode.PTypes.append(t['type'])
            p[0] = p[1] , 0

# FUN_CALL
def p_funCall(p):
    '''
    funCall : ID iniciaFunCall funCall2 terminaFunCall
    '''

    if p[1] in varsTable.table:
        p[0] = p[1]

        init = varsTable.table[p[0]]['begin']
        params_declarados = varsTable.table[p[0]]['params']
        type = varsTable.table[p[0]]['type']
        interCode.fillERA(p[1])
        interCode.generateGOSUB(init,type)

        # if there is not parameters, send empty list
        if p[3] is not None:
            params_mandados = p[3]
        else:
            params_mandados = []

        interCode.checkParamTypes(params_declarados,params_mandados)

    else:
        raise TypeError(f"Function '{p[1]}' not declared")

    p[0] = interCode.Quads[-1].result


def p_iniciaFunCall(p):
    '''
    iniciaFunCall : LPARENT
    '''
    # fondo falso porque si no no jala
    interCode.POper.append('(')
    interCode.generateERA()


def p_terminaFunCall(p):
    '''
    terminaFunCall : RPARENT
    '''
    interCode.POper.pop()


def p_funCall2(p):
    '''
    funCall2 : funCallParam funCall3
             | empty
    '''
    types = []

    if len(p) == 3:
        types.append(p[1])
        types.append(p[2:])
        types = flatten(types)
        types = types[:-1]
        
        p[0] = types


def p_funCall3(p):
    '''
    funCall3 : COMMA funCallParam funCall3
             | empty
    '''

    if len(p) == 4:
        p[0] = p[2:]



def p_funCallParam(p):
    '''
    funCallParam : exp
    '''
    
    if isinstance(p[1],tuple):
        var_param = p[1][0]
        
        vt = varsTable.searchVar(var_param)
        dir = vt['dir']
        t = vt['type']
    else:
        # es constante el parametro alv
        dir = p[1]
        temp = interCode.constants[dir]

        if type(temp) is int:
            t = 'int'
        elif type(temp) is float:
            t = 'float'
        elif type(temp) is str:
            t = 'string'

    p[0] = t
    interCode.generateParamQuad()


# CTE
def p_cte_int(p):
    '''
    cte_int : negativo CTE_INT
    '''

    if p[1] is not None:
        num = int(f'-{p[2]}')
        dir = interCode.memoryDirection('constants','int',1,num)
    else:

        dir = interCode.memoryDirection('constants','int',1, p[2])

    p[0] = dir
    interCode.PTypes.append('int')
    interCode.PilaO.append(dir)


def p_cte_float(p):
    '''
    cte_float : negativo CTE_FLOAT
    '''
    if p[1] is not None:
        num = float(f'-{p[2]}')
    
        dir = interCode.memoryDirection('constants','float',1,num)
    else:
    
        dir = interCode.memoryDirection('constants','float',1, p[2])

    p[0] = dir
    interCode.PTypes.append('float')
    interCode.PilaO.append(dir)

def p_cte_string(p):
    '''
    cte_string : CTE_STRING
    '''
    dir = interCode.memoryDirection('constants','string', 1, p[1])
    p[0] = dir
    interCode.PilaO.append(dir)
    interCode.PTypes.append('string')


# RETURN
def p_return(p):
    '''
    return : RETURN return1 SEMICOLON
    '''
    scope = varsTable.current_scope
    tipo_fun = varsTable.table[scope]['type']
    interCode.generateReturn(tipo_fun)


def p_return1(p):
    '''
    return1 : vcte
            | exp
    '''
    p[0] = p[1]


# L_OP - LOGICAL OPERATOR
def p_loper(p):
    '''
    loper : GREATERT
          | MINORT
          | GREATEREQT
          | MINOREQT
          | DIFFERENT
          | ISEQUAL
    '''
    # 8. POper.Push(rel.op)
    interCode.POper.append(p[1])


# CONDITION
def p_condition(p):
    '''
    condition : IF head_cond body condition1
    '''
    # 2.-
    end = interCode.PJumps.pop()
    interCode.fillQuad(end)


def p_condition1(p):
    '''
    condition1 : elseif head_cond body condition1
               | else body
               | empty
    '''
    if len(p) == 5:
        end = interCode.PJumps.pop()
        interCode.fillQuad(end)


def p_elseif(p):
    '''
    elseif : ELSEIF
    '''
    interCode.generateElse()


def p_else(p):
    '''
    else : ELSE
    '''
    interCode.generateElse()

def p_head_cond(p):
    '''
    head_cond : LPARENT expression close_condition
    '''

# BODY
def p_body(p):
    '''
    body : LCURBRA body1 RCURBRA
    '''


def p_close_condition(p):
    '''
    close_condition : RPARENT
    '''
    # generate GOTOF
    interCode.generateGOTOF()


def p_body1(p):
    '''
    body1 : stmt body1
          | empty
    '''

# in list
def p_for_v2(p):
    '''
    for_v2 : nuevo_for forBody
    '''
    
    var = varsTable.searchVar(p[1][0])

    if var is not None:
        dir = var['dir']
    else:
        raise TypeError(f"'Variable {p[1][0]}' not declared")

    interCode.PilaO.append(dir)
    interCode.PTypes.append('int')


    suma_uno = interCode.memoryDirection('constants','int',1,1)

    interCode.PilaO.append(suma_uno)
    interCode.PTypes.append('int')
    interCode.POper.append('+')

    interCode.generateQuad(varsTable.current_scope)


    interCode.PilaO.append(dir)
    interCode.PTypes.append('int')
    interCode.POper.append('=')

    interCode.generateQuad(varsTable.current_scope)

    fin_for = interCode.PJumps.pop()
    ret = interCode.PJumps.pop()

    interCode.generateGOTO()
    interCode.fillGOTO(ret)

    interCode.fillQuad(fin_for)


def p_nuevo_for(p):
    '''
    nuevo_for : FOR LPARENT id COLON for2 RPARENT
    '''
    info = varsTable.searchVar(p[3][0])
    
    dir = info['dir']

    temp = interCode.PilaO[-1]

    temp_t = interCode.PTypes[-1]
    interCode.PilaO.pop()
    interCode.PTypes.pop()

    interCode.PilaO.append(dir)
    interCode.PTypes.append('int')
    interCode.POper.append('=')

    interCode.PilaO.append(dir)
    interCode.PTypes.append('int')
    interCode.POper.append('<')

    interCode.PilaO.append(temp)
    interCode.PTypes.append(temp_t)

    interCode.generateQuad(varsTable.current_scope)

    interCode.PJumps.append(len(interCode.Quads))

    interCode.generateGOTOF()
    p[0] = p[3]

def p_for2(p):
    '''
    for2 : exp
    '''
    p[0] = p[1]

def p_forBody(p):
    '''
    forBody : body
    '''
    
# WHILE
def p_while(p):
    '''
    while : while1 body
    '''
    end = interCode.PJumps.pop()
    w_return = interCode.PJumps.pop()

    interCode.generateGOTO()
    interCode.fillGOTO(w_return)

    interCode.fillQuad(end)


def p_while1(p):
    '''
    while1 : while_w LPARENT expression RPARENT
    '''
    interCode.generateGOTOF()


def p_while_w(p):
    '''
    while_w : WHILE
    '''
    # 1.-
    interCode.PJumps.append(len(interCode.Quads) + 1)


# (exp,exp)
def p_dosExp(p):
    '''
    dosExp : LPARENT exp COMMA exp RPARENT
    '''


# (exp)
def p_unaExp(p):
    '''
    unaExp : LPARENT exp RPARENT
    '''

# GRAPH_STMT
def p_graphstmt(p):
    '''
    graphstmt : graphfig
             | graphview
             | graphmove
    '''

# GRAPH_FIGURE
def p_graphfig(p):
    '''
    graphfig : graphfig1 SEMICOLON
             | graphfig2 SEMICOLON
    '''

# One expression
def p_graphfig1(p):
    '''
    graphfig1 : CIRCLE unaExp
            | SQUARE unaExp
            | TRIANGLE unaExp
    '''
    p[0] = p[1]
    interCode.generateQuadGraph1(p[0])

# two expressions
def p_graphfig2(p):
    '''
    graphfig2 : RECTANGLE dosExp
    '''
    p[0] = p[1]
    interCode.generateQuadGraph2(p[0])

# GRAPH_MOVEMENT
def p_graphmove(p):
    '''
    graphmove : graphmove0  SEMICOLON
              | graphmove1 SEMICOLON
    '''


def p_graphmove0(p):
    '''
    graphmove0 : DOWN
              | UP
    '''
    p[0] = p[1]
    interCode.generateQuadGraph0(p[0])


def p_graphmove1(p):
    '''
    graphmove1 : GO unaExp
              | LEFT unaExp
              | RIGHT unaExp
              | BACK unaExp
    '''
    p[0] = p[1]
    interCode.generateQuadGraph1(p[0])


# GRAPH_VIEW
def p_graphview(p):
    '''
    graphview : graphview0 SEMICOLON
              | graphview1 SEMICOLON
              | graphview2 SEMICOLON
    '''

def p_graphview0(p):
    '''
    graphview0 : EXIT
              | START_F
              | END_F
    '''
    p[0] = p[1]
    interCode.generateQuadGraph0(p[0])

def p_graphview1(p):
    '''
    graphview1 : POINTER_COLOR unaExp
              | POINTER_SIZE unaExp
              | SPEED unaExp
    '''
    p[0] = p[1]
    interCode.generateQuadGraph1(p[0])

def p_graphview2(p):
    '''
    graphview2 : POSITION dosExp
    '''
    p[0] = p[1]
    interCode.generateQuadGraph2(p[0])

# expression
def p_expression(p):
    '''
    expression : exp loper exp
               | exp
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1:]

# exp
def p_exp(p):
    '''
    exp : term
        | term exp_o exp
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1]

    if interCode.POper and interCode.POper[-1] in ['>','<','==','!=','<=','>=']:
        interCode.generateQuad(varsTable.current_scope)

def p_exp_o(p):
    '''
    exp_o : PLUS
          | MINUS
    '''
    interCode.POper.append(p[1])

def p_openP(p):
    '''
    openP : LPARENT
    '''
    # 6. crea fondo falso
    interCode.POper.append(p[1])


def p_closeP(p):
    '''
    closeP : RPARENT
    '''
    # 7. quita fondo falso
    interCode.POper.pop()

# TERM
def p_term(p):
    '''
    term : factor term_o term
         | factor
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1:]

    if interCode.POper and interCode.POper[-1] in ['+', '-']:
        t = interCode.generateQuad(varsTable.current_scope)

       


def p_term_o(p):
    '''
    term_o : MULT 
           | DIVIDE
    '''
    interCode.POper.append(p[1])


# FACTOR
def p_factor(p):
    '''
    factor : vcte
           | openP expression closeP
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1:]

    if interCode.POper and interCode.POper[-1] in ['*', '/']:
        t = interCode.generateQuad(varsTable.current_scope)
      

def p_negativo(p):
    '''
    negativo : MINUS
             | empty
    '''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    p[0] = None
    pass


def p_error(p):

    if p is not None:
        err = f"{p.value} in line {p.lineno}"

    raise TypeError(f"Sintax error: {err}")

def flatten(li):
    return sum(([x] if not isinstance(x, list) else flatten(x) for x in li), [])

parser = yacc.yacc(start='program')