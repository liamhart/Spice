# grammar for Cuppa3

from ply import yacc
from cuppa3_lex import tokens, lexer

# set precedence and associativity
# NOTE: all arithmetic operator need to have tokens
#       so that we can put them into the precedence table
precedence = (
              ('left', 'EQ', 'LE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
              ('right', 'UMINUS', 'NOT')
             )


def p_grammar(_):
    '''
    program : stmt_list

    stmt_list : stmt stmt_list
              | empty

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

    opt_formal_args : formal_args
                    | empty

    formal_args : ID ',' formal_args
                | ID

    opt_contents : contents
                 | empty
                 
    contents : exp ',' contents
             | exp
    
    opt_init : '=' exp
             | empty
             
    opt_actual_args : actual_args
                    | empty
    
    actual_args : exp ',' actual_args
                | exp
                
    opt_exp : exp
            | empty

    opt_else : ELSE stmt
             | empty
             
    opt_semi : ';'
             | empty
            
    req_col : ':'
            | empty
             
    int_slice : INTEGER req_col INTEGER
              | INTEGER
              
    index_exp : INTEGER req_col INTEGER
              | INTEGER

    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp EQ exp
        | exp LE exp
        | INTEGER
        | INTEGER '[' int_slice ']'
        | ID
        | ID '(' opt_actual_args ')'
        | ID '[' index_exp ']'
        | '(' exp ')'
        | '[' exp ']'
        | MINUS exp %prec UMINUS
        | NOT exp
    '''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)

### build the parser
parser = yacc.yacc()




       
   
  
            






