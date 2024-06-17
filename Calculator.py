import re

def parse_expression(expression):
    if expression.count('(') != expression.count(')'):
        raise ValueError("Unbalanced parentheses in expression.")
    tokens = re.findall(r'[-+]?\d*\.?\d+|[^\d\s]', expression)
    return tokens

def Format(In):
    Equation = []
    Bracket = False
    Temp = []
    for i in range(len(In)):
        if In[i] == "(":
            Bracket = True
        elif In[i] == ")":
            Bracket = False
            Equation.append(Temp)
            Temp = []
        elif Bracket:
            Temp.append(In[i])
        else:
            Equation.append(In[i])

    Brackets(Equation)
    return Equation


def Brackets(Equation):
    for i in range(len(Equation)):
        if type(Equation[i]) == list:
            Equation[i] = Indicies(Equation[i])
            if len(Equation[i]) == 1:
                Equation[i] = str(Equation[i][0])

            Equation[i] = Divide(Equation[i])
            if len(Equation[i]) == 1:
                Equation[i] = str(Equation[i][0])

            Equation[i] = Multiply(Equation[i])
            if len(Equation[i]) == 1:
                Equation[i] = str(Equation[i][0])
            
            Equation[i] = Addition_Subtraction(Equation[i])
            if len(Equation[i]) == 1:
                Equation[i] = str(Equation[i][0])
        
    if "(" not in Equation:
        Equation = Indicies(Equation)

        Equation = Divide(Equation)

        Equation = Multiply(Equation)
        
        Equation = Addition_Subtraction(Equation)
    
    return Equation

def Indicies(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "^":
            Temp = float(Equation[i-1]) ** float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def Divide(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "/":
            if float(Equation[i+1]) == 0:
                raise ZeroDivisionError("Division by zero encountered.")
            Temp = float(Equation[i-1]) / float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def Multiply(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "*":
            Temp = float(Equation[i-1]) * float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def Addition(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "+":
            Temp = float(Equation[i-1]) + float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def Addition_Subtraction(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "-":
            Temp = float(Equation[i-1]) - float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        elif Equation[i] == "+":
            Temp = float(Equation[i-1]) + float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def main():
    while True:
        try:
            In = input("Enter Equation (type 'exit' to quit):\n>>>")
            if In.lower() == 'exit':
                break

            In = parse_expression(In)
            Output = Format(In)
            Output = Brackets(Output)

            print("Output = ", Output[0])
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()