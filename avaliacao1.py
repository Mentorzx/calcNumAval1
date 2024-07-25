import math


def eval_func(x, func_str):
    """
    Evaluate the function provided by the user at a given point x.

    Parameters:
    x (float): The input value for which the function is evaluated.
    func_str (str): The function as a string, where 'x' is used as the variable.

    Returns:
    float: The result of the function evaluation.
    """
    return eval(func_str.replace("x", str(x)))


def eval_func_derivative(x, func_str, h=1e-5):
    """
    Evaluate the derivative of the function provided by the user at a given point x
    using numerical differentiation.

    Parameters:
    x (float): The input value for which the derivative is evaluated.
    func_str (str): The function as a string, where 'x' is used as the variable.
    h (float): The step size for numerical differentiation.

    Returns:
    float: The result of the derivative evaluation.
    """
    # Calculate the derivative using the finite difference method
    f_x_plus_h = eval_func(x + h, func_str)
    f_x_minus_h = eval_func(x - h, func_str)
    return (f_x_plus_h - f_x_minus_h) / (2 * h)


def bisection_method(lower_bound, upper_bound, tolerance, f_func_str):
    """
    Find a root of the function using the Bisection Method.

    Parameters:
    lower_bound (float): The lower bound of the interval where the root is to be found.
    upper_bound (float): The upper bound of the interval where the root is to be found.
    tolerance (float): The stopping criterion for the root-finding process.
    f_func_str (str): The function f(x) as a string, where 'x' is used as the variable.

    Returns:
    tuple: A tuple containing:
        - best_guess (float): The estimated root of the function.
        - iterations_done (int): The number of iterations performed.
        - stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_lower = lower_bound
    current_upper = upper_bound
    max_iterations = math.ceil(math.log2(abs(upper_bound - lower_bound) / tolerance))

    for i in range(1, max_iterations + 1):
        current_bisection = (current_lower + current_upper) / 2
        func_value = eval_func(current_bisection, f_func_str)

        if abs(func_value) < tolerance:
            return current_bisection, i, "Exact root found"
        elif eval_func(current_lower, f_func_str) * func_value < 0:
            current_upper = current_bisection
        else:
            current_lower = current_bisection

    return current_bisection, i, "Maximum iterations reached"


def fixed_point_method(
    initial_guess, tolerance, max_iterations, f_func_str, g_func_str
):
    """
    Find a root of the function using the Fixed Point Iteration Method.

    Parameters:
    initial_guess (float): The initial guess for the root.
    tolerance (float): The stopping criterion for the root-finding process.
    max_iterations (int): The maximum number of iterations.
    f_func_str (str): The function f(x) as a string, where 'x' is used as the variable.
    g_func_str (str): The function g(x) as a string, where 'x' is used as the variable.

    Returns:
    tuple: A tuple containing:
        - best_guess (float): The estimated root of the function.
        - iterations_done (int): The number of iterations performed.
        - stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_guess = initial_guess

    for i in range(1, max_iterations + 1):
        next_guess = eval_func(current_guess, g_func_str)
        func_value = eval_func(next_guess, f_func_str)

        if abs(next_guess - current_guess) < tolerance:
            return next_guess, i, "Converged to the fixed point"
        if abs(func_value) < tolerance:
            return next_guess, i, "Approximate root found"

        current_guess = next_guess

    return next_guess, i, "Maximum iterations reached"


