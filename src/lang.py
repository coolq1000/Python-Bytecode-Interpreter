from lark import Lark, Transformer
import sys, argparse, json

class Refine(Transformer):

    def expr_add(self, args):
        out = {
            'type': 'add',
            'left': args[0],
            'right': args[1]
        }
        return out

    def expr_sub(self, args):
        out = {
            'type': 'sub',
            'left': args[0],
            'right': args[1]
        }
        return out
    
    def expr_mul(self, args):
        out = {
            'type': 'mul',
            'left': args[0],
            'right': args[1]
        }
        return out

    def expr_div(self, args):
        out = {
            'type': 'div',
            'left': args[0],
            'right': args[1]
        }
        return out
    
    def expr_eql(self, args):
        out = {
            'type': 'eql',
            'left': args[0],
            'right': args[1]
        }
        return out

    def expr_neq(self, args):
        out = {
            'type': 'neq',
            'left': args[0],
            'right': args[1]
        }
        return out
    
    def expr_geq(self, args):
        out = {
            'type': 'geq',
            'left': args[0],
            'right': args[1]
        }
        return out

    def expr_leq(self, args):
        out = {
            'type': 'leq',
            'left': args[0],
            'right': args[1]
        }
        return out
    
    def expr_gre(self, args):
        out = {
            'type': 'gre',
            'left': args[0],
            'right': args[1]
        }
        return out

    def expr_les(self, args):
        out = {
            'type': 'les',
            'left': args[0],
            'right': args[1]
        }
        return out

    def expr_num(self, args):
        out = {
            'type': 'number',
            'value': float(args[0].value) if not args[0].value.isdigit() else int(args[0].value)
        }
        return out
    
    def expr_str(self, args):
        out = {
            'type': 'string',
            'value': args[0].value
        }
        return out
    
    def expr_tru(self, args):
        out = {
            'type': 'bool',
            'value': True
        }
        return out
    
    def expr_fal(self, args):
        out = {
            'type': 'bool',
            'value': False
        }
        return out
    
    def expr_name(self, args):
        out = {
            'type': 'expr_name',
            'name': args[0]['name']
        }
        return out
    
    def expr_call(self, args):
        out = {
            'type': 'call',
            'name': args[0]['name'],
            'params': args[1].children
        }
        return out
    
    def expr_array(self, args):
        out = {
            'type': 'array',
            'elements': args[0].children
        }
        return out
    
    def stmt_if(self, args):
        out = {
            'type': 'if',
            'cond': args[0],
            'body': args[1]
        }
        return out
    
    def stmt_while(self, args):
        out = {
            'type': 'while',
            'cond': args[0],
            'body': args[1]
        }
        return out
    
    def stmt_fn(self, args):
        out = {
            'type': 'fn',
            'params': args[1],
            'name': args[0],
            'body': args[2]
        }
        return out

    def stmt_ret(self, args):
        out = {
            'type': 'ret',
            'value': args[0] if args else None
        }
        return out
    
    def stmt_assign(self, args):
        out = {
            'type': 'assign',
            'name': args[0],
            'value': args[1]
        }
        return out
    
    def stmt_closure(self, args):
        out = args
        return out

    def stmt_expr(self, args):
        out = {
            'type': 'expr',
            'expression': args[0]
        }
        return out
    
    def name(self, args):
        out = {
            'type': 'name',
            'name': args[0].value
        }
        return out
    

