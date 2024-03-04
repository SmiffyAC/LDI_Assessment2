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
            contents = file.read()
            print(f"Content of {file_name}: {contents}")
            return contents
    except FileNotFoundError:
        return "File not found."
    

def tokenize_arithmetic(content):
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
            token = content[i:i+4] if content[i:i+4].upper() == 'TRUE' else content[i:i+5]
            tokens.append(Lexeme(line, 'boolean', token))
            i += len(token) - 1  # Adjust index based on token length
        # elif content[i:i+4].upper() == 'TRUE' or content[i:i+5].upper() == 'FALSE':
        #     token_value = content[i:i+4].upper() if content[i:i+4].upper() == 'TRUE' else content[i:i+5].upper()
        #     tokens.append(Lexeme(line, 'boolean', token))
        #     i += len(token_value) - 1

        i += 1

    if num:  # If there's a number left at the end
        tokens.append(Lexeme(line, 'number', num))

    return tokens

# CAN MERGE THIS IWHT LEXEME CLASS - ADD VARIABLE TYPE AND VARIABLE NAME
# WHEN FINDING A VARIABLE, ADD IT TO A DICTIONARY
# IF I FIND VARIABLE NAME, REPLACE IT WITH THE VALUE
# IF I FIND A VARIABLE NAME, AND IT IS NOT IN THE DICTIONARY, THROW AN ERROR
# ADD FOR RIGHT HAND SIDE AND LEFT HAND SIDE
class Variable:
    # Use this when implementing variables
    def __init__(self, name, variable_type, value):
        self.name = name
        self.variable_type = variable_type
        self.value = value

    def __repr__(self):
        return f"Variable(name='{self.name}', variable_type='{self.variable_type}' ,value={self.value})"


class Lexeme:
    def __init__(self, line, token_type, value):
        self.line = line
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f"Lexeme(line={self.line}, token_type='{self.token_type}', value='{self.value}')"


def shunting_yard(tokens):
    output_queue = []
    operator_stack = []
    # Updated precedence to reflect correct handling, especially for '>=', '==', and '!'
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '>=': 1, '==': 1, '!': 4, '&': 0, '|': -1, '>': 1, '<': 1}
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '>=': 'L', '==': 'L', '!': 'R', '&': 'L', '|': 'L', '>': 'L', '<': 'L'}

    for lexeme in tokens:
        token = lexeme.value  # Use the value of the Lexeme object
        # if token.replace('.', '', 1).isdigit() or token in ['TRUE', 'FALSE', '"']:  # Check if the token is a digit, TRUE, FALSE, or a string
        #     output_queue.append(lexeme)  # Append the Lexeme object directly
        if lexeme.token_type in ['int', 'float', 'boolean', 'string']:
            output_queue.append(lexeme)  # Append the Lexeme object directly
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
            operator_stack.pop()  # Remove '('
    while operator_stack:
        output_queue.append(operator_stack.pop())
    
    return output_queue



