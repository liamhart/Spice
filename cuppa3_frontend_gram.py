# Specification of the Cuppa3 Frontend

from ply import yacc
from cuppa3_lex import tokens, lexer, is_ID
from cuppa3_state import state

#########################################################################
# set precedence and associativity
# NOTE: all operators need to have tokens
#       so that we can put them into the precedence table
precedence = (
              ('left', 'EQ', 'LE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
              ('right', 'UMINUS', 'NOT')
             )

#########################################################################
# grammar rules with embedded actions
#########################################################################
def p_prog(p):
    '''
    program : stmt_list
    '''
    state.AST = p[1]

#########################################################################
def p_stmt_list(p):
    '''
    stmt_list : stmt stmt_list
              | empty
    '''
    if (len(p) == 3):
        p[0] = ('seq', p[1], p[2])
    elif (len(p) == 2):
        p[0] = p[1]

#########################################################################
def p_stmt(p):
    '''
    stmt : DECLARE ID '(' opt_formal_args ')' stmt
         | DECLARE ID opt_init opt_semi
         | ID '=' exp opt_semi
         | ID '=' '[' opt_contents ']' opt_semi
         | GET ID opt_semi
         | PUT exp opt_semi
         | ID '(' opt_actual_args ')' opt_semi
         | RETURN opt_exp opt_semi
         | WHILE '(' exp ')' stmt
         | IF '(' exp ')' stmt opt_else
         | '{' stmt_list '}'
    '''
    if p[1] == 'declare' and p[3] == '(':
        p[0] = ('fundecl', p[2], p[4], p[6])
    elif p[1] == 'declare':
        p[0] = ('declare', p[2], p[3])
    elif is_ID(p[1]) and p[2] == '=' and p[3] != '[':
        p[0] = ('assign', p[1], p[3])
    elif is_ID(p[1]) and p[2] == '=' and p[3] == '[':
        p[0] = ('assign', p[1], p[4])
    elif p[1] == 'get':
        p[0] = ('get', p[2])
    elif p[1] == 'put':
        p[0] = ('put', p[2])
    elif is_ID(p[1]) and p[2] == '(':
        p[0] = ('callstmt', p[1], p[3])
    elif p[1] == 'return':
        p[0] = ('return', p[2])
    elif p[1] == 'while':
        p[0] = ('while', p[3], p[5])
    elif p[1] == 'if':
        p[0] = ('if', p[3], p[5], p[6])
    elif p[1] == '{':
        p[0] = ('block', p[2])
    else:
        raise ValueError("unexpected symbol {}".format(p[1]))

#########################################################################
def p_opt_formal_args(p):
    '''
    opt_formal_args : formal_args
                    | empty
    '''
    p[0] = p[1]

#########################################################################
def p_formal_args(p):
    '''
    formal_args : ID ',' formal_args
                | ID
    '''
    if (len(p) == 4):
        p[0] = ('seq', ('id', p[1]), p[3])
    elif (len(p) == 2):
        p[0] = ('seq', ('id', p[1]), ('nil',))

#########################################################################
def p_opt_init(p):
    '''
    opt_init : '=' exp
             | empty
    '''
    if p[1] == '=':
        p[0] = p[2]
    else:
        p[0] = p[1]
        
#########################################################################
def p_opt_contents(p):
    '''
    opt_contents : contents
                 | empty
    '''
    
    p[0] = ('list', p[1])
    
#########################################################################
def p_contents(p):
    '''
    contents : exp ',' contents
             | exp
    '''
    if len(p) > 2:
        p[0] = [p[1], p[3]]
    else:
        p[0] = p[1]
    
#########################################################################
def p_opt_actual_args(p):
    '''
    opt_actual_args : actual_args
                    | empty
    '''
    p[0] = p[1]

#########################################################################
def p_actual_args(p):
    '''
    actual_args : exp ',' actual_args
                | exp
    '''
    if (len(p) == 4):
        p[0] = ('seq', p[1], p[3])
    elif (len(p) == 2):
        p[0] = ('seq', p[1], ('nil',))

#########################################################################
def p_opt_exp(p):
    '''
    opt_exp : exp
            | empty
    '''
    p[0] = p[1]

#########################################################################
def p_opt_else(p):
    '''
    opt_else : ELSE stmt
             | empty
    '''
    if p[1] == 'else':
        p[0] = p[2]
    else:
        p[0] = p[1]
    
#########################################################################
def p_binop_exp(p):
    '''
    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp EQ exp
        | exp LE exp
    '''
    p[0] = (p[2], p[1], p[3])
 
#########################################################################
def p_integer_exp(p):
    '''
    exp : INTEGER
    '''
    p[0] = ('integer', int(p[1]))
    
#########################################################################
def p_slice(p):
    '''
    exp : INTEGER '[' int_slice ']'
    '''
    p[0] = ('intindex', p[1], p[3])
    
#########################################################################
def p_integer_slice(p):
    '''
    int_slice : INTEGER req_col INTEGER
              | INTEGER
    
    '''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]

#########################################################################
def p_req_col(p):
    '''
    req_col : ':'  
    '''
    pass

    
#########################################################################
def p_id_exp(p):
    '''
    exp : ID
    '''
    p[0] = ('id', p[1])

#########################################################################
def p_call_exp(p):
    '''
    exp : ID '(' opt_actual_args ')'
    '''
    p[0] = ('callexp', p[1], p[3])

#########################################################################
def p_list_index(p):
    '''
    exp : ID '[' index_exp ']'
    '''
    p[0] = ('index', p[1], p[3])

#########################################################################
def p_index_exp(p):
    '''
    index_exp : INTEGER req_col INTEGER
              | INTEGER
    '''
    if len(p) == 4:
        # DO TEST IF LEN P0 > 2
        p[0] = (p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]

#########################################################################
def p_paren_exp(p):
    '''
    exp : '(' exp ')'
    '''
    p[0] = ('paren', p[2])
    
#########################################################################
def p_bracket_exp(p):
    '''
    exp : '[' exp ']'
    '''
    p[0] = ('bracket', p[2])
    
#########################################################################
def p_uminus_exp(p):
    '''
    exp : MINUS exp %prec UMINUS
    '''
    p[0] = ('uminus', p[2])

#########################################################################
def p_not_exp(p):
    '''
    exp : NOT exp
    '''
    p[0] = ('not', p[2])

#########################################################################
def p_opt_semi(p):
    '''
    opt_semi : ';'
             | empty
    '''
    pass

#########################################################################
def p_empty(p):
    '''
    empty :
    '''
    p[0] = ('nil',)

#########################################################################
def p_error(t):
    print("Syntax error at '%s'" % t.value)

#########################################################################
# build the parser
#########################################################################
parser = yacc.yacc(debug=False,tabmodule='cuppa3parsetab')