class OSXLang:

    def t_if(self, args):
        body = '\n'.join(args['body']) if type(args['body']) is list else args['body']
        out = '{}\nNOT_COND_JUMP {}\n{}'.format(
            args['cond'],
            len(body.split('\n') if type(body) is not list else body),
            body
        )
        return out

    def t_while(self, args):
        body = '\n'.join(args['body']) if type(args['body']) is list else args['body']
        cond = '\n'.join(args['cond']) if type(args['cond']) is list else args['cond']
        b_length = (len(body.split('\n') if type(body) is not list else body)) + 2
        c_length = (len(cond.split('\n') if type(cond) is not list else cond))
        out = '{}\nNOT_COND_JUMP {}\n{}\nJUMP {}'.format(
            args['cond'],
            b_length,
            body,
            -(b_length + c_length)
        )
        return out
    
    def t_fn(self, args):
        body = '\n'.join(args['body']) if type(args['body']) is list else args['body']
        argLen = len(body.split('\n') if type(body) is not list else body) + len(args['params'].children) + 1
        out = 'PUSH_NAME {}\nFUNCTION {}{}{}\n{}\nRETURN'.format(
            args['name'],
            argLen,
            '\n' if len(args['params'].children) else '',
            '\n'.join(['STORE_NAME ' + x['name'] for x in args['params'].children]),
            body
        )
        return out
    
    def t_ret(self, args):
        return '{}\nRETURN'.format(args['value'] if args['value'] else '')
    
    def t_assign(self, args):
        out = '{}\nSTORE_NAME {}'.format(
            args['value'],
            args['name']
        )
        return out

    def t_add(self, args):
        out = '{}\n{}\nBINARY_ADD'.format(args['left'], args['right'])
        return out

    def t_sub(self, args):
        out = '{}\n{}\nBINARY_SUB'.format(args['left'], args['right'])
        return out

    def t_mul(self, args):
        out = '{}\n{}\nBINARY_MUL'.format(args['left'], args['right'])
        return out

    def t_div(self, args):
        out = '{}\n{}\nBINARY_DIV'.format(args['left'], args['right'])
        return out
    
    def t_eql(self, args):
        out = '{}\n{}\nBINARY_EQL'.format(args['left'], args['right'])
        return out

    def t_neq(self, args):
        out = '{}\n{}\nBINARY_NEQ'.format(args['left'], args['right'])
        return out
    
    def t_geq(self, args):
        out = '{}\n{}\nBINARY_GEQ'.format(args['left'], args['right'])
        return out

    def t_leq(self, args):
        out = '{}\n{}\nBINARY_LEQ'.format(args['left'], args['right'])
        return out
    
    def t_gre(self, args):
        out = '{}\n{}\nBINARY_GRE'.format(args['left'], args['right'])
        return out

    def t_les(self, args):
        out = '{}\n{}\nBINARY_LES'.format(args['left'], args['right'])
        return out
    
    def t_expr(self, args):
        return args['expression']
    
    def t_number(self, args):
        out = 'PUSH_CONST {}'.format(args['value'])
        return out
    
    def t_string(self, args):
        out = 'PUSH_STRING {}'.format(args['value'])
        return out
    
    def t_bool(self, args):
        out = 'PUSH_CONST {}'.format(1 if args['value'] else 0)
        return out

    def t_expr_name(self, args):
        return 'PUSH_NAME {}'.format(args['name'])

    def t_name(self, args):
        return args['name']
    
    def t_call(self, args):
        out = 'PUSH_NAME {}\n{}\nCALL_FUNCTION {}'.format(
            args['name'],
            '\n'.join(args['params']),
            len(args['params'])
        )
        return out
    
    def t_array(self, args):
        out = '{}\nPUSH_ARRAY {}'.format('\n'.join(args['elements']), len(args['elements']))
        return out

    def transform(self, RAST):
        if type(RAST) is list:
            out = []
            for node in RAST:
                out.append(self.transform(node))
            return out
        elif type(RAST) is dict:
            for key, item in zip(list(RAST.keys()), list(RAST.values())):
                RAST[key] = self.transform(item)
            if 'type' in RAST:
                if hasattr(self, 't_' + RAST['type']):
                    return getattr(self, 't_' + RAST['type'])(RAST)
            else:
                return RAST
        return RAST

    def parse(self, RAST):
        bytecode = self.transform(RAST)
        return '\n'.join(bytecode).split('\n')

