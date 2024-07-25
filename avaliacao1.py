from sympy import symbols, solve, diff, Eq, sympify, Mul, Pow
from typing import Any, Optional
from math import ceil, log2, sqrt


def eval_func(func_str: str, x: Optional[float] = None) -> tuple[float, list[float]]:
    """
    Evaluate the function provided by the user at a given point x.

    Parameters:
        x (float): The input value for which the function is evaluated.
        func_str (str): The function as a string, where 'x' is used as the variable.

    Returns:
        float: The result of the function evaluation.        - list[float]: The list of roots of the function.
    """

    var = symbols("x")
    roots = solve(Eq(sympify(func_str), 0), var)
    roots_list = roots if isinstance((roots), list) else [roots]
    roots_list = [
        root.evalf() if isinstance(root, Mul | Pow) else root for root in roots_list
    ]
    func_value = (
        eval(func_str.replace("x", str(1)), {"__builtins__": None}, {"sqrt": sqrt})
        if x is not None
        else -1
    )

    return func_value, roots_list  # type: ignore


def eval_func_derivative(func_str: str, x: float, h: float = 1e-5):
    """
    Evaluate the derivative of the function provided by the user at a given point x
    using numerical differentiation.

    Parameters:
        x (float): The input value for which the derivative is evaluated.
        func_str (str): The function as a string, where 'x' is used as the variable.
        h (float): The step size for numerical differentiation.

    Returns:
        float: The result of the derivative evaluation.
        list[float]: The list of roots of the derivative.
    """

    # Calculate the derivative using the finite difference method
    f_x_plus_h = eval_func(func_str, x + h)[0]
    f_x_minus_h = eval_func(func_str, x - h)[0]
    func_value = (f_x_plus_h - f_x_minus_h) / (2 * h)
    var = symbols("x")
    roots = solve(Eq(diff(sympify(func_str)), 0), var)
    roots_list = roots if isinstance((roots), list) else [roots]
    roots_list = [
        root.evalf() if isinstance(root, Mul | Pow) else root for root in roots_list
    ]

    return func_value, roots_list


def relative_error(approx_value: float, true_value: float) -> float:
    """
    Calculate the relative error between an approximate value and the true value.

    Parameters:
        approx_value (float): The approximate value.
        true_value (float): The true value.

    Returns:
        float: The relative error.
    """
    return abs((approx_value - true_value) / true_value)


def bisection_method(
    f_func_str: str,
    lower_bound: float,
    upper_bound: float,
    tolerance: float,
    max_iterations: int,
) -> tuple[float, int, str]:
    """
    Find a root of the function using the Bisection Method.

    Parameters:
        lower_bound (float): The lower bound of the interval where the root is to be found.
        upper_bound (float): The upper bound of the interval where the root is to be found.
        tolerance (float): The stopping criterion for the root-finding process.
        max_iterations (int): The maximum number of iterations.
        f_func_str (str): The function f(x) as a string, where 'x' is used as the variable.

    Returns:
        tuple: A tuple containing:
            best_guess (float): The estimated root of the function.
            iterations_done (int): The number of iterations performed.
            stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_lower = lower_bound
    current_upper = upper_bound

    bisection_iterations = ceil(log2(abs(upper_bound - lower_bound) / tolerance))

    if bisection_iterations < max_iterations:
        max_iterations = bisection_iterations
        stop_reason = "Tolerance reached"
    else:
        stop_reason = "Maximum iterations reached"

    for i in range(1, max_iterations + 1):
        current_bisection = (current_lower + current_upper) / 2
        f_of_bisection = eval_func(f_func_str, current_bisection)[0]
        f_of_lower = eval_func(f_func_str, current_lower)[0]

        if f_of_bisection == 0:
            return current_bisection, i, "Exact root found"
        if f_of_lower == 0:
            return current_lower, i, "Exact root found"
        elif f_of_lower * f_of_bisection < 0:
            current_upper = current_bisection
        else:
            current_lower = current_bisection

    return current_bisection, i, stop_reason


def fixed_point_method(
    f_func_str: str,
    g_func_str: str,
    tolerance: float,
    initial_guess: float,
    max_iterations: int,
) -> tuple[float, int, str]:
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
            best_guess (float): The estimated root of the function.
            iterations_done (int): The number of iterations performed.
            stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_guess = initial_guess

    for i in range(1, max_iterations + 1):
        next_guess = eval_func(g_func_str, current_guess)[0]
        func_value = eval_func(f_func_str, next_guess)[0]

        if abs(next_guess - current_guess) < tolerance:
            return next_guess, i, "Converged to the fixed point"
        if abs(func_value) < tolerance:
            return next_guess, i, "Approximate root found"

        current_guess = next_guess

    return next_guess, i, "Maximum iterations reached"


def newton_raphson_method(
    f_func_str: str, tolerance: float, initial_guess: float, max_iterations: int
) -> tuple[float, int, str]:
    """
    Find a root of the function using the Newton-Raphson Method.

    Parameters:
        initial_guess (float): The initial guess for the root.
        tolerance (float): The stopping criterion for the root-finding process.
        max_iterations (int): The maximum number of iterations.
        f_func_str (str): The function f(x) as a string, where 'x' is used as the variable.

    Returns:
        tuple: A tuple containing:
            best_guess (float): The estimated root of the function.
            iterations_done (int): The number of iterations performed.
            stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_guess = initial_guess

    for i in range(1, max_iterations + 1):
        func_value = eval_func(f_func_str, current_guess)[0]
        derivative_value = eval_func_derivative(f_func_str, current_guess)[0]

        if derivative_value == 0:
            return current_guess, i, "Derivative is zero, method fails"
        next_guess = current_guess - func_value / derivative_value

        if abs(next_guess - current_guess) < tolerance:
            return next_guess, i, "Converged to the root"
        current_guess = next_guess

    return next_guess, i, "Maximum iterations reached"


def get_input(prompt: str, default_value: Any, value_type: type) -> Any:
    """
    Prompt the user for input and return the value converted to the specified type.

    Parameters:
        prompt (str): The prompt message to display to the user.
        default_value (Any): The default value to return if the user provides no input.
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


def get_user_input(
    patterns: dict[str, tuple[str, str, float, float, float, float, int]]
) -> dict[str, Any]:
    """
    Get input from the user for function definitions and parameters and return patterns if first input is empty.

    Parameters:
        patterns (dict): A dictionary of patterns to inputs.

    Returns:
        dict: A dict containing:
            f_func_str (str): The function f(x) as a string.
            g_func_str (str): The function (gx) as a string for the fixed point iteration.
            lower_bound (float): Lower bound for the Bisection Method.
            upper_bound (float): Upper bound for the Bisection Method.
            tolerance (float): Tolerance for the methods.
            initial_guess (float): Initial guess for the Fixed Point Method.
            max_iterations (int): Maximum number of iterations for the Fixed Point Method.
    """

    input_prompts = {
        "f_func_str": [
            "Enter the function f(x) in terms of x (e.g., x**2 - 3) or press 'Enter' to use patterns: ",
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
            "Enter the maximum number of iterations of Methods: ",
            patterns["max_iterations"],
            int,
        ],
    }

    for key, value in input_prompts.items():
        user_input = get_input(*value)
        if user_input == "":
            return {k: v[1] for k, v in input_prompts.items()}
        input_prompts[key] = user_input

    return input_prompts


def print_results(
    method_name: str,
    func_str: str,
    true_roots: list[float],
    results: tuple[float, int, str],
) -> None:
    """
    Print the results of the method including magnitude of error and relative error if true_value is provided.

    Parameters:
        method_name (str): The name of the method.
        func_str (str): The function as a string, where 'x' is used as the variable.
        true_roots (list): The true values of the roots for error calculation.
        results (tuple): The results to be printed.
    """

    root, iterations, stop_reason = results

    if not true_roots:
        magnitude_err = -1
        rel_err = -1
        stop_reason = "This function doesn’t have roots."
    else:
        if len(true_roots) == 1:
            true_root = true_roots[0]
        elif root >= 0:
            true_root = next((r for r in true_roots if r >= 0), None)
        else:
            true_root = next((r for r in true_roots if r < 0), None)

        magnitude_err = abs(root - true_root)  # type: ignore
        rel_err = relative_error(root, true_root)  # type: ignore

    print(f"\n{method_name} Results:")
    print(f"Function: {func_str}")
    print(f"Root reached: {root}")
    print(f"True root: {true_root if true_roots else 'N/A'}")
    print(f"Magnitude of Error: {magnitude_err}")
    print(f"Relative Error: {rel_err:.6f}")
    print(f"Iterations: {iterations}")
    print(f"Stop Reason: {stop_reason}")


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
        "f_func_str": "x**2 - 3",
        "g_func_str": "x/2 + 1",
        "lower_bound": 1,
        "upper_bound": 2,
        "tolerance": 0.01,
        "initial_guess": 3.0,
        "max_iterations": 5,
    }
    print("Warning: This code does not handle all possible input errors. Please ensure that your inputs are valid to avoid potential issues such as calculating the square root of a negative number, division by zero, or other out-of-scope errors. Input validation is the user's responsibility.")
    specs = get_user_input(specs_patterns)
    methods = {
        "Bisection Method": lambda: bisection_method(
            specs["f_func_str"],
            specs["lower_bound"],
            specs["upper_bound"],
            specs["tolerance"],
            specs["max_iterations"],
        ),
        "Fixed Point Method": lambda: fixed_point_method(
            specs["f_func_str"],
            specs["g_func_str"],
            specs["tolerance"],
            specs["initial_guess"],
            specs["max_iterations"],
        ),
        "Newton-Raphson Method": lambda: newton_raphson_method(
            specs["f_func_str"],
            specs["tolerance"],
            specs["initial_guess"],
            specs["max_iterations"],
        ),
    }

    for method_name, method_func in methods.items():
        func_str = (
            specs["f_func_str"]
            if method_name != "Fixed Point Method"
            else specs["g_func_str"]
        )
        results = method_func()
        true_root = eval_func(func_str)[1]
        print_results(method_name, func_str, true_root, results)