def newton_raphson_method(initial_guess, tolerance, max_iterations, f_func_str):
    """
    Find a root of the function using the Newton-Raphson Method.

    Parameters:
    initial_guess (float): The initial guess for the root.
    tolerance (float): The stopping criterion for the root-finding process.
    max_iterations (int): The maximum number of iterations.
    f_func_str (str): The function f(x) as a string, where 'x' is used as the variable.

    Returns:
    tuple: A tuple containing:
        - best_guess (float): The estimated root of the function.
        - iterations_done (int): The number of iterations performed.
        - stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_guess = initial_guess

    for i in range(1, max_iterations + 1):
        func_value = eval_func(current_guess, f_func_str)
        derivative_value = eval_func_derivative(current_guess, f_func_str)

        if derivative_value == 0:
            return current_guess, i, "Derivative is zero, method fails"
        next_guess = current_guess - func_value / derivative_value

        if abs(next_guess - current_guess) < tolerance:
            return next_guess, i, "Converged to the root"
        current_guess = next_guess

    return next_guess, i, "Maximum iterations reached"


def get_input(prompt, default_value, value_type):
    """
    Prompt the user for input and return the value converted to the specified type.

    Parameters:
        prompt (str): The prompt message to display to the user.
        default_value: The default value to return if the user provides no input.
        value_type (type): The type to which the input should be converted (e.g., str, float).

    Returns:
        The user input converted to the specified type, or the default value if no input is provided.
    """

    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            return default_value
        try:
            return value_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {value_type.__name__}.")


def get_user_input(patterns):
    """
    Get input from the user for function definitions and parameters and return patterns if first input is empty.

    Returns:
        dict: A dict containing:
            - f_func_str (str): The function f(x) as a string.
            - g_func_str (str): The function (gx) as a string for the fixed point iteration.
            - lower_bound (float): Lower bound for the Bisection Method.
            - upper_bound (float): Upper bound for the Bisection Method.
            - tolerance (float): Tolerance for the methods.
            - initial_guess (float): Initial guess for the Fixed Point Method.
            - max_iterations (int): Maximum number of iterations for the Fixed Point Method.
    """

    input_prompts = {
        "f_func_str": [
            "Enter the function f(x) in terms of x (e.g., x**2 - 4) or press 'Enter' to use patterns: ",
            patterns["f_func_str"],
            str,
        ],
        "g_func_str": [
            "Enter the function g(x) for the Fixed Point Method (e.g., x/2 + 1): ",
            patterns["g_func_str"],
            str,
        ],
        "lower_bound": [
            "Enter the lower bound for the Bisection Method: ",
            patterns["lower_bound"],
            float,
        ],
        "upper_bound": [
            "Enter the upper bound for the Bisection Method: ",
            patterns["upper_bound"],
            float,
        ],
        "tolerance": [
            "Enter the tolerance for the methods: ",
            patterns["tolerance"],
            float,
        ],
        "initial_guess": [
            "Enter the initial guess for the Fixed Point and Newton-Raphson Methods: ",
            patterns["initial_guess"],
            float,
        ],
        "max_iterations": [
            "Enter the maximum number of iterations for the Fixed Point and Newton-Raphson Methods: ",
            patterns["max_iterations"],
            int,
        ],
    }

    for key, value in input_prompts.items():
        input_prompts[key] = get_input(*value)

        if input_prompts[key] == value[1]:
            input_prompts = {
                k: (v[1] if i > 0 else v)
                for i, (k, v) in enumerate(input_prompts.items())
            }
            break

    return input_prompts


def print_results(method_name, func_str, results):
    """
    Print the results of the method.

    Parameters:
    method_name (str): The name of the method.
    func_str (str): The function as a string, where 'x' is used as the variable.
    results (tuple): The results to be printed.
    """
    print(f"\n{method_name} Results:")
    print(f"Function: {func_str}")
    print(f"Root: {results[0]}")
    print(f"Iterations: {results[1]}")
    print(f"Stop Reason: {results[2]}")


if __name__ == "__main__":
    """
    Main entry point for the script. This block of code executes when the script is run directly.

    It performs the following steps:
    1. Defines default values for function specifications and parameters.
    2. Prompts the user to input values for function specifications and parameters using `get_user_input`.
    3. Sets up a dictionary of methods (Bisection Method, Fixed Point Method, and Newton-Raphson Method), each associated with a lambda function for execution.
    4. Iterates over the dictionary of methods, executes each method with the provided specifications, and prints the results using `print_results`.

    The script allows the user to test different root-finding methods by providing their own functions and parameters or using default values.
    """

    specs_patterns = {
        "f_func_str": "x**2 - 4",
        "g_func_str": "x/2 + 1",
        "lower_bound": 0,
        "upper_bound": 3,
        "tolerance": 0.01,
        "initial_guess": 3.0,
        "max_iterations": 10,
    }
    specs = get_user_input(specs_patterns)
    methods = {
        "Bisection Method": lambda: bisection_method(
            specs["lower_bound"],
            specs["upper_bound"],
            specs["tolerance"],
            specs["f_func_str"],
        ),
        "Fixed Point Method": lambda: fixed_point_method(
            specs["initial_guess"],
            specs["tolerance"],
            specs["max_iterations"],
            specs["f_func_str"],
            specs["g_func_str"],
        ),
        "Newton-Raphson Method": lambda: newton_raphson_method(
            specs["initial_guess"],
            specs["tolerance"],
            specs["max_iterations"],
            specs["f_func_str"],
        ),
    }

    for method_name, method_func in methods.items():
        func_str = (
            specs["f_func_str"]
            if method_name != "Fixed Point Method"
            else specs["g_func_str"]
        )
        results = method_func()
        print_results(method_name, func_str, results)
