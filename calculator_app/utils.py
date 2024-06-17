def calculate_rpn(expression: str) -> float:
    stack = []
    for token in expression.split():
        if token in ["+", "-", "*", "/"]:
            operand2 = stack.pop()
            operand1 = stack.pop()
            if token == "+":
                result = operand1 + operand2
            elif token == "-":
                result = operand1 - operand2
            elif token == "*":
                result = operand1 * operand2
            elif token == "/":
                result = operand1 / operand2
            stack.append(result)
            
        else:
            stack.append(float(token))
            
    return stack.pop()