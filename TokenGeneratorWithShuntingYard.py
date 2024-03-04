# This file is used to generate tokens from the arithmetic in the txt file

def classify_character(char):
    """
    Classifies the character into one of the categories: 'digit', 'operation', 'space', or 'unknown'.
    Identifies specific arithmetic symbols as operations.

    :param char: A single character string to classify.
    :return: A string representing the character's classification or the specific operation.
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
    elif char == '=':
        return 'equals'
    else:
        return 'unknown'


def read_arithmetic_file(file_name):
    try:
        with open(file_name, 'r') as file:
            contents = file.read()
            print(f"Content of {file_name}: {contents}")
            return contents
    except FileNotFoundError:
        return "File not found."

def tokenize_arithmetic(content):
    """
    Tokenizes the arithmetic content into numbers and operators.
    """
    tokens = []
    num = ''
    for char in content:
        if char.isdigit():
            num += char  # Build up the number string
        else:
            if num:
                tokens.append(num)  # Append the complete number
                num = ''  # Reset number string
            if char in "+-*/=":  # Directly append operators
                tokens.append(char)
    if num:  # Append any number left in the buffer
        tokens.append(num)
    return tokens

def shunting_yard(tokens):
    """
    Converts a list of tokens into postfix notation using the Shunting Yard algorithm.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []  # Operator stack
    output = []  # Output list
    for token in tokens:
        if token.isdigit():  # Directly append numbers to the output
            output.append(token)
        elif token in precedence:
            while (stack and stack[-1] != '=' and
                   precedence[token] <= precedence.get(stack[-1], 0)):
                output.append(stack.pop())
            stack.append(token)
        elif token == '=':  # Equality sign treated as right parenthesis
            while stack:
                output.append(stack.pop())
    while stack:  # Pop any remaining operators
        output.append(stack.pop())
    return output

def evaluate_postfix(postfix):
    """
    Evaluates a postfix expression using a stack.

    :param postfix: A list of strings representing the postfix expression.
    :return: The result of the expression.
    """
    stack = []
    for token in postfix:
        if token.isdigit():
            stack.append(int(token))
        else:
            num2 = stack.pop()
            num1 = stack.pop()
            if token == '+':
                stack.append(num1 + num2)
            elif token == '-':
                stack.append(num1 - num2)
            elif token == '*':
                stack.append(num1 * num2)
            elif token == '/':
                stack.append(num1 / num2)
    return stack.pop()

if __name__ == "__main__":
    file_name = "arithmetic.txt"
    content = read_arithmetic_file(file_name)
    tokens = tokenize_arithmetic(content)
    print(f"Tokens: {tokens}")
    postfix = shunting_yard(tokens)
    print(f"Postfix: {' '.join(postfix)}")
    result = evaluate_postfix(postfix)
    print(f"Result: {result}")