class OSXLVM:

    def __init__(self):
        self.variables = {}
        self.stack = []
        self.callStack = [0]
        self.builtins = {
            'PUSH_CONST': self._PUSH_CONST,
            'PUSH_NAME': self._PUSH_NAME,
            'PUSH_STRING': self._PUSH_STRING,
            'PUSH_ARRAY': self._PUSH_ARRAY,
            'STORE_NAME': self._STORE_NAME,
            'BINARY_ADD': self._BINARY_ADD,
            'BINARY_SUB': self._BINARY_SUB,
            'BINARY_MUL': self._BINARY_MUL,
            'BINARY_DIV': self._BINARY_DIV,
            'BINARY_EQL': self._BINARY_EQL,
            'BINARY_NEQ': self._BINARY_NEQ,
            'BINARY_GEQ': self._BINARY_GEQ,
            'BINARY_LEQ': self._BINARY_LEQ,
            'BINARY_GRE': self._BINARY_GRE,
            'BINARY_LES': self._BINARY_LES,
            'NOT_COND_JUMP': self._NOT_COND_JUMP,
            'JUMP': self._JUMP,
            'FUNCTION': self._FUNCTION,
            'CALL_FUNCTION': self._CALL_FUNCTION,
            'RETURN': self._RETURN
        }

        self.stdlib = {
            'print': self._STD_PRINT
        }
    
    def _PUSH_CONST(self, args):
        self.stack.append(float(args[0]) if not args[0].isdigit() else int(args[0]))
    
    def _PUSH_NAME(self, args):
        if args[0] in self.variables:
            args[0] = self.variables[args[0]]
        self.stack.append(args[0])
    
    def _PUSH_STRING(self, args):
        self.stack.append(' '.join(args))
    
    def _PUSH_ARRAY(self, args):
        self.stack.append(list(reversed([self.stack.pop() for x in range(int(args[0]))])))
    
    def _STORE_NAME(self, args):
        self.variables[args[0]] = self.stack.pop()

    def _BINARY_ADD(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(right + left)
    
    def _BINARY_SUB(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(right - left)
    
    def _BINARY_MUL(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(right * left)
    
    def _BINARY_DIV(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(right / left)
    
    def _BINARY_EQL(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if right == left else 0)
    
    def _BINARY_NEQ(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if right != left else 0)
    
    def _BINARY_GEQ(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if right >= left else 0)
    
    def _BINARY_LEQ(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if right <= left else 0)
    
    def _BINARY_GRE(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if right > left else 0)
    
    def _BINARY_LES(self, args):
        left, right = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if right < left else 0)
    
    def _NOT_COND_JUMP(self, args):
        if not self.stack.pop():
            self.callStack[-1] += int(args[0])
    
    def _JUMP(self, args):
        self.callStack[-1] += int(args[0])

    def _FUNCTION(self, args):
        self.variables[self.stack.pop()] = self.getPC()
        self.callStack[-1] += int(args[0])

    def _CALL_FUNCTION(self, args):
        numberArguments = int(args[0])
        arguments = list(reversed([self.stack.pop() for a in range(numberArguments)]))
        ind = self.stack.pop()
        if ind in list(self.variables.values()):
            fnName = list(self.variables.keys())[list(self.variables.values()).index(ind)]
            for arg in arguments:
                self.stack.append(arg)
            self.callStack.append(self.variables[fnName])
        elif ind in self.stdlib:
            self.stdlib[ind](arguments)

    def _RETURN(self, args):
        self.callStack.pop()
    
    def _STD_PRINT(self, args):
        print(' '.join([str(x[1:-1] if type(x) is str else x) for x in args]))

    def getPC(self):
        return self.callStack[-1]

    def execute(self, bytecode, debug=False):
        while self.getPC() < len(bytecode):
            ln = bytecode[self.getPC()].split(' ')
            op, args = ln[0], ln[1:]
            if op:
                if debug:
                    print('---\nOP: {}\nARGS: {}\nSTACK: {}\nPC: {}'.format(op, args, self.stack, self.callStack))

                if op in self.builtins:
                    self.builtins[op](args)
                else:
                    print('VM_ERROR: Encountered unknown instruction `{}`.'.format(op))
                    exit()
            self.callStack[-1] += 1
        if debug:
            print('END: STACK:', self.stack, self.variables)
