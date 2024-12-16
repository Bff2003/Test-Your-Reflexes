# Shot With Your Hands

## A proposta 
Esta documento tem como objetivo apresentar a proposta para o projeto final da disciplina de computação visual. A ideia principal é a criação de um jogo que tem como objetivo usar a mão em gesto de pistola e tentar mirar nos alvos que apareceram no ecrã, sendo o projeto nomeado de "Shot With Your Hands". 

## Desafio Principal
O maior desafio deste projeto é a detecção de "para onde se esta a apontar no ecra", a ideia proposta de resolução é calcular a distancia entre o polegar o dedo indicador e a partir dai assumir que:
- Dedo polegar em um y menor que o indicador, apontar para cima
- Dedo polegar em um y maior que o indicador, apontar para baixo
- Dedo polegar em um y igual que o indicador, apontar para a frente 

## Motivação 
A motivação pela qual levou a criação desta proposta, foi o facto de pensar em algum jogo que pudesse ser jogado com as mãos.   

## Funcionalidades principais 
O projeto devera fazer uso do algoritmo MediaPipe (para reconhecimento da posição dos dedos) e devera conter as seguintes funcionalidades principais: 

| Funcionalidade                      | Prioridade |
| ----------------------------------- | ---------- |
| Detetar para onde se esta a apontar | P1         |
| Reconhecer o gesto de disparar      | P1         |
| Contador de Vidas                   | P3         |
| Apresentar inimigos no ecrã         | P1         |

Funcionalidades extras poderão ser acrescentadas no decorrer do desenvolvimento do projeto, contudo deverão ser desenvolvidas somente e exclusivamente apos todas as outras funcionalidades terem sido desenvolvidas corretamente. 

## Público alvo 
O "Shot With Your Hands" tem como objetivo principal ser usado para entretenimento e tem o seguinte publico alvo: 
- Jovens e Adultos que gostam de jogar.