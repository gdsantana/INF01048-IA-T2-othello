# Othello | Trabalho 2 da disciplina de Inteligência Artificial INF01048

- Caio Corardi | 00279825 | Turma B

- Giovani da Silva | 00305086 | Turma A

- Guilherme Santana | 00301388 | Turma A

==============================================================================

## Condição de parada:
    Foi utilizado o tempo limite de 5 segundos ou que atinja um estado terminal


## Heuristicas:
  ### Cantos Capturados:
   A ideia é que no othello os cantos são posições valiosas, já que um vez capturados eles não pode ser recapturados pelo jogador adversário.
  
  ### Mobilidade Básica:
    A mobilidade é fundamental no jogo, tanto para maximizar as possibilidades do jogador, quanto para reduzir as possibilidades do oponente. A mobilidade básica é calculada com base na quantidade de movimentos disponíveis para o jogador e para o oponente
  
  ### Mobilidade Potencial:
    A mobilidade potencial atua de forma a prever a mobilidade em jogadas futuras, ou seja, a longo prazo. A mobilidade potencial é calculada verificando a quantidade de espaços vazios ao redor das peças do oponente

  ### Diferença de Pontos:
   Avalia o atual estado do tabuleiro e calcula a diferença de pontos entre os jogadores
  
  #### Proximidade dos cantos:
   Assim como é importante capturar um canto, é importante evitar que seu oponente capture. Peças contornando os cantos permitem que o oponente coloque uma peça no canto. Por isso, o ideal é evitar estas posições
  
  
  
  
  ### Algumas das dificuldades encontradas: 
  - Problemas em se acertar com a biblioteca de time;
  - Problema na retira do nó com melhor escolha;
  - Problema com jogadas inválidas quando a melhor não estava disponível
