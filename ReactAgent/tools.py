from langchain.tools import tool, BaseTool

@tool
def multiply(a: float, b: float) -> float:
    """ Use this tool when you need to multiply two numbers (a and b) and get the result.
    Args: 
        a: Float multiplicand.
        b: Float multiplier.
        
        Returns:
        The product of a and b (a * b) as a float.
    """
    return a * b

@tool
def add(a: float, b: float) -> float:
    """ Use this tool when you need to add two numbers (a and b) and get the result.
    Args: 
        a: Float addend.
        b: Float addend.
        
        Returns:
        The sum of a and b (a + b) as a float.
    """
    return a + b

@tool 
def subtract(a: float, b: float) -> float:
    """ Use this tool when you need to subtract two numbers (a and b) and get the result.
    Args: 
        a: Float minuend.
        b: Float subtrahend.
        
        Returns:
        The difference of a and b (a - b) as a float.
    """
    return a - b

@tool
def divide(a: float, b: float) -> float:
    """ Use this tool when you need to divide two numbers (a and b) and get the result.
    Args: 
        a: Float dividend.
        b: Float divisor.
        
        Returns:
        The quotient of a and b (a / b) as a float. If b is zero, returns "Error: Division by zero".
    """
    if b == 0:
        raise ValueError("Error: Division by zero")
    return a / b 


TOOLS: list[BaseTool] = [multiply, divide, add, subtract]
TOOL_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}