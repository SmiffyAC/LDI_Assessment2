# IMPORTS
from string_with_arrows import *
from lexer import Lexer
from parser import Parser
from errors import *
from values import *
from interpreter import Interpreter
from shared import RTResult
from built_ins import *
from symbol_table import SymbolTable, Context

import string
import os
import math


# RUN

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
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
global_symbol_table.set("index", BuiltInFunction.index)
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