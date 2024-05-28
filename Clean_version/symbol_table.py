# CONTEXT

class Context:
  # Represents the execution context for a block of code, such as a function or loop.
  def __init__(self, display_name, parent=None, parent_entry_pos=None):
    self.display_name = display_name # Name to display for the context (e.g. function name)
    self.parent = parent # Parent context (e.g., the context from which the function was called)
    self.parent_entry_pos = parent_entry_pos # The position in the code where the parent context was entered
    self.symbol_table = None # Symbol table for identifiers


# SYMBOL TABLE

class SymbolTable:
  # Represents a symbol table that maps variable names to their values.
  def __init__(self, parent=None):
    self.symbols = {} # A dictionary that maps identifiers to their values
    self.parent = parent # Parent symbol table (for nested scopes)

  def get(self, name):
    # Retrieves the value of a variable by name.
    # If the variable is not found in the current symbol table, it checks the parent symbol table.
    value = self.symbols.get(name, None)
    if value == None and self.parent:
      return self.parent.get(name)
    return value

  def set(self, name, value):
    # Sets the value of a variable in the symbol table.
    self.symbols[name] = value

  def remove(self, name):
    # Removes a variable from the symbol table.
    del self.symbols[name]