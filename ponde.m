iteracoes_desejadas = 10;
limite_inferior = 1;
limite_superior = 2;
tolerancia = 0.01;

function y = funcao_avaliada(x)
  y = (x*x) - 3;
endfunction

%{
Método da Bissecção
%}

function [melhor_palpite, iteracoes_efetuadas, motivo_parada] = metodo_bisseccao(limite_inferior_bisseccao, limite_superior_bisseccao, tolerancia_bisseccao)
  limite_inferior_atual = limite_inferior_bisseccao;
  limite_superior_atual = limite_superior_bisseccao;
  iteracoes_bisseccao = ceil(log2(abs(limite_superior_bisseccao-limite_inferior_bisseccao)/tolerancia_bisseccao));
  
  raiz_exata_achada = false;
  for i = 0:iteracoes_bisseccao
    iteracoes_efetuadas = i;
    bisseccao_atual = (limite_inferior_atual + limite_superior_atual)/2;

    if(abs(funcao_avaliada(bisseccao_atual)) < tolerancia)
      melhor_palpite = limite_inferior_atual;
      motivo_parada = 'Raiz exata encontrada';
      break;
    elseif (funcao_avaliada(limite_inferior_atual) * funcao_avaliada(bisseccao_atual) < 0)
      limite_superior_atual = bisseccao_atual;
    elseif (funcao_avaliada(limite_inferior_atual) * funcao_avaliada(bisseccao_atual) > 0)
      limite_inferior_atual = bisseccao_atual;
    else
      raiz_exata_achada = true;
      if(funcao_avaliada(bisseccao_atual) == 0)
        melhor_palpite = bisseccao_atual;
      else
        melhor_palpite = limite_inferior_atual;
      endif
        motivo_parada = 'Raiz exata encontrada';
      break;
    endif
  endfor

  if (!raiz_exata_achada)
    melhor_palpite = bisseccao_atual;
    motivo_parada = 'Número máximo de iterações atingido';
  endif
  
endfunction

%{
Método do Ponto Fixo
%}

function [melhor_palpite, iteracoes_efetuadas, motivo_parada] = metodo_bisseccao(limite_inferior_bisseccao, limite_superior_bisseccao, tolerancia_bisseccao)
  limite_inferior_atual = limite_inferior_bisseccao;
  limite_superior_atual = limite_superior_bisseccao;
  iteracoes_bisseccao = ceil(log2(abs(limite_superior_bisseccao-limite_inferior_bisseccao)/tolerancia_bisseccao));
  
  raiz_exata_achada = false;
  for i = 0:iteracoes_bisseccao
    iteracoes_efetuadas = i;
    bisseccao_atual = (limite_inferior_atual + limite_superior_atual)/2;
    
    if (funcao_avaliada(limite_inferior_atual) * funcao_avaliada(bisseccao_atual) < 0)
      limite_superior_atual = bisseccao_atual;
    elseif (funcao_avaliada(limite_inferior_atual) * funcao_avaliada(bisseccao_atual) > 0)
      limite_inferior_atual = bisseccao_atual;
    else
      raiz_exata_achada = true;
      if(funcao_avaliada(bisseccao_atual) == 0)
        melhor_palpite = bisseccao_atual;
      else
        melhor_palpite = limite_inferior_atual;
      endif
        motivo_parada = 'Raiz exata encontrada';
      break;
    endif
  endfor

  if (!raiz_exata_achada)
    melhor_palpite = bisseccao_atual;
    motivo_parada = 'Número máximo de iterações atingido';
  endif
  
endfunction

if (funcao_avaliada(limite_inferior) * funcao_avaliada(limite_superior) > 0)
  printf('ERRO: Pelo teorema de Bolzano, não é possível afirmar se há raízes para a função informada no intervalo informado. Tente novamente.');
else 