# Lexer: Lexical analyzer of FIGURE language
#
# @author: Emilio López Hernández
#
# A01651283
#
# Delivery date: 27/11/2019 
#
#


from ply import lex

# List of reserved words
keywords = {
    'program' : 'PROGRAM',
    'int': 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'void': 'VOID',
    'function' : 'FUNCTION',
    'return': 'RETURN',
    'if' : 'IF',
    'else' : 'ELSE',
    'elseif' : 'ELSEIF',
    'print' : 'PRINT',
    'read' : 'READ',
    'while' : 'WHILE',
    'for': 'FOR',
    'circle': 'CIRCLE',
    'square': 'SQUARE',
    'triangle': 'TRIANGLE',
    'rectangle': 'RECTANGLE',
    'go': 'GO',
    'left': 'LEFT',
    'right': 'RIGHT',
    'back': 'BACK',
    'down': 'DOWN',
    'up': 'UP',
    'position': 'POSITION',
    'speed' : 'SPEED',
    'pointer_color': 'POINTER_COLOR',
    'pointer_size': 'POINTER_SIZE',
    'start_f': 'START_F',
    'end_f': 'END_F',
    'exit': 'EXIT'
} 

# List of tokens
tokens = [
    'ID', 'COMMA', 'COLON', 'SEMICOLON','LPARENT', 'RPARENT', 
    'LCURBRA', 'RCURBRA', 'LBRACK','RBRACK','EQUAL', 'ISEQUAL', 
    'DIFFERENT','PLUS','MINUS','MULT', 'DIVIDE', 'MINORT','GREATERT', 
    'MINOREQT','GREATEREQT', 'CTE_INT', 'CTE_FLOAT','CTE_STRING'
] + list(keywords.values())

# Tokens definition
t_ignore = r' '
t_COMMA = r'\,'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LCURBRA= r'\{'
t_RCURBRA = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_EQUAL = r'\='
t_ISEQUAL = r'\=='
t_DIFFERENT = r'\!='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIVIDE = r'\/'
t_MINORT = r'\<'
t_GREATERT = r'\>'
t_MINOREQT = r'\<='
t_GREATEREQT = r'\>='

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_CTE_FLOAT(t):
    r'[+-]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTE_STRING(t):
    r'\"(\\.|[^"\\])*\"'
    t.value = str(t.value)
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()






