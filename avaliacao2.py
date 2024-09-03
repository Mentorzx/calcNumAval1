from typing import Callable, Any, Dict


def trapezoidal_rule(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    """
    Calculate the integral of a function f(x) from a to b using the trapezoidal rule.

    Parameters:
    - f: function to integrate
    - a: lower bound of the integration
    - b: upper bound of the integration
    - n: number of intervals

    Returns:
    - float: approximated integral value
    """
    h = (b - a) / n
    integral = (f(a) + f(b)) / 2
    for i in range(1, n):
        integral += f(a + i * h)
    integral *= h
    return integral


def simpsons_one_third_rule(
    f: Callable[[float], float], a: float, b: float, n: int
) -> float:
    """
    Calculate the integral of a function f(x) from a to b using Simpson's 1/3 rule.

    Parameters:
    - f: function to integrate
    - a: lower bound of the integration
    - b: upper bound of the integration
    - n: number of intervals (must be even)

    Returns:
    - float: approximated integral value
    """
    if n % 2 != 0:
        raise ValueError("Number of intervals (n) must be even for Simpson's 1/3 rule.")

    h = (b - a) / n
    integral = f(a) + f(b)
    for i in range(1, n, 2):
        integral += 4 * f(a + i * h)
    for i in range(2, n - 1, 2):
        integral += 2 * f(a + i * h)
    integral *= h / 3
    return integral


def get_input(prompt: str, value_type: type) -> Any:
    """
    Prompt the user for input and return the value converted to the specified type.

    Parameters:
        prompt (str): The prompt message to display to the user.
        value_type (type): The type to which the input should be converted (e.g., str, float).

    Returns:
        The user input converted to the specified type, or the default value if no input is provided.
    """

    while True:
        user_input = input(prompt).strip()
        try:
            return value_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {value_type.__name__}.")


def get_user_input(patterns: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get input from the user for function definitions and parameters and return patterns if first input is empty.

    Parameters:
        patterns (dict): A dictionary of default patterns to inputs.

    Returns:
        dict: A dictionary containing user inputs or default patterns.
    """
    input_prompts = {
        "f": [
            "Enter the function f(x) in terms of x (e.g., x**2 - 3) or press 'Enter' to use default: ",
            str,
            patterns["f"],
        ],
        "a": [
            "Enter the lower bound (a): ",
            float,
            patterns["a"],
        ],
        "b": [
            "Enter the upper bound (b): ",
            float,
            patterns["b"],
        ],
        "n": [
            "Enter the number of intervals (n): ",
            int,
            patterns["n"],
        ],
    }

    print(
        "Warning: Please ensure that your inputs are valid to avoid potential issues such as calculating the square root of a negative number, division by zero, or other out-of-scope errors."
    )
    print("Input validation is the user's responsibility.\n")
    user_inputs = {}
    for key, value in input_prompts.items():
        user_input = get_input(*value[:-1])
        if user_input == "":
            print("Using default values...\n")
            user_inputs = {k: v[2] for k, v in input_prompts.items()}
            user_inputs["f"] = eval(f"lambda x: {user_inputs['f']}")
            return user_inputs
        input_prompts[key] = user_input

    user_inputs["f"] = eval(f"lambda x: {user_inputs['f']}")
    return user_inputs


def execute_methods(f: Callable[[float], float], a: float, b: float, n: int) -> None:
    """
    Executes the numerical integration methods and prints the results.

    Parameters:
    - f: function to integrate
    - a: lower bound of the integration
    - b: upper bound of the integration
    - n: number of intervals
    """
    methods = {
        "Trapezoidal Rule": lambda: trapezoidal_rule(f, a, b, n),
        "Simpson's 1/3 Rule": lambda: simpsons_one_third_rule(f, a, b, n),
    }

    for method_name, method_func in methods.items():
        result = method_func()
        print(f"{method_name} Result: {result}")


if __name__ == "__main__":
    """
    Main function that drives the numerical integration script.

    It performs the following steps:
    1. Defines default values for the function, lower bound, upper bound, and the number of intervals.
    2. Prompts the user to input values for the function, bounds, and intervals using `get_user_inputs`.
    3. Sets up two numerical integration methods (Trapezoidal Rule and Simpson's 1/3 Rule) with the provided specifications.
    4. Executes each method and prints the results of the integration.
    5. If an error occurs during execution, it prints an error message and prompts the user to correct the inputs before retrying.
    """
    default_values = {"f": "x**2", "a": 0.0, "b": 1.0, "n": 10}
    done = False
    while not done:
        try:
            user_inputs = get_user_input(default_values)
            execute_methods(**user_inputs)
            done = True
        except ValueError as e:
            print(f"Error: {e}")
        except SyntaxError as e:
            print(f"Syntax Error in function definition: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
