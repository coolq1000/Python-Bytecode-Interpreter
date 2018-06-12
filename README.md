# Python-Bytecode-Interpreter

PBI is a simple bytecode interpreter that I created to see if I could progress past a tree-walker interpreter.

>*PBI is written for Python3 only*

## Command line
```
usage: main.py [-h] [-b B] input_file

PBI is a simple bytecode interpreter that I created to see if I could progress past a tree-walker interpreter.

positional arguments:
  input_file  The path to the target file to be compiled and executed.

optional arguments:
  -h, --help  show this help message and exit
  -b B        Output the bytecode to target path.
```

## Sample use
`python3 main.py examples/example.osxl`

## Example code
```JS
function cube(x)
{
    return x * x * x;
}

print(cube(3));
```

`>>> 27`

## Known issues
 1. Arithmetic Order Of Operations is not correct.

## Dependencies
 - Lark (`pip3 install lark-parser`)