def evaluate_postfix(postfix):
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
                    stack.append(Lexeme(lhv.line, 'string', concatenateed))
                elif lhv.token_type == 'int' and rhv.token_type == 'int':
                    # Integer addition
                    stack.append(Lexeme(lhv.line, 'int', int(lhv.value) + int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    # Float addition
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) + float(rhv.value)))
                elif (lhv.token_type == "boolean" and rhv.token_type=="boolean"):
                    # Throw an error
                    # raise ValueError(f"Invalid operands for the + operator: {lhv} and {rhv}")
                    pass # decide how to handle string and other type additions
                else:
                    raise ValueError(f"Invalid operands for the + operator: {lhv} and {rhv}")
                

            elif token == '-':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'int', int(lhv.value) - int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) - float(rhv.value)))
                elif lhv.token_type == "string" or rhv.token_type=="string":        
                    pass # decide how to handle string and other type additions 
                elif lhv.token_type == "boolean" or rhv.token_type=="boolean":        
                    pass # decide how to handle string and other type additions

            elif token == '*':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'int', int(lhv.value) * int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) * float(rhv.value)))
                elif lhv.token_type == "string" or rhv.token_type=="string":        
                    pass # decide how to handle string and other type additions
                elif lhv.token_type == "boolean" or rhv.token_type=="boolean":
                    pass # decide how to handle string and other type additions

            elif token == '/':
                if rhv == 0:
                    raise ZeroDivisionError("division by zero")
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'int', int(lhv.value) / int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) / float(rhv.value)))
                elif lhv.token_type == "int" or rhv.token_type=="float" or lhv.token_type == "float" or rhv.token_type=="int":
                    stack.append(Lexeme(lhv.line, 'float', float(lhv.value) / float(rhv.value)))
                elif lhv.token_type == "string" or rhv.token_type=="string":
                    pass # decide how to handle string and other type additions
                elif lhv.token_type == "boolean" or rhv.token_type=="boolean":
                    pass # decide how to handle string and other type additions

            elif token == '>=':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) >= int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) >= float(rhv.value)))
                elif lhv.token_type == "int" or rhv.token_type=="float" or lhv.token_type == "float" or rhv.token_type=="int":
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) >= float(rhv.value)))
                elif lhv.token_type == "string" or rhv.token_type=="string":
                    pass # decide how to handle string and other type additions
                elif lhv.token_type == "boolean" or rhv.token_type=="boolean":
                    pass # decide how to handle string and other type additions

            elif token == '<=':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) <= int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) <= float(rhv.value)))
                elif (lhv.token_type == "int" and rhv.token_type=="float") or (lhv.token_type == "float" and rhv.token_type=="int"):
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) <= float(rhv.value)))
                elif lhv.token_type == "string" or rhv.token_type=="string":
                    pass # decide how to handle string and other type additions
                elif lhv.token_type == "boolean" or rhv.token_type=="boolean":
                    pass # decide how to handle string and other type additions

            elif token == '>':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) > int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) > float(rhv.value)))
                elif lhv.token_type == "int" or rhv.token_type=="float" or lhv.token_type == "float" or rhv.token_type=="int":
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) > float(rhv.value)))
                elif lhv.token_type == "string" or rhv.token_type=="string":
                    pass # decide how to handle string and other type additions
                elif lhv.token_type == "boolean" or rhv.token_type=="boolean":
                    pass # decide how to handle string and other type additions

            elif token == '<':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) < int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) < float(rhv.value)))
                elif lhv.token_type == "int" or rhv.token_type=="float" or lhv.token_type == "float" or rhv.token_type=="int":
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) < float(rhv.value)))
                elif lhv.token_type == "string" or rhv.token_type=="string":
                    pass # decide how to handle string and other type additions
                elif lhv.token_type == "boolean" or rhv.token_type=="boolean":
                    pass # decide how to handle string and other type additions

            elif token == '==':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) == int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) == float(rhv.value)))
                elif lhv.token_type == "string" and rhv.token_type=="string":
                    stack.append(Lexeme(lhv.line, 'boolean', str(lhv.value) == str(rhv.value)))
                elif lhv.token_type == "boolean" and rhv.token_type=="boolean":
                    stack.append(Lexeme(lhv.line, 'boolean', bool(lhv.value) == bool(rhv.value)))

            elif token == '!=':
                if lhv.token_type == 'int' and rhv.token_type == 'int':
                    stack.append(Lexeme(lhv.line, 'boolean', int(lhv.value) != int(rhv.value)))
                elif lhv.token_type == 'float' and rhv.token_type == 'float':
                    stack.append(Lexeme(lhv.line, 'boolean', float(lhv.value) != float(rhv.value)))
                elif lhv.token_type == "string" and rhv.token_type=="string":
                    stack.append(Lexeme(lhv.line, 'boolean', str(lhv.value) != str(rhv.value)))
                elif lhv.token_type == "boolean" and rhv.token_type=="boolean":
                    stack.append(Lexeme(lhv.line, 'boolean', bool(lhv.value) != bool(rhv.value)))

            elif token == '&':
                if lhv.token_type == 'boolean' and rhv.token_type == 'boolean':
                    stack.append(Lexeme(lhv.line, 'boolean', lhv.value and rhv.value))
                else:
                    raise ValueError("Invalid operands for the AND operator.")

            elif token == '|':
                if lhv.token_type == 'boolean' and rhv.token_type == 'boolean':
                    stack.append(Lexeme(lhv.line, 'boolean', lhv.value or rhv.value))
                else:
                    raise ValueError("Invalid operands for the OR operator.")

        elif token == '!':
            # Ensure there is at least one value on the stack for unary operation
            if not stack:
                raise ValueError("Insufficient values in the expression for unary operation.")
            val = stack.pop()
            stack.append(Lexeme(val.line, 'boolean', not val.value))
        else:
            raise ValueError(f"Unknown token: {lexeme}")
    if len(stack) != 1:
        raise ValueError("The expression is invalid.")
    return stack[0].value



def classify_character(char):
    """
    Classifies a given character based on its type or value.

    Parameters:
        char (str): The character to be classified.

    Returns:
        str: A string representing the character's classification. This can be 'digit', 'space', 'addition', 
        'subtraction', 'multiplication', 'division', 'and', 'or', 'not', 'not equal to', 'greater than', 
        'greater than or equal to', 'less than', 'less than or equal to', 'equal to', 'equals', or 'unknown'.
    """

    if char.isdigit():
        return 'digit'
    elif char.isspace():
        return 'space'
    elif char == '+':
        return 'addition'
    elif char == '-':
        return 'subtraction'
    elif char == '*':
        return 'multiplication'
    elif char == '/':
        return 'division'
    # AND, OR, NOT
    elif char == '&':
        return 'and'
    elif char == '|':
        return 'or'
    # >, >=, <, <=, ==, !=
    elif char == '!':
        # check for not
        if char == '=':
            return 'not equal to'
        else:
            return 'not'
    elif char == '>':
        # Check for greater than or equal to
        if char == '=':
            return 'greater than or equal to'
        else:
            return 'greater than'
    elif char == '<':
        # Check for less than or equal to
        if char == '=':
            return 'less than or equal to'
        else:
            return 'less than'
    elif char == '=':
        # Check for equal to
        if char == '=':
            return 'equal to'
        else:
            return 'equals'
    else:
        return 'unknown'



if __name__ == "__main__":
    #file_name = "arithmetic.txt"
    # file_name = "stringTest.txt"
    file_name = "testing.txt"
    content = read_arithmetic_file(file_name)
    tokens = tokenize_arithmetic(content)
    print(f"Tokens: {tokens}")
    postfix = shunting_yard(tokens)
    print(f"Postfix: {' '.join(repr(lexeme) for lexeme in postfix)}")
    result = evaluate_postfix(postfix)
    print(f"\nResult: {result}\n")
