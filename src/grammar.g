
start: statement*

// Expressions
?expression: expr_gre
    | expr_les
    | expr_eql
    | expr_neq
    | expr_geq
    | expr_leq
    | expr_add
    | expr_sub
    | expr_mul
    | expr_div
    | expr_cap
    | expr_num
    | expr_str
    | expr_tru
    | expr_fal
    | expr_name
    | expr_call
    | expr_array

expr_add: expression "+" expression
expr_sub: expression "-" expression
expr_mul: expression "*" expression
expr_div: expression "/" expression
expr_gre: expression ">" expression
expr_les: expression "<" expression
expr_eql: expression "==" expression
expr_neq: expression "!=" expression
expr_geq: expression ">=" expression
expr_leq: expression "<=" expression
expr_cap: "(" expression ")"
expr_num: NUMBER
expr_str: STRING
expr_tru: "true"
expr_fal: "false"
expr_name: name
expr_call: expression "(" args ")"
expr_array: "[" args "]"

// Statements
?statement: stmt_if
    | stmt_while
    | stmt_fn
    | stmt_ret
    | stmt_assign
    | stmt_closure
    | stmt_expr

stmt_if: "if" "(" expression ")" statement

stmt_while: "while" "(" expression ")" statement

stmt_fn: "function" name "(" params ")" statement

stmt_ret: "return" expression? ";"

stmt_assign: name "=" expression ";"

stmt_closure: "{" statement* "}"

stmt_expr: expression ";"

params: [name ("," name)*]
args: [expression ("," expression)*]
name: CNAME

%import common.WS
%import common.ESCAPED_STRING -> STRING
%import common.SIGNED_NUMBER -> NUMBER
%import common.CNAME

%ignore WS
