# Lexer for Cuppa3

import re
from ply import lex

reserved = {
    'get'     : 'GET',
    'put'     : 'PUT',
    'if'      : 'IF',
    'else'    : 'ELSE',
    'while'   : 'WHILE',
    'not'     : 'NOT',
    'declare' : 'DECLARE',
    'return'  : 'RETURN'
}

literals = [',',';','=','(',')','{','}','[',']',':']

tokens = [
          'PLUS','MINUS','TIMES','DIVIDE',
          'EQ','LE', 
          'INTEGER','ID'
          ] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQ      = r'=='
t_LE      = r'<='

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def is_ID(s):
    m = re.match(r'[a-zA-Z_][a-zA-Z_0-9]*', s)
    
    if s in list(reserved.keys()):
        return False
    elif m and len(m.group(0)) == len(s):
        return True
    else:
        return False

def t_INTEGER(t):
    r'[0-9]+'
    return t

def t_COMMENT(t):
    r'//.*'
    pass

def t_NEWLINE(t):
    r'\n'
    pass

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# build the lexer
lexer = lex.lex(debug=0)

