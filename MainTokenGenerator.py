# BOOK TO READ:
# Crafting Interpreters
# Sections 1-10
#--------------------------------------------
# THIS FILE INCLUDES:
# Shunting Yard
# Tokenization
# Evaluation of the postfix expression
# Incorporates floats
# SHOULD BE AROUND 40% MARK
#--------------------------------------------
# TO ADD:
# Add NULL
# Add variables


def read_arithmetic_file(file_name):
    """
    Reads the content of a file with the given name.

    Parameters:
        file_name (str): The name of the file to be read.

    Returns:
        str: The content of the file as a string, or "File not found." if the file does not exist.

    """
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()  # Read and return lines
            print(f"Content of {file_name}:\n{''.join(lines)}")
            return lines
    except FileNotFoundError:
        return "File not found."
    

def tokenize_arithmetic(content):
    """
    Tokenize arithmetic expressions.

    This function takes a string of arithmetic content and breaks it down into a list of Lexeme objects.
    Each Lexeme object represents a token in the content.

    Parameters:
        content (str): The arithmetic content to tokenize.

    Returns:
        list: A list of Lexeme objects representing the tokens in the content.

    """

    tokens = []
    num = ''
    line = 1  # Example line number handling; you'll need to adjust this based on actual content lines
    i = 0
    while i < len(content):
        char = content[i]

        # Handle numbers (int and float)
        if char.isdigit() or char == '.':
            num += char
            # Peek ahead to see if next character continues the number
            if i + 1 < len(content) and (content[i + 1].isdigit() or content[i + 1] == '.'):
                i += 1
                continue
            # Determine if the number is int or float
            if '.' in num:
                tokens.append(Lexeme(line, 'float', num))
            else:
                tokens.append(Lexeme(line, 'int', num))
            num = ''  # Reset number buffer

        if char == '"':
            i += 1
            start = i
            while i < len(content) and content[i] != '"':
                i += 1
            tokens.append(Lexeme(line, 'string', '"' + content[start:i] + '"'))

        elif char in "+-*/()=&|<>!":
            if char in "=<>!" and i < len(content) - 1 and content[i + 1] == '=':
                token = char + content[i + 1]
                i += 1
            else:
                token = char
            tokens.append(Lexeme(line, 'operator', token))

        elif content[i:i+4].upper() == 'TRUE' or content[i:i+5].upper() == 'FALSE':
            token = content[i:i+4].upper() if content[i:i+4].upper() == 'TRUE' else content[i:i+5].upper()
            tokens.append(Lexeme(line, 'boolean', token))
            i += len(token) - 1  # Adjust index based on token length

        # New handling for identifiers and assignments
        if char.isalpha():  # Simple check for variable name (identifier) start
            start = i
            while i + 1 < len(content) and (content[i + 1].isalnum() or content[i + 1] == '_'):
                i += 1
            identifier = content[start:i+1]
            tokens.append(Lexeme(line, 'identifier', identifier))

        i += 1

    if num:  # If there's a number left at the end
        tokens.append(Lexeme(line, 'number', num))

    return tokens
    
class Lexeme:
    def __init__(self, line, token_type, value, name=None, variable_type=None):
        self.line = line
        self.token_type = token_type
        self.value = value
        self.name = name
        self.variable_type = variable_type

    def __repr__(self):
        return f"Lexeme(line={self.line}, token_type='{self.token_type}', value={self.value}, name='{self.name}', variable_type='{self.variable_type}')"


# Dictionary to store the variables
variables = {}

def shunting_yard(tokens, variables):
    output_queue = []
    operator_stack = []
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '>=': 1, '==': 1, '!=': 1, '!': 4, '&': 0, '|': -1, '>': 1, '<': 1, '=': -2}
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '>=': 'L', '==': 'L', '!=': 'L', '!': 'R', '&': 'L', '|': 'L', '>': 'L', '<': 'L', '=': 'R'}

    for lexeme in tokens:
        token = lexeme.value
        if lexeme.token_type in ['int', 'float', 'boolean', 'string', 'identifier']:
            output_queue.append(lexeme)
        elif token in precedence:
            while operator_stack and operator_stack[-1].value != '(' and (
                (associativity[token] == 'L' and precedence[token] <= precedence[operator_stack[-1].value]) or
                (associativity[token] == 'R' and precedence[token] < precedence[operator_stack[-1].value])
            ):
                output_queue.append(operator_stack.pop())
            operator_stack.append(lexeme)
        elif token == '(':
            operator_stack.append(lexeme)
        elif token == ')':
            while operator_stack and operator_stack[-1].value != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue


