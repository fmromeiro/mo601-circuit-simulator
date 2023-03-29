# MO601 2023S1 Projeto 1 - Simulador de Circuitos

> Felipe Martins Romeiro - 215720  
> Vinícius Waki Teles - 257390

Neste projeto desenvolvemos um simulador de circuitos que a partir de uma descrição do circuito e de uma série de entradas descreve o estado do circuito a cada clock, simulando um cenário em que não há atraso nas portas lógicas e em que este atraso é de 1 clock.

## Execução

Para executar os testes na pasta `test`, basta rodar `docker compose up`. Esse comando vai rodar um script python que detecta os testes, executa as simulações e as coloca nas subpastas de `test`, sobrescrevendo as saídas que estiverem lá.

## Algoritmo

O algoritmo de simulação é separado entre a simulação de atraso 0 e a simulação de atraso 1.

A simulação de atraso 1 é mais simples. Nela, a cada ciclo de clock passamos por todos os sinais e atualizamos os seus valores com base no valores dos sinais no último ciclo, gerando o estado para o clock atual. Para isso mantemos um dicionário que mapeia o nome do sinal à sua porta lógica e aos sinais de entrada dessa porta lógica. Para encerrar a simulação, esperamos que existam dois estados consecutivos iguais e que não haja mais nenhum estimulo a ser inserido no circuito no arquivo de estimulos.txt. Também encerramos a simulação depois de um número predeterminado de ciclos, evitando que testes que não estabilizam impeçam a execução dos demais testes.

Já a simulação de atraso 0 é semelhante, com a diferença de que esperamos que o estado estabilize também dentro de cada clock. Para isso, a cada ciclo de clock, criamos uma série de ciclos de _delta_ que funcionam da mesma maneira da simulação de atraso 1 descrita acima, isto é, os sinais são atualizados com base no estado de _delta_ anterior e a simulação de delta é encerrada quando o estado delta estabiliza por dois ciclos ou o limite de ciclos é superado. O último estado delta é então copiado para o estado de clock atual, e caso o estado de clock esteja estabilizado e não hajam mais entradas, encerramos a simulação.

## Testes

Primeiro, desenvolvemos testes para cada uma das portas lógicas, basicamente copiando a sua tabela verdade para um teste, validando a implementação de cada uma delas. Depois, testamos o circuito dado como exemplo na especificação do projeto, validando o encadeamento de portas lógicas. Em seguida, testamos algumas features dos arquivos de entrada, como o passo variável do arquivo de estímulos. Por fim, testamos alguns casos de borda, como circuitos em loop, circuitos que possuem ciclos no meio e circuitos "em paralelo", ou seja, dois circuitos que não se comunicam dentro de um mesmo teste.

## Conclusão

No desenvolvimento deste projeto aprendemos sobre como simular a propagação de sinais e a passagem de tempo em circuitos lógicos. Estes dois conhecimentos podem ser úteis em outras aplicações, como em outras aplicações de simulação ou em sistemas de logística. Também desenvolvemos um maior intuição sobre como aplicações de simulação e a propagação de sinais em circuitos funcionam.