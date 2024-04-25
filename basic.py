# Import all the necessary modules
from parser_1 import *
from lexer import *
from interpreter import *
from context import *
from values import *
from builtins import *
from errors import *
from nodes import *
from position import *
from tokens import *
from runtime_result import *
from symbolTable import *


#######################################
# RUN
#######################################

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
# global_symbol_table.set("False", Number.false)
# global_symbol_table.set("True", Number.true)
global_symbol_table.set("False", Boolean(False))
global_symbol_table.set("True", Boolean(True))
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("print_ret", BuiltInFunction.print_ret)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("run", BuiltInFunction.run)

def run(fn, text):
  # Generate tokens
  lexer = Lexer(fn, text)
  tokens, error = lexer.make_tokens()
  if error: return None, error
  
  # Generate AST
  parser = Parser(tokens)
  ast = parser.parse()
  if ast.error: return None, ast.error

  # Run program
  interpreter = Interpreter()
  context = Context('<program>')
  context.symbol_table = global_symbol_table
  result = interpreter.visit(ast.node, context)

  return result.value, result.error