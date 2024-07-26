from typing import Any, Optional
from math import ceil, log2, sqrt


def eval_func(func_str: str, x: Optional[float] = None) -> float:
    """
    Evaluate the function provided by the user at a given point x.

    Parameters:
        x (float): The input value for which the function is evaluated.
        func_str (str): The function as a string, where 'x' is used as the variable.

    Returns:
        float: The result of the function evaluation.
    """

    return (
        eval(
            func_str.replace("x", str(x)),
            {"__builtins__": None},
            {"sqrt": sqrt},
        )
        if x is not None
        else -1
    )


def eval_func_derivative(func_str: str, x: float, h: float = 1e-5) -> float:
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
    f_x_plus_h = eval_func(func_str, x + h)
    f_x_minus_h = eval_func(func_str, x - h)
    return (f_x_plus_h - f_x_minus_h) / (2 * h)


def calculate_errors(current_value: float, previous_value: float | None) -> list[float]:
    """
    Calculate the absolute and relative errors.

    Parameters:
        current (float): The current estimate of the root.
        previous (float | None): The previous estimate of the root.

    Returns:
        list: A list containing the Absolute Error and the Relative Error.
    """
    abs_error = abs(current_value - previous_value) if previous_value else float("inf")
    rel_error = (
        abs_error / abs(current_value) if abs(current_value) != 0 else float("inf")
    )
    return [abs_error, rel_error]


def bisection_method(
    f_func_str: str,
    lower_bound: float,
    upper_bound: float,
    tolerance: float,
    max_iterations: int,
) -> tuple[float, list[float], int, str]:
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
            errors (list[float]): A list containing the Absolute Error and the Relative Error.
            iterations_done (int): The number of iterations performed.
            stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_lower = lower_bound
    current_upper = upper_bound
    previous_bisection = None
    bisection_iterations = ceil(log2(abs(upper_bound - lower_bound) / tolerance))

    if bisection_iterations < max_iterations:
        max_iterations = bisection_iterations
        stop_reason = "Tolerance reached"
    else:
        stop_reason = "Maximum iterations reached"

    for i in range(1, max_iterations + 1):
        current_bisection = (current_lower + current_upper) / 2
        f_of_bisection = eval_func(f_func_str, current_bisection)
        f_of_lower = eval_func(f_func_str, current_lower)

        if f_of_bisection == 0:
            return current_bisection, [0.0, 0.0], i, "Exact root found"
        elif f_of_lower == 0:
            return current_lower, [0.0, 0.0], i, "Exact root found"
        elif f_of_lower * f_of_bisection < 0:
            current_upper = current_bisection
        else:
            current_lower = current_bisection
        errors = calculate_errors(current_bisection, previous_bisection)
        previous_bisection = current_bisection

        if errors[0] < tolerance:
            return current_bisection, errors, i, "Converged to tolerance"

    return current_bisection, errors, i, stop_reason


def fixed_point_method(
    f_func_str: str,
    g_func_str: str,
    tolerance: float,
    initial_guess: float,
    max_iterations: int,
) -> tuple[float, list[float], int, str]:
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
            errors (list[float]): A list containing the Absolute Error and the Relative Error.
            iterations_done (int): The number of iterations performed.
            stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_guess = initial_guess

    for i in range(1, max_iterations + 1):
        next_guess = eval_func(g_func_str, current_guess)
        func_value = eval_func(f_func_str, next_guess)
        errors = calculate_errors(next_guess, current_guess)

        if errors[0] < tolerance:
            return next_guess, errors, i, "Converged to the fixed point"
        if abs(func_value) < tolerance:
            return next_guess, errors, i, "Approximate root found"
        current_guess = next_guess

    return next_guess, errors, i, "Maximum iterations reached"


def newton_raphson_method(
    f_func_str: str, tolerance: float, initial_guess: float, max_iterations: int
) -> tuple[float, list[float], int, str]:
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
            errors (list[float]): A list containing the Absolute Error and the Relative Error.
            iterations_done (int): The number of iterations performed.
            stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_guess = initial_guess

    for i in range(1, max_iterations + 1):
        func_value = eval_func(f_func_str, current_guess)
        derivative_value = eval_func_derivative(f_func_str, current_guess)

        if derivative_value == 0:
            return (
                current_guess,
                [float("inf"), float("inf")],
                i,
                "Derivative is zero, method fails",
            )
        next_guess = current_guess - func_value / derivative_value
        errors = calculate_errors(next_guess, current_guess)

        if errors[0] < tolerance:
            return next_guess, errors, i, "Converged to the root"
        current_guess = next_guess

    return next_guess, errors, i, "Maximum iterations reached"


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
            str,
            patterns["f_func_str"],
        ],
        "g_func_str": [
            "Enter the function g(x) for the Fixed Point Method (e.g., x/2 + 1): ",
            str,
            patterns["g_func_str"],
        ],
        "lower_bound": [
            "Enter the lower bound for the Bisection Method: ",
            float,
            patterns["lower_bound"],
        ],
        "upper_bound": [
            "Enter the upper bound for the Bisection Method: ",
            float,
            patterns["upper_bound"],
        ],
        "tolerance": [
            "Enter the tolerance for the methods: ",
            float,
            patterns["tolerance"],
        ],
        "initial_guess": [
            "Enter the initial guess for the Fixed Point Method: ",
            float,
            patterns["initial_guess"],
        ],
        "max_iterations": [
            "Enter the maximum number of iterations of Methods: ",
            int,
            patterns["max_iterations"],
        ],
    }

    print(
        "Warning: This code does not handle all possible input errors. Please ensure that your inputs are valid to avoid potential issues such as calculating the square root of a negative number, division by zero, or other out-of-scope errors. Input validation is the user's responsibility."
    )
    for key, value in input_prompts.items():
        user_input = get_input(*value[:-1])
        if user_input == "":
            return {k: v[2] for k, v in input_prompts.items()}
        input_prompts[key] = user_input

    return input_prompts


def print_results(
    method_name: str,
    func_str: str,
    results: tuple[float, list[float], int, str],
) -> None:
    """
    Print the results of the method including magnitude of error and relative error if true_value is provided.

    Parameters:
        method_name (str): The name of the method.
        func_str (str): The function as a string, where 'x' is used as the variable.
        true_roots (list): The true values of the roots for error calculation.
        results (tuple): The results to be printed.
    """

    root, errors, iterations, stop_reason = results

    print(f"\n{method_name} Results:")
    print(f"Function: {func_str}")
    print(f"Root reached: {root}")
    print(f"Absolute Error: {errors[0]}")
    print(f"Relative Error: {errors[1]}")
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
            ((specs["lower_bound"] + specs["upper_bound"]) / 2),
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
        print_results(method_name, func_str, results)
