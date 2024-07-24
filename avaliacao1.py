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


def bisection_method(lower_bound, upper_bound, tolerance, func_str):
    """
    Find a root of the function using the Bisection Method.

    Parameters:
    lower_bound (float): The lower bound of the interval where the root is to be found.
    upper_bound (float): The upper bound of the interval where the root is to be found.
    tolerance (float): The stopping criterion for the root-finding process.
    func_str (str): The function as a string, where 'x' is used as the variable.

    Returns:
    tuple: A tuple containing:
        - best_guess (float): The estimated root of the function.
        - iterations_done (int): The number of iterations performed.
        - stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_lower = lower_bound
    current_upper = upper_bound
    max_iterations = math.ceil(math.log2(abs(upper_bound - lower_bound) / tolerance))

    for iterations_done in range(max_iterations + 1):
        current_bisection = (current_lower + current_upper) / 2
        func_value = eval_func(current_bisection, func_str)

        if abs(func_value) < tolerance:
            return current_bisection, iterations_done, "Exact root found"

        if eval_func(current_lower, func_str) * func_value < 0:
            current_upper = current_bisection
        else:
            current_lower = current_bisection

    return current_bisection, iterations_done, "Maximum iterations reached"


def fixed_point_method(initial_guess, tolerance, max_iterations, func_str, g_func_str):
    """
    Find a root of the function using the Fixed Point Iteration Method.

    Parameters:
    initial_guess (float): The initial guess for the root.
    tolerance (float): The stopping criterion for the root-finding process.
    max_iterations (int): The maximum number of iterations.
    func_str (str): The function as a string, where 'x' is used as the variable.
    g_func_str (str): The function g(x) as a string, where 'x' is used as the variable.

    Returns:
    tuple: A tuple containing:
        - best_guess (float): The estimated root of the function.
        - iterations_done (int): The number of iterations performed.
        - stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_guess = initial_guess
    iterations_done = 0

    while True:
        next_guess = eval_func(current_guess, g_func_str)
        func_value = eval_func(next_guess, func_str)

        if abs(next_guess - current_guess) < tolerance:
            return next_guess, iterations_done, "Converged to the fixed point"

        if abs(func_value) < tolerance:
            return next_guess, iterations_done, "Approximate root found"

        if iterations_done > max_iterations:
            return next_guess, iterations_done, "Maximum iterations reached"

        current_guess = next_guess
        iterations_done += 1


def newton_raphson_method(initial_guess, tolerance, max_iterations, func_str):
    """
    Find a root of the function using the Newton-Raphson Method.

    Parameters:
    initial_guess (float): The initial guess for the root.
    tolerance (float): The stopping criterion for the root-finding process.
    max_iterations (int): The maximum number of iterations.
    func_str (str): The function as a string, where 'x' is used as the variable.

    Returns:
    tuple: A tuple containing:
        - best_guess (float): The estimated root of the function.
        - iterations_done (int): The number of iterations performed.
        - stop_reason (str): A message indicating why the algorithm stopped.
    """
    current_guess = initial_guess
    iterations_done = 0

    while True:
        func_value = eval_func(current_guess, func_str)
        derivative_value = eval_func_derivative(current_guess, func_str)

        if derivative_value == 0:
            return current_guess, iterations_done, "Derivative is zero, method fails"

        next_guess = current_guess - func_value / derivative_value

        if abs(next_guess - current_guess) < tolerance:
            return next_guess, iterations_done, "Converged to the root"

        if iterations_done >= max_iterations:
            return next_guess, iterations_done, "Maximum iterations reached"

        current_guess = next_guess
        iterations_done += 1


def get_user_input():
    """
    Get input from the user for function definitions and parameters.

    Returns:
    tuple: A tuple containing:
        - func_str (str): The function as a string.
        - g_func_str (str): The fixed point iteration function as a string.
        - lower_bound (float): Lower bound for the Bisection Method.
        - upper_bound (float): Upper bound for the Bisection Method.
        - tolerance (float): Tolerance for the methods.
        - initial_guess (float): Initial guess for the Fixed Point Method.
        - max_iterations (int): Maximum number of iterations for the Fixed Point Method.
    """
    func_str = input("Enter the function f(x) in terms of x (e.g., x**2 - 4): ")
    g_func_str = input(
        "Enter the function g(x) for the Fixed Point Method (e.g., x/2 + 1): "
    )

    lower_bound = float(input("Enter the lower bound for the Bisection Method: "))
    upper_bound = float(input("Enter the upper bound for the Bisection Method: "))
    tolerance = float(input("Enter the tolerance for the methods: "))

    initial_guess = float(
        input(
            "Enter the initial guess for the Fixed Point and Newton-Raphson Methods: "
        )
    )
    max_iterations = int(
        input(
            "Enter the maximum number of iterations for the Fixed Point and Newton-Raphson Methods: "
        )
    )

    return (
        func_str,
        g_func_str,
        lower_bound,
        upper_bound,
        tolerance,
        initial_guess,
        max_iterations,
    )


def print_results(method_name, results):
    """
    Print the results of the method.

    Parameters:
    method_name (str): The name of the method.
    results (tuple): The results to be printed.
    """
    print(f"\n{method_name} Results:")
    print(f"Root: {results[0]}")
    print(f"Iterations: {results[1]}")
    print(f"Stop Reason: {results[2]}")


if __name__ == "__main__":
    (
        func_str,
        g_func_str,
        lower_bound,
        upper_bound,
        tolerance,
        initial_guess,
        max_iterations,
    ) = get_user_input()

    methods = {
        "Bisection Method": lambda: bisection_method(
            lower_bound, upper_bound, tolerance, func_str
        ),
        "Fixed Point Method": lambda: fixed_point_method(
            initial_guess, tolerance, max_iterations, func_str, g_func_str
        ),
        "Newton-Raphson Method": lambda: newton_raphson_method(
            initial_guess, tolerance, max_iterations, func_str
        ),
    }

    for method_name, method_func in methods.items():
        results = method_func()
        print_results(method_name, results)
        
