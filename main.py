from src.lang import *
import argparse

if __name__ == '__main__':

    # Parse arguments,
    aparser = argparse.ArgumentParser(description='''
PBI is a simple bytecode interpreter that I created to see if I could progress past a tree-walker interpreter.
''')
    aparser.add_argument('input_file', help='The path to the target file to be compiled and executed.')
    aparser.add_argument('-b', help='Output the bytecode to target path.')
    args = aparser.parse_args()

    grammar, code = None, None
    with open('src/grammar.g') as f:
        grammar = f.read()
    with open(args.input_file) as f:
        code = f.read()
    
    osxlParser = Lark(grammar, parser='lalr')
    AST = osxlParser.parse(code)
    #print('AST:', AST)
    refined = Refine().transform(AST)
    #print('AST Refined:', refined)
    bytecode = OSXLang().parse(refined.children)
    if args.b:
        print('\n'.join(bytecode), file=open(args.b, 'w'))
    OSXLVM().execute(bytecode)