def evaluate_postfix(postfix, variables):
    stack = []
    for lexeme in postfix:
        token = lexeme.value  # Extract the value for comparison and operation
        print(f"Token: {token}\n")
        if token == 'TRUE':
            stack.append(lexeme)
        elif token == 'FALSE':
            stack.append(lexeme)
        elif token.replace('.', '', 1).isdigit():
            stack.append(Lexeme(lexeme.line, 'float' if '.' in token else 'int', token))
        # Hanlde strings
        elif lexeme.token_type == 'string':
            stack.append(lexeme)
        elif token in ['+', '-', '*', '/', '>=', '<=', '>', '<', '==', '!=', '&', '|']:
            # Ensure there are at least two values on the stack for binary operators
            if len(stack) < 2:
                print("STACK AT ERROR: ", stack)
                raise ValueError("Insufficient values in the expression for binary operation.")
            rhv = stack.pop()
            lhv = stack.pop()

            # Perform the operation based on the token and push the result back on the stack
            if token == '+':
                # Check the types of the operands to determine whether to add or concatenate using lexeme.token_type
                if lhv.token_type == 'string' and rhv.token_type == 'string':
                    # String concatenation
                    # Remove the quotes from the string
                    lhv.value = lhv.value.strip('"')
                    rhv.value = rhv.value.strip('"')
                    concatenateed = '"' + lhv.value + rhv.value + '"'
                    # Append the concatenated string to the stack
                    stack.append(Lexeme(lhv.line, 'string', concatenateed))
                elif lhv.token_type == 'int' and rhv.token_type == 'int':
                    # Integer addition
                    stack.append(Lexeme(lhv.line, 'int', int(lhv.value) + int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    # Float addition
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) + float(rhv.value)))
                else:
                    raise ValueError(f"Invalid operands for the + operator: {lhv} and {rhv}")
                

            elif token == '-':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    # Integer subtraction
                    stack.append(Lexeme(lhv.line, 'int', int(lhv.value) - int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    # Float subtraction
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) - float(rhv.value)))
                else:
                    raise ValueError(f"Invalid operands for the - operator: {lhv} and {rhv}")

            elif token == '*':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'int', int(lhv.value) * int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) * float(rhv.value)))
                else:
                    raise ValueError(f"Invalid operands for the * operator: {lhv} and {rhv}")

            elif token == '/':
                if rhv == 0:
                    raise ZeroDivisionError("division by zero")
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'int', int(lhv.value) / int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) / float(rhv.value)))
                elif (lhv.token_type == "int" and rhv.token_type=="float") or (lhv.token_type == "float" and rhv.token_type=="int"):
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) / float(rhv.value)))
                else:
                    raise ValueError(f"Invalid operands for the / operator: {lhv} and {rhv}")

            elif token == '>=':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) >= int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) >= float(rhv.value)))
                elif (lhv.token_type == "int" and rhv.token_type=="float") or (lhv.token_type == "float" and rhv.token_type=="int"):
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) >= float(rhv.value)))
                else:
                    raise ValueError(f"Invalid operands for the >= operator: {lhv} and {rhv}")

            elif token == '<=':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) <= int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) <= float(rhv.value)))
                elif (lhv.token_type == "int" and rhv.token_type=="float") or (lhv.token_type == "float" and rhv.token_type=="int"):
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) <= float(rhv.value)))
                else:
                    raise ValueError(f"Invalid operands for the <= operator: {lhv} and {rhv}")

            elif token == '>':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) > int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) > float(rhv.value)))
                elif (lhv.token_type == "int" and rhv.token_type=="float") or (lhv.token_type == "float" and rhv.token_type == "int"):
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) > float(rhv.value)))
                else:
                    raise ValueError(f"Invalid operands for the > operator: {lhv} and {rhv}")

            elif token == '<':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) < int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) < float(rhv.value)))
                elif (lhv.token_type == "int" and rhv.token_type == "float") or (lhv.token_type == "float" and rhv.token_type == "int"):
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) < float(rhv.value)))
                else:
                    raise ValueError(f"Invalid operands for the < operator: {lhv} and {rhv}")

            elif token == '==':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) == int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) == float(rhv.value)))
                elif (lhv.token_type == "int" and rhv.token_type== "float") or (lhv.token_type == "float" and rhv.token_type == "int"):
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) == float(rhv.value)))
                elif lhv.token_type == "string" and rhv.token_type=="string":
                    stack.append(Lexeme(lhv.line, 'boolean', str(lhv.value) == str(rhv.value)))
                elif lhv.token_type == "boolean" and rhv.token_type== "boolean":
                    stack.append(Lexeme(lhv.line, 'boolean', lhv.value == rhv.value))
                else:
                    raise ValueError(f"Invalid operands for the == operator: {lhv} and {rhv}")

            elif token == '!=':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) != int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) != float(rhv.value)))
                elif lhv.token_type == "string" and rhv.token_type=="string":
                    stack.append(Lexeme(lhv.line, 'boolean', str(lhv.value) != str(rhv.value)))
                elif lhv.token_type == "boolean" and rhv.token_type=="boolean":
                    stack.append(Lexeme(lhv.line, 'boolean', lhv.value != rhv.value))
                else:
                    raise ValueError(f"Invalid operands for the != operator: {lhv} and {rhv}")

            elif token == '&':
                if lhv.token_type == 'boolean' and rhv.token_type == 'boolean':
                    stack.append(Lexeme(lhv.line, 'boolean', lhv.value and rhv.value))
                else:
                    raise ValueError("Invalid operands for the AND operator.")

            elif token == '|':
                if lhv.token_type == 'boolean' and rhv.token_type == 'boolean':
                    # NOTE: False | True is = to False - NOT SURE WHY?!
                    BLHV = BRHV = False
                    if lhv.value == "TRUE":
                        BLHV = True
                    if rhv.value == "TRUE":
                        BRHV = True

                    stack.append(Lexeme(lhv.line, 'boolean', str(BLHV or BRHV)))
                else:
                    raise ValueError("Invalid operands for the OR operator.")

        elif token == '!':
            # Ensure there is at least one value on the stack for unary operation
            if not stack:
                raise ValueError("Insufficient values in the expression for unary operation.")
            val = stack.pop()
            stack.append(Lexeme(val.line, 'boolean', not val.value))

        elif lexeme.token_type == 'identifier':
            # Push variable value if exists, else push variable name for later assignment
            if token in variables:
                # NOTE: This is a simple implementation that assumes all variables are integers!!!
                # Get the type of the variable
                variable_type_local = 'int'
                # Get the variable value from the variables dictionary
                stack.append(Lexeme(lexeme.line, token_type=variable_type_local, value=variables[token], name=token, variable_type=variable_type_local))
            else:
                stack.append(Lexeme(lexeme.line, 'identifier', token, name=token))
        elif token == '=':
            # Handle assignment
            if len(stack) < 2:
                raise ValueError("Insufficient values for assignment.")
            value_lexeme = stack.pop()
            variable_lexeme = stack.pop()
            if variable_lexeme.token_type != 'identifier':
                raise ValueError(f"Invalid assignment target: {variable_lexeme}")
            # Update the variables dictionary
            variables[variable_lexeme.value] = value_lexeme.value
            # Update the variable type
            variable_lexeme.variable_type = value_lexeme.token_type
            # Push the assignment result back to stack if needed
            stack.append(value_lexeme)
        else:
            raise ValueError(f"Unknown token: {lexeme}")
        

    if len(stack) != 1:
        raise ValueError("The expression is invalid.")
    return stack[0].value


if __name__ == "__main__":
    #file_name = "arithmetic.txt"
    # file_name = "stringTest.txt"
    file_name = "testing.txt"

    lines = read_arithmetic_file(file_name)
    for line in lines:
        print(f"Line: {line}")
        tokens = tokenize_arithmetic(line.strip())  # Ensure to strip newline characters
        if tokens:  # Check if line is not empty
            print(f"Tokens: {tokens}")
            postfix = shunting_yard(tokens, variables)
            print(f"Postfix: {' '.join(repr(lexeme) for lexeme in postfix)}")
            result = evaluate_postfix(postfix, variables)
            print(f"Variables: {variables}")
            print(f"Result: {result}\n")
