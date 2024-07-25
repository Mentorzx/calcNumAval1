# README

Este README é composto por duas partes: uma em inglês e uma em português. A seção em inglês está acima e a seção em português está abaixo.

---

## English

### Overview

This script, named `avaliacao1.py`, implements several numerical methods to find roots of functions. The methods included are:

1. **Bisection Method** - Finds a root by repeatedly dividing the interval in half.
2. **Fixed Point Method** - Finds a root by iteratively applying a function.
3. **Newton-Raphson Method** - Finds a root using the derivative of the function.

### Functions

- **`eval_func(x, func_str)`**: Evaluates a function at a given point.
- **`eval_func_derivative(x, func_str, h=1e-5)`**: Evaluates the derivative of a function using numerical differentiation.
- **`bisection_method(lower_bound, upper_bound, tolerance, f_func_str)`**: Finds a root using the Bisection Method.
- **`fixed_point_method(initial_guess, tolerance, max_iterations, f_func_str, g_func_str)`**: Finds a root using the Fixed Point Iteration Method.
- **`newton_raphson_method(initial_guess, tolerance, max_iterations, f_func_str)`**: Finds a root using the Newton-Raphson Method.
- **`get_input(prompt, default_value, value_type)`**: Prompts the user for input and converts it to the specified type.
- **`get_user_input(patterns)`**: Gets input from the user for function definitions and parameters.
- **`print_results(method_name, func_str, results)`**: Prints the results of the method.

### Legal Notice

This script is provided "as is" without any warranties. The authors are not liable for any damages arising from the use of this script.

### Running the Script

To run the script, execute it directly. It will prompt you to enter values for function specifications and parameters or use default values. The results for each method will be displayed.

---

**Note:** The README will be updated to include future tests scripts.

---

## Português

### Visão Geral

Este script, chamado `avaliacao1.py`, implementa vários métodos numéricos para encontrar raízes de funções. Os métodos incluídos são:

1. **Método da Bisseção** - Encontra uma raiz dividindo repetidamente o intervalo ao meio.
2. **Método do Ponto Fixo** - Encontra uma raiz aplicando iterativamente uma função.
3. **Método de Newton-Raphson** - Encontra uma raiz usando a derivada da função.

### Funções

- **`eval_func(x, func_str)`**: Avalia uma função em um ponto dado.
- **`eval_func_derivative(x, func_str, h=1e-5)`**: Avalia a derivada de uma função usando diferenciação numérica.
- **`bisection_method(lower_bound, upper_bound, tolerance, f_func_str)`**: Encontra uma raiz usando o Método da Bisseção.
- **`fixed_point_method(initial_guess, tolerance, max_iterations, f_func_str, g_func_str)`**: Encontra uma raiz usando o Método de Iteração de Ponto Fixo.
- **`newton_raphson_method(initial_guess, tolerance, max_iterations, f_func_str)`**: Encontra uma raiz usando o Método de Newton-Raphson.
- **`get_input(prompt, default_value, value_type)`**: Solicita ao usuário uma entrada e converte-a para o tipo especificado.
- **`get_user_input(patterns)`**: Obtém entradas do usuário para definições e parâmetros de funções.
- **`print_results(method_name, func_str, results)`**: Imprime os resultados do método.

### Aviso Legal

Este script é fornecido "como está" sem garantias. Os autores não são responsáveis por quaisquer danos decorrentes do uso deste script.

### Execução do Script

Para executar o script, execute-o diretamente. Ele solicitará que você insira valores para especificações de funções e parâmetros ou use valores padrão. Os resultados para cada método serão exibidos.

---

**Nota:** O README será atualizado para incluir futuros scripts de avaliações.
