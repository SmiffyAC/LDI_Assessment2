# This file is used to generate tokens from the arithmetic in the txt file

def read_arithmetic_file(file_name):
    try:
        with open(file_name, 'r') as file:
            contents = file.read()
            print(f"Content of {file_name}: {contents}")
            return contents
    except FileNotFoundError:
        return "File not found."


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


def tokenize_arithmetic(content):
    """
    Tokenizes the arithmetic content into different categories.

    :param content: String containing the arithmetic expression.
    :return: A dictionary with categorized tokens.
    """
    tokens = {
        'digits': [],
        'addition': [],
        'subtraction': [],
        'multiplication': [],
        'division': [],
        'equals': [],
        'spaces': [],
        'unknown': []
    }

    for position, char in enumerate(content):
        char_type = classify_character(char)
        if char_type in tokens:  # For known types, append the character or its position
            tokens[char_type].append((position, char))
        else:
            tokens['unknown'].append((position, char))

    return tokens

if __name__ == "__main__":
    file_name = "arithmetic.txt"  # Assuming the file is in the same directory
    content = read_arithmetic_file(file_name)

    tokens = tokenize_arithmetic(content)
    for token_type, token_list in tokens.items():
        print(f"{token_type.capitalize()}: {token_list}")


