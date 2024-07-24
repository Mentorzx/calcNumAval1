x = 3;
tol = 1e-6;

function main(x, tol)
  e = 1;
  n = 1;
  e_x_previo = 0;
  while true
    e_x_previo = e;
    e = e + x^n / factorial(n);
    if abs((e - e_x_previo) / e) < tol
      break;
    endif
    n = n + 1;
  endwhile
  fprintf("e^%.2f = %.20f (n = %d)\n", x, e, n);
endfunction

main(x, tol);